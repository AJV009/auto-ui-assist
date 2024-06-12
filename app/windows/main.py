import os
import requests
import uuid
import json
import importlib

from dotenv import load_dotenv
import pyautogui
load_dotenv()

from utils.apps import app_list, office_app_list
from utils.user import get_userid
from utils.common import get_temp_path, get_temp_session_path, get_input_with_timeout, encode_image
from utils.api import retry_api_call

from action.screenshot import capture_screenshot

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

desktop_image = pyautogui.screenshot()
desktop_image_encoded = encode_image(IMAGE_object=desktop_image)

@retry_api_call(max_attempts=3, delay=1)
def task_corrector():
    task_corrector_uri = f"{api_url}/task_corrector"
    task_corrector_payload = {
        "userid": userid,
        "sessionid": user_session_uuid,
        "os": "windows",
        "task": user_task,
        "app_list": os_apps,
        "image_base64": desktop_image_encoded,
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
first_office_app_name = first_office_app_type[1]
first_office_app_type = first_office_app_type[0]
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
            "image_base64": desktop_image_encoded
        }
        response = requests.post(task_refiner_stage_1_uri, json=task_refiner_stage_1_payload)
        response = json.loads(response.text)
        print(f"Refinement questions: {response['refinement_question_list']}")
        return response

    response = task_refiner_stage_1()

    # [[PART]] 3.1: Take user input for the refinement questions
    qna_str = ""
    print("Please answer the following questions for task refinement: \n")
    for question in response['refinement_question_list']:
        user_answer = get_input_with_timeout(f"Q: {question}\n A: ", 5)
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
        "image_base64": desktop_image_encoded,
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
    print(f"Attempt {CURRENT_ATTEMPT} to verify the action plan")
    # [[PART]] 4.1: Verify the action plan
    @retry_api_call(max_attempts=3, delay=1)
    def action_plan_verifier():
        action_plan_verifier_uri = f"{api_url}/action_plan_verifier"
        action_plan_verifier_payload = {
            "userid": userid,
            "sessionid": user_session_uuid,
            "os": "windows",
            "task": user_task,
            "step_list": json.dumps(step_list),
            "image_base64": desktop_image_encoded,
        }
        response = requests.post(action_plan_verifier_uri, json=action_plan_verifier_payload)
        response = json.loads(response.text)
        print(f"Verified: {response['verified']}\n Scratchpad: {response['scratchpad']}")
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
        user_input = get_input_with_timeout("Please help correct the action plan (if left empty will use scratchpad to refine it further. Field timesout in 5 sec): ", 5)
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
                "image_base64": desktop_image_encoded,
            }
            response = requests.post(action_plan_refiner_uri, json=action_plan_refiner_payload)
            response = json.loads(response.text)
            print(f"Refined steps: {response['step_list']}")
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
        "step_list": json.dumps(step_list),
    }
    response = requests.post(task_step_summarization_uri, json=task_step_summarization_payload)
    response = json.loads(response.text)
    print(f"Task summary: {response['summary']}")
    return response

response = task_step_summarization()
task_summary = response["summary"]
task_scratchpad = response["scratchpad"]

# [[PART]] 6: Clear the logs folder
# for file in os.listdir("logs"):
#     if file.endswith(".json"):
#         os.remove(os.path.join("logs", file))

# [[PART]] 7: Iterate over the steps, record actions, run actions, verify actions, revert if needed
action_dict = {}

# # [[PART]] 7.1: Import the TOOLING using importlib & first_office_app_type
module = importlib.import_module(f"app_tools.{first_office_app_type}.function_call_repo")
TOOLING = module.TOOLING

step_id = 0
for i, step in enumerate(step_list):
    step = step[f"step_{i+1}"]
    print(f"Step: {step}")

    # [[PART]] 7.2: take a screenshot: annotated and rectangle store as a object in screenshot_list
    temp_session_step_path = os.path.join(temp_session_path, f"step_{i+1}")
    app_window_ann_screenshot_path, app_window_coordinate_dict = capture_screenshot(
        screenshot_type="app_window",
        app_title=first_office_app_name,
        temp_session_step_path=temp_session_step_path
    )
    app_window_ann_screenshot_base64 = encode_image(app_window_ann_screenshot_path)

    # [[PART]] 7.3: record the action
    action_dict[f"step_{i+1}"] = {
        "high_level_action": step,
        "low_level_actions": {},
        "record": {
            "before_screenshot": app_window_ann_screenshot_path,
            "after_screenshot": None,
        }
    }

    # [[PART]] 7.4: Generate the low level action plan for each high level action
    @retry_api_call(max_attempts=3, delay=1)
    def low_level_action_plan_creation():
        low_level_action_plan_creation_uri = f"{api_url}/low_level_action_plan_creation"
        low_level_action_plan_creation_payload = {
            "userid": userid,
            "sessionid": user_session_uuid,
            "os": "windows",
            "task": user_task,
            "step": step,
            "app": first_office_app_type,
            "tooling": json.dumps(TOOLING),
            "image_base64": app_window_ann_screenshot_base64,
        }
        response = requests.post(low_level_action_plan_creation_uri, json=low_level_action_plan_creation_payload)
        response = json.loads(response.text)
        print(f"Low level action plan: {response}")
        return response

    response = low_level_action_plan_creation()
    # save to log file for debugging
    # with open(f"logs/low_level_action_plan_{step_id}.json", "w") as f:
    #     json.dump(response, f)
    low_level_action_plan = response['action_list']
    action_dict[f"step_{i+1}"]["low_level_actions"] = low_level_action_plan

    if len(low_level_action_plan) <= 0:
        step_id += 1
        print("No action detected")
        continue
    
    # [[PART]] 7.5: Iterate over the low level actions & just run them
    for i, action in enumerate(low_level_action_plan):
        action = action[f'action_{i+1}']
        print("Action: ", action)

        # [[PART]] 7.5.1: Extract the function call & parameters
        function_name = action['action_function_call']
        # if action has the key parameters, extract the parameters
        if "parameters" in action:
            parameters = action['parameters']
            # parameters is a dict of key value pairs
        else:
            parameters = None

        # [[PART]] 7.5.2: Run the function call: Call function_name with parameters
        # check for function_name in TOOLING and call the function_path with parameters
        for tool in TOOLING:
            if tool['name'] == function_name:
                function_path = tool['function_path']
                break
        # import the function_path and call the function with parameters
        module = importlib.import_module(function_path)
        function_call = getattr(module, function_name)
        if parameters:
            function_call(**parameters)
        else:
            function_call()
