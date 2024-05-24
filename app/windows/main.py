'''
all windows helpers will be here
TODO: This is temp test code, will moved later depending on how we package the app for windows
'''
import os
import requests
import uuid
import json

from dotenv import load_dotenv
load_dotenv()

from utils.apps import app_list, launch_app
from utils.screenshot import capture_screenshot
from utils.user import get_userid
from utils.common import get_temp_path, get_temp_session_path

# temperory code for excel
from utils.tooling import sample_prompt, keyboard_mouse, xmlResponseToDict, verify_prompt, correction_prompt
from utils.control import execute_action
import base64
import time

def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

headers = {
  "Content-Type": "application/json",
  "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}"
}



# App name
app_name = "autoUIAssist"
# App base temp path
app_temp_path = get_temp_path(app_name)
# current user id
userid = get_userid(app_temp_path)
# current run session id
user_session_uuid = str(uuid.uuid4())
# current session path
temp_session_path = get_temp_session_path(app_temp_path, user_session_uuid)
# the endpoint url
api_url = os.getenv("API_URL")
# complete app list
os_apps = app_list(user_session_uuid)

# Takes input from users
user_task = input("Enter your user_task: ")

task_corrector_uri = f"{api_url}/task_corrector"
task_corrector_payload = {
    "userid": userid,
    "sessionid": user_session_uuid,
    "os": "windows",
    "task": user_task,
    "app_list": os_apps,
}
response = requests.post(task_corrector_uri, json=task_corrector_payload)
response = json.loads(response.text)
print(f"Corrected task: {response['corrected_task']}")

# [[IMP]] user_task
user_task = response["corrected_task"]

launch_app_list = response["selected_app_list"]
print(f"Launch app list: {launch_app_list}")

# check if "refinement" key in response
if response["refinement"]:
    print("Refinement requested")
    
    # trigger refinement url at /task_refiner_stage_1
    task_refiner_stage_1_uri = f"{api_url}/task_refiner_stage_1"
    task_refiner_stage_1_payload = {
        "userid": userid,
        "sessionid": user_session_uuid,
        "os": "windows",
        "task": user_task,
    }
    response = requests.post(task_refiner_stage_1_uri, json=task_refiner_stage_1_payload)
    response = json.loads(response.text)
    print(f"Refinement questions: {response['refinement_question_list']}")
    qna_str = ""
    for question in response['refinement_question_list']:
        user_answer = input(f"Q: {question}\n A: ")
        qna_str = qna_str + f"{question}\n{user_answer}\n\n"
    print("Refinement data collected: \n", qna_str)
    
    # trigger refinement url at /task_refiner_stage_2
    task_refiner_stage_2_uri = f"{api_url}/task_refiner_stage_2"
    task_refiner_stage_2_payload = {
        "userid": userid,
        "sessionid": user_session_uuid,
        "os": "windows",
        "task": user_task,
        "refinement_data": qna_str,
    }
    response = requests.post(task_refiner_stage_2_uri, json=task_refiner_stage_2_payload)
    response = json.loads(response.text)
    print(f"Final refined task: {response['refined_task']}")
    # [[IMP]] user_task
    user_task = response["refined_task"]
    
# Create rough step planner
step_creation_stage_1_uri = f"{api_url}/step_creation_stage_1"
step_creation_stage_1_payload = {
    "userid": userid,
    "sessionid": user_session_uuid,
    "os": "windows",
    "task": user_task,
}
response = requests.post(step_creation_stage_1_uri, json=step_creation_stage_1_payload)
response = json.loads(response.text)
print(f"Step planner: {response['step_list']}")
# [[IMP]] step_list
step_list = response["step_list"]

# Generate summary from task_step_summarization endpoint
task_step_summarization_uri = f"{api_url}/task_step_summarization"
task_step_summarization_payload = {
    "userid": userid,
    "sessionid": user_session_uuid,
    "os": "windows",
    "task": user_task,
    "step_list": step_list,
}
response = requests.post(task_step_summarization_uri, json=task_step_summarization_payload)
response = json.loads(response.text)
print(f"Task summary: {response['summary']}")

with open(f"logs/response.json", "w") as f:
    json.dump(response, f, indent=4)

# [[IMP]] Task summary, scratchpad
task_summary = response["summary"]
task_scratchpad = response["scratchpad"]

screenshot_list = []

