'''
[[Milestone]] 1: Complete the Excel Integration
1. Fix the agent: Refinement and high level Action Plan Creation [[DONE]] (Milestone 0.25)
    - Task expanding - Claude Sonnet [[DONE]]
    - Select main office app to be used (Excel in our case) [[DONE]]
    - Create a new action plan for that office app (Excel in our case) [[DONE]]
    - Verify the Action plan against a set of predefined rules [[DONE]]
        - Every action should be an executable or workable action
        - No actions like think or plan or so on
    - Verify with user input [[DONE]]
        - Let the user edit the final action plan before execution

2. Action Plan Creation for Excel: [[WIP]] (Milestone 0.5)
    - create a textual dictionary of helper functions [[TODO]] (use __doc__ attribute of functions)
    - Generate low level action plan for each high level action [[TODO]]
    - Execute a action at a time [[TODO]]
    - Verify each action with the tool use description - Use Haiku for verification [[TODO]]
    - If any action execution fails, jump back to the previous step and try again (max 3 times) [[TODO]]

3. Create a UI for this complete process [[TODO]] (Milestone 0.75)
    - Add ability to switch between apps to deal with switching for user input and so on [[TODO]]
4. Create a simple portable PyInstaller package for this app [[TODO]] (Milestone 1)

[[Milestone]] 2: Add the Word Integration (Milestone 2)
1. Pick up some tasks for Word [[TODO]]
2. Implement a set of tooling for Word [[TODO]]
3. Implement a set of actions for Word [[TODO]]
4. Implement a set of fewshot prompts for Word [[TODO]]

[[Milestone]] 3: Finally add the PowerPoint Integration (Milestone 3)
1. Pick up some tasks for PowerPoint [[TODO]]
2. Implement a set of tooling for PowerPoint [[TODO]]
3. Implement a set of actions for PowerPoint [[TODO]]
4. Implement a set of fewshot prompts for PowerPoint [[TODO]]
'''

import os
import requests
import uuid
import json
import concurrent.futures
import time

from dotenv import load_dotenv
load_dotenv()

from utils.apps import app_list, office_app_list
from action.screenshot import capture_screenshot
from utils.user import get_userid
from utils.common import get_temp_path, get_temp_session_path, get_input_with_timeout
from utils.api import retry_api_call

# temperory code for excel
from utils.tooling import sample_prompt, keyboard_mouse, xmlResponseToDict, verify_prompt, correction_prompt
from app.windows.action.control import execute_action
import base64

def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

headers = {
  "Content-Type": "application/json",
  "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}"
}

# [[PART]] 1: Setup the app & user environment
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

# [[PART]] 2: Take the user task as input and correct it for clarity
# Takes the first user task as input
user_task = input("Enter your user_task: ")

@retry_api_call(max_attempts=3, delay=1)
def task_corrector():
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
    return response

response = task_corrector()
user_task = response["corrected_task"]

# [[PART]] 2.1: Extract complete app list from the corrected task
launch_app_list = response["selected_app_list"]
print(f"Launch app list: {launch_app_list}")

# [[PART]] 2.1.1: Extract the first office app from the launch_app_list
# first_office_app_type contains the string "excel"
# extract active window, get the title and check if it contains first_office_app_type
first_office_app, first_office_app_type = office_app_list(os_apps=launch_app_list)
print(f"First Office App: {first_office_app}\n First Office App Type: {first_office_app_type}")

# [[PART]] 3: If the task needs refinement, trigger the refinement process
if response["refinement"]:
    print("Refinement requested")
    
    # trigger refinement url at /task_refiner_stage_1
    @retry_api_call(max_attempts=3, delay=1)
    def task_refiner_stage_1():
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
        return response

    response = task_refiner_stage_1()

    # [[PART]] 3.1: Take user input for the refinement questions
    qna_str = ""
    for question in response['refinement_question_list']:
        user_answer = input(f"Q: {question}\n A: ")
        qna_str = qna_str + f"{question}\n{user_answer}\n\n"
    print("Refinement data collected: \n", qna_str)
    
    # [[PART]] 3.2: Augment the user task with the refinement data & generate the final refined task
    # trigger refinement url at /task_refiner_stage_2
    @retry_api_call(max_attempts=3, delay=1)
    def task_refiner_stage_2():
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
        print(response)
        print(f"Final refined task: {response['refined_task']}")
        return response
    
    response = task_refiner_stage_2()
    user_task = response["refined_task"]

# [[PART]] 4: Generate the high level action plan
@retry_api_call(max_attempts=3, delay=1)
def high_level_action_plan_creation():
    high_level_action_plan_creation_uri = f"{api_url}/high_level_action_plan_creation"
    high_level_action_plan_creation_payload = {
        "userid": userid,
        "sessionid": user_session_uuid,
        "os": "windows",
        "task": user_task,
        "app": first_office_app_type,
    }
    response = requests.post(high_level_action_plan_creation_uri, json=high_level_action_plan_creation_payload)
    response = json.loads(response.text)
    print(f"Step planner: {response['step_list']}")
    return response

response = high_level_action_plan_creation()
step_list = response["step_list"]

