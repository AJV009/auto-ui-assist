'''
all windows helpers will be here
TODO: This is temp test code, will moved later depending on how we package the app for windows
'''
import requests
from utils.apps import app_list, launch_app
import os
from dotenv import load_dotenv
import uuid
import json

load_dotenv()

'''
TODO:
1. Take the query from the user using stdin
2. Enable Query Corrector
    Returns the following:
    - Corrected Query
    - Extracted launch applications in order
    - Additional questions for the user
4. Take the new user inputs and Rerun the query corrector until the query is detailed enough
'''

user_session_uuid = str(uuid.uuid4())
query = os.getenv("QUERY")

api_url = os.getenv("API_URL")
stage_1_uri = f"{api_url}/plan_stage_1"

os_apps = app_list(user_session_uuid)

stage_1_data = {'uuid': user_session_uuid, "query": query, "os_apps": os_apps, "os": "windows"}

response = requests.post(stage_1_uri, json=stage_1_data, stream=True)

running_chunk = ""
response_messages = []

try:
    for chunk in response.iter_content(chunk_size=None):
        if chunk:
            text = chunk.decode('utf-8')
            objects = text.split("\n")
            for obj in objects:
                running_chunk += obj
                try:
                    data = json.loads(running_chunk)
                    if 'success' in data:
                        if data['action'] == "processing":
                            response_messages.append(data['success'])
                    elif 'error' in data:
                        print(data['error'])
                        response_messages.append(data['error'])
                    running_chunk = ""
                except json.JSONDecodeError:
                    pass

except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")
    response_messages.append(f"An error occurred: {e}")

print("Response messages:")
for message in response_messages:
    print(" - ", message)

if "selected_app_list" in message:
    print("Selected app list:", message["selected_app_list"])
    # Launch the selected app
    for app in message["selected_app_list"]:
        print("Launching app:", app)
        launch_app(user_session_uuid, app)