step_id = 0
for step in step_list:
    print(f"Step: {step}")
    # check app list, launch first app
    # take a screenshot: annotated and rectangle store as a object in screenshot_list
    temp_session_step_path = os.path.join(temp_session_path, f"step_{step_id}")
    app_window_ann_screenshot_path, app_window_coordinate_dict = capture_screenshot(
        screenshot_type="app_window",
        app_title="Excel",
        temp_session_step_path=temp_session_step_path
    )
    # compile: current step + task summary + current screenshot + current-1 screenshot, all agents and tools data -> gpt-4o ::: EXPENSIVE
    the_prompt = sample_prompt.format(
        TASK_SUMMARY=task_summary,
        CURRENT_STEP=step_list[step_id],
        TOOLING_AVAILABLE=keyboard_mouse,
    )
    step_id += 1
    base64_image = encode_image(app_window_ann_screenshot_path)
    payload = {
        "model": "gpt-4o",
        "temperature": 0,
        "messages": [
            {
            "role": "user",
            "content": [
                {
                "type": "text",
                "text": the_prompt
                },
                {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{base64_image}"
                }
                }
            ]
            }
        ]
    }
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    print(response.json())

    # save to a file for inspection
    full_response = response.json()
    full_response["prompt"] = the_prompt
    with open(f"logs/response_{step_id}.json", "w") as f:
        json.dump(full_response, f, indent=4)
    
    content = full_response["choices"][0]["message"]["content"]
    if len(content) <= 10:
        print("No action detected")
        continue

    action_dict = xmlResponseToDict(content)
    # pretty print action_dict to a file and save it for inspection
    with open(f"logs/action_dict_{step_id}.json", "w") as f:
        json.dump(action_dict, f, indent=4)

    # if action_dict is empty, continue to next step
    if action_dict['step_list'] == []:
        continue

    def process_actions(step_list):
        action_list = []
        step_list = step_list['step_list']
        step_id = 1
        for step in step_list:
            action_obj = step[f'step_{step_id}']
            if "text_list" in action_obj["parameters"]:
                action_obj["parameters"]["keys"] = list(action_obj["parameters"]["text_list"][0])
                del action_obj["parameters"]["text_list"]
            elif "key_list" in action_obj["parameters"]:
                action_obj["parameters"]["keys"] = action_obj["parameters"]["key_list"]
                del action_obj["parameters"]["key_list"]
            action_list.append(action_obj)
            step_id += 1
        return action_list
    action_list = process_actions(action_dict)

    action_id = 0
    for action in action_list:
        print(action)
        screenshot_before_action = capture_screenshot(screenshot_type="app_window", app_title="Excel", temp_session_step_path=temp_session_step_path)
        execute_action(action)
        screenshot_after_action = capture_screenshot(screenshot_type="app_window", app_title="Excel", temp_session_step_path=temp_session_step_path)
        # combine the two screenshots
        action_screenshot = capture_screenshot(screenshot_type="concat", concat_images=[screenshot_before_action, screenshot_after_action], temp_session_step_path=temp_session_step_path)
        print("action_screenshot: ", action_screenshot)
        action_screenshot = encode_image(action_screenshot[0])
        # verify the action worked
        the_prompt = verify_prompt.format(ACTION=json.dumps(action))
        payload = {
            "model": "gpt-4o",
            "temperature": 0,
            "messages": [
                {
                "role": "user",
                "content": [
                    {
                    "type": "text",
                    "text": the_prompt
                    },
                    {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{action_screenshot}"
                    }
                    }
                ]
                }
            ]
        }
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
        print(response.json())

        # save to a file for inspection
        full_response = response.json()
        with open(f"logs/response_{step_id}_verify.json", "w") as f:
            json.dump(full_response, f, indent=4)
        
        content = response.json()["choices"][0]["message"]["content"]
        
        if "true" in content.lower():
            print("Action verified")
            action_id += 1
            continue
        elif "false" in content.lower():
            print("Action not verified")
            old_action = action
            if action_id+1 < len(action_list):
                new_action = action_list[action_id+1]
            else:
                new_action = "no new action left"
            the_prompt = correction_prompt.format(
                TOOLING=keyboard_mouse,
                PERFORMED_ACTION=json.dumps(old_action),
                PREPARE_FOR_ACTION=json.dumps(new_action)
            )
            payload = {
                "model": "gpt-4o",
                "temperature": 0,
                "messages": [
                    {
                    "role": "user",
                    "content": [
                        {
                        "type": "text",
                        "text": the_prompt
                        },
                        {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{action_screenshot}"
                        }
                        }
                    ]
                    }
                ]
            }
            response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
            print(response.json())
            full_response = response.json()
            full_response["prompt"] = the_prompt
            with open(f"logs/response_{step_id}_correction.json", "w") as f:
                json.dump(full_response, f, indent=4)
            
            content = response.json()["choices"][0]["message"]["content"]
            if len(content) <= 10:
                print("No action detected")
                continue

            correction_action_dict = xmlResponseToDict(content)
            # pretty print action_dict to a file and save it for inspection
            with open(f"logs/action_dict_{step_id}_correction.json", "w") as f:
                json.dump(action_dict, f, indent=4)
                
            correction_action_list = process_actions(correction_action_dict)
            correction_action_id = 0
            for correction_action in correction_action_list:
                print(correction_action)
                execute_action(correction_action)

    time.sleep(0.2)