# [[PART]] 5: Verify the action plan & iterate over the verification process if needed
MAX_ATTEMPTS = 3
CURRENT_ATTEMPT = 0
while CURRENT_ATTEMPT < MAX_ATTEMPTS:
    CURRENT_ATTEMPT += 1
    print(f"Attempt: {CURRENT_ATTEMPT}")
    # [[PART]] 4.1: Verify the action plan
    @retry_api_call(max_attempts=3, delay=1)
    def action_plan_verifier():
        action_plan_verifier_uri = f"{api_url}/action_plan_verifier"
        action_plan_verifier_payload = {
            "userid": userid,
            "sessionid": user_session_uuid,
            "os": "windows",
            "task": user_task,
            "step_list": step_list,
        }
        response = requests.post(action_plan_verifier_uri, json=action_plan_verifier_payload)
        response = json.loads(response.text)
        print(f"Verified steps: {response}")
        return response

    response = action_plan_verifier()
    verified = response["verified"]
    GLOBAL_ACTION_PLAN_SCRATCHPAD = response["scratchpad"]

    # [[PART]] 4.2: Ask user to help correct or if user input left empty use scratchpad as a fix
    if 'true' == verified.strip().lower():
        print("Action plan verified")
        break
    else:
        print("Action plan not verified")
        print("Scratchpad: ", GLOBAL_ACTION_PLAN_SCRATCHPAD)
        # user_input = input("Please help correct the action plan (if left empty will use scratchpad to refine it further): ")
        user_input = get_input_with_timeout("Please help correct the action plan (if left empty will use scratchpad to refine it further. Field timesout in 5): ", 5)
        if user_input:
            GLOBAL_ACTION_PLAN_SCRATCHPAD = GLOBAL_ACTION_PLAN_SCRATCHPAD + "\n User Feedback: " + user_input

        # trigger refinement url at /action_plan_refiner
        @retry_api_call(max_attempts=3, delay=1)
        def action_plan_refiner():
            action_plan_refiner_uri = f"{api_url}/action_plan_refiner"
            action_plan_refiner_payload = {
                "userid": userid,
                "sessionid": user_session_uuid,
                "os": "windows",
                "task": user_task,
                "step_list": step_list,
                "feedback": GLOBAL_ACTION_PLAN_SCRATCHPAD,
            }
            response = requests.post(action_plan_refiner_uri, json=action_plan_refiner_payload)
            response = json.loads(response.text)
            print(f"Refined steps: {response}")
            return response
        
        response = action_plan_refiner()
        step_list = response["step_list"]
else:
    print("Action plan not verified after 3 attempts. Exiting...")
    exit()

# [[PART]] 5: Summarize the task and steps for action plan generation
@retry_api_call(max_attempts=3, delay=1)
def task_step_summarization():
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
    return response

response = task_step_summarization()
task_summary = response["summary"]
task_scratchpad = response["scratchpad"]

# # [[PART]] 6: Clear the logs folder
# for file in os.listdir("logs"):
#     if file.endswith(".json"):
#         os.remove(os.path.join("logs", file))


# action_dict = {}
# step_id = 0
# for step in step_list:
#     print(f"Step: {step}")
#     # take a screenshot: annotated and rectangle store as a object in screenshot_list
#     temp_session_step_path = os.path.join(temp_session_path, f"step_{step_id}")
#     app_window_ann_screenshot_path, app_window_coordinate_dict = capture_screenshot(
#         screenshot_type="app_window",
#         app_title="Excel",
#         temp_session_step_path=temp_session_step_path
#     )

#     # TODO: WE ARE HERE JUST SO THAT YOU KNOW! thats roughly 30% of the work done

#     # compile: current step + task summary + current screenshot + current-1 screenshot, all agents and tools data -> gpt-4o ::: EXPENSIVE
#     the_prompt = sample_prompt.format(
#         TASK_SUMMARY=task_summary,
#         CURRENT_STEP=step_list[step_id],
#         # CURRENT_STEP=json.dumps(step_list),
#         TOOLING_AVAILABLE=keyboard_mouse,
#     )
#     step_id += 1
#     base64_image = encode_image(app_window_ann_screenshot_path)
#     payload = {
#         "model": "gpt-4o",
#         "temperature": 0,
#         "messages": [
#             {
#             "role": "user",
#             "content": [
#                 {
#                 "type": "text",
#                 "text": the_prompt
#                 },
#                 {
#                 "type": "image_url",
#                 "image_url": {
#                     "url": f"data:image/jpeg;base64,{base64_image}"
#                 }
#                 }
#             ]
#             }
#         ]
#     }

#     @retry_api_call(max_attempts=3, delay=1)
#     def get_response():
#         response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
#         print(response.json())
        
#         # save to a file for inspection
#         full_response = response.json()
#         full_response["prompt"] = the_prompt
#         with open(f"logs/response_{step_id}.json", "w") as f:
#             json.dump(full_response, f, indent=4)
        
#         content = full_response["choices"][0]["message"]["content"]
        
#         return content, full_response
    
#     content, full_response = get_response()
    
#     if len(content) <= 10:
#         print("No action detected")
#         continue

