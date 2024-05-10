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

user_task = input("Enter your user_task: ")

api_url = os.getenv("API_URL")
stage_1_uri = f"{api_url}/plan_stage_1"

os_apps = app_list(user_session_uuid)
launch_app_list = []

TASK_REFINEMENT_MAX_TRIES = int(os.getenv("TASK_REFINEMENT_MAX_TRIES", 3))
refinement_tries = 0
refinement_qa_str = ''
while True:

    if refinement_tries >= TASK_REFINEMENT_MAX_TRIES:
        break

    stage_1_data = {
        "userid": get_userid(),
        "sessionid": user_session_uuid,
        "task": user_task,
        "app_list": os_apps,
        "os": "windows",
        "refinement": refinement_qa_str
    }

    response = requests.post(stage_1_uri, json=stage_1_data)
    response = json.loads(response.text)
    stage_1_data["task"] = response['corrected_task']
    launch_app_list = response['launch_app_list']
    refinement_questions = response['refinement_questions']
    if refinement_questions:
        for question in refinement_questions:
            answer = input(question + " ")
            refinement_qa_str = f"\n\n{question}\n{answer}"
        stage_1_data['refinement'] = refinement_qa_str
        refinement_tries += 1
    else:
        break

print(json.dumps(stage_1_data, indent=2))
