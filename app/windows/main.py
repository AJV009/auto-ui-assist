'''
all windows helpers will be here
TODO: This is temp test code, will moved later depending on how we package the app for windows
'''
import requests
from utils.apps import app_list, launch_app
from utils.user import get_userid
import os
from dotenv import load_dotenv
import uuid
import json

load_dotenv()

user_session_uuid = str(uuid.uuid4())
api_url = os.getenv("API_URL")
os_apps = app_list(user_session_uuid)

user_task = input("Enter your user_task: ")

task_corrector_uri = f"{api_url}/task_corrector"
task_corrector_payload = {
    "userid": get_userid(),
    "sessionid": user_session_uuid,
    "os": "windows",
    "task": user_task,
    "app_list": os_apps,
}
response = requests.post(task_corrector_uri, json=task_corrector_payload)
response = json.loads(response.text)
print(f"Corrected task: {response['corrected_task']}")

launch_app_list = response["launch_app_list"]
print(f"Launch app list: {launch_app_list}")

# check if "refinement" key in response
if "refinement" in response:
    # TASK_REFINEMENT_MAX_TRIES = int(os.getenv("TASK_REFINEMENT_MAX_TRIES", 3))
    print("Refinement requested")
    user_task = response["corrected_task"]
    
    # trigger refinement url at /task_refiner
    task_refiner_uri = f"{api_url}/task_refiner"
    task_refiner_payload = {
        "userid": get_userid(),
        "sessionid": user_session_uuid,
        "os": "windows",
        "task": user_task,
    }
    response = requests.post(task_refiner_uri, json=task_refiner_payload)
    response = json.loads(response.text)
    print(f"Refined task: {response['refined_task']}")
    print(f"Refinement questions: {response['refinement_questions']}")
    qna_str = "Further refinement data:\n"
    for question in response['refinement_questions']:
        user_answer = input(f"{question}: ")
        qna_str = qna_str + f"{question}: {user_answer}\n"
    print("Refinement data collected: \n", qna_str)
    
    # trigger refinement url at /task_refiner_stage_2
    task_refiner_stage_2_uri = f"{api_url}/task_refiner_stage_2"
    task_refiner_stage_2_payload = {
        "userid": get_userid(),
        "sessionid": user_session_uuid,
        "os": "windows",
        "task": user_task + "\n" + qna_str,
    }
    response = requests.post(task_refiner_stage_2_uri, json=task_refiner_stage_2_payload)
    response = json.loads(response.text)
    print(f"Final refined task: {response['refined_task']}")