#     action_dict = xmlResponseToDict(content)
#     # pretty print action_dict to a file and save it for inspection
#     with open(f"logs/action_dict_{step_id}.json", "w") as f:
#         json.dump(action_dict, f, indent=4)

#     # if action_dict is empty, continue to next step
#     if action_dict['step_list'] == []:
#         continue

#     def process_actions(step_list):
#         action_list = []
#         step_list = step_list['step_list']
#         step_id = 1
#         for step in step_list:
#             action_obj = step[f'step_{step_id}']
#             if "text_list" in action_obj["parameters"]:
#                 action_obj["parameters"]["keys"] = list(action_obj["parameters"]["text_list"][0])
#                 del action_obj["parameters"]["text_list"]
#             elif "key_list" in action_obj["parameters"]:
#                 action_obj["parameters"]["keys"] = action_obj["parameters"]["key_list"]
#                 del action_obj["parameters"]["key_list"]
#             action_list.append(action_obj)
#             step_id += 1
#         return action_list
#     action_list = process_actions(action_dict)

#     screenshot_before_action = capture_screenshot(screenshot_type="app_window", app_title="Excel", temp_session_step_path=temp_session_step_path)
#     action_id = 0
#     for action in action_list:
#         print(action)
#         execute_action(action)
#         time.sleep(0.2)

    # # verify complete action list
    # screenshot_after_action = capture_screenshot(screenshot_type="app_window", app_title="Excel", temp_session_step_path=temp_session_step_path)
    # # combine the two screenshots
    # action_screenshot = capture_screenshot(screenshot_type="concat", concat_images=[screenshot_before_action, screenshot_after_action], temp_session_step_path=temp_session_step_path)
    # print("action_list_screenshot: ", action_screenshot)
    # action_screenshot = encode_image(action_screenshot[0])
    # # verify the action worked
    # the_prompt = verify_prompt.format(ACTION=json.dumps(action_list))
    # payload = {
    #     "model": "gpt-4o",
    #     "temperature": 0,
    #     "messages": [
    #         {
    #         "role": "user",
    #         "content": [
    #             {
    #             "type": "text",
    #             "text": the_prompt
    #             },
    #             {
    #             "type": "image_url",
    #             "image_url": {
    #                 "url": f"data:image/jpeg;base64,{action_screenshot}"
    #             }
    #             }
    #         ]
    #         }
    #     ]
    # }
    # @retry_api_call(max_attempts=3, delay=1)
    # def get_verify_response():
    #     response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    #     print(response.json())
        
    #     # save to a file for inspection
    #     full_response = response.json()
    #     with open(f"logs/response_{step_id}_verify.json", "w") as f:
    #         json.dump(full_response, f, indent=4)
        
    #     content = full_response["choices"][0]["message"]["content"]
        
    #     return content, full_response
    
    # content, full_response = get_verify_response()
    
    # if "true" in content.lower():
    #     print("Action verified")
    #     step_id += 1
    #     continue
    # elif "false" in content.lower():
    #     print("Action not verified")
    #     old_step = step
    #     if step_id+1 < len(step_list):
    #         new_step = step_list[step_id+1]
    #     else:
    #         new_step = "no new step left"
    #     the_prompt = correction_prompt.format(
    #         TASK_SUMMARY=task_summary,
    #         TOOLING=keyboard_mouse,
    #         PERFORMED_STEP=old_step,
    #         PERFORMED_ACTION_LIST=json.dumps(action_list),
    #         PREPARE_FOR_NEXT_STEP=json.dumps(new_step)
    #     )
    #     payload = {
    #         "model": "gpt-4o",
    #         "temperature": 0,
    #         "messages": [
    #             {
    #             "role": "user",
    #             "content": [
    #                 {
    #                 "type": "text",
    #                 "text": the_prompt
    #                 },
    #                 {
    #                 "type": "image_url",
    #                 "image_url": {
    #                     "url": f"data:image/jpeg;base64,{action_screenshot}"
    #                 }
    #                 }
    #             ]
    #             }
    #         ]
    #     }
    #     @retry_api_call(max_attempts=3, delay=1)
    #     def get_correction_response():
    #         response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    #         print(response.json())
            
    #         # save to a file for inspection
    #         full_response = response.json()
    #         full_response["prompt"] = the_prompt
    #         with open(f"logs/response_{step_id}_correction.json", "w") as f:
    #             json.dump(full_response, f, indent=4)
            
    #         content = response.json()["choices"][0]["message"]["content"]
            
    #         return content, full_response
        
    #     content, full_response = get_correction_response()
    #     if len(content) <= 10:
    #         print("No action detected")
    #         continue
    #     correction_action_dict = xmlResponseToDict(content)
    #     # pretty print action_dict to a file and save it for inspection
    #     with open(f"logs/action_dict_{step_id}_correction.json", "w") as f:
    #         json.dump(correction_action_dict, f, indent=4)
            
    #     correction_action_list = process_actions(correction_action_dict)
    #     correction_action_id = 0
    #     for correction_action in correction_action_list:
    #         print(correction_action)
    #         execute_action(correction_action)

    # time.sleep(0.2)
    # break
