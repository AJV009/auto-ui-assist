'''
all windows helpers will be here
TODO: This is temp test code, will moved later depending on how we package the app for windows
'''
import os
import requests
import uuid
import json

from dotenv import load_dotenv

from utils.apps import app_list, launch_app
from utils.screenshot import capture_screenshot
from utils.user import get_userid
from utils.common import get_temp_path, get_temp_session_path

load_dotenv()

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

# [[IMP]] Task summary, scratchpad
task_summary = response["task_summary"]
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
    # compile: current step + task summary + current screenshot + current-1 screenshot, all agents and tools data -> gpt-4o EXPENSIVE
    # genereate execution step
    
