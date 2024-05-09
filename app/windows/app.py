'''
all windows helpders will be here
'''
import requests
from utils.apps import app_list
import os
from dotenv import load_dotenv
import uuid

load_dotenv()

user_session_uuid = str(uuid.uuid4())
query = os.getenv("QUERY")

api_url = os.getenv("API_URL")
stage_1_uri = f"{api_url}/plan_stage_1"

os_apps = app_list(user_session_uuid)

stage_1_data = {'uuid': user_session_uuid, "query": query, "os_apps": os_apps, "os": "windows"}

response = requests.post(stage_1_uri, json=stage_1_data, stream=True)

for chunk in response.iter_content(chunk_size=None):
    if chunk:
        message = chunk.decode('utf-8').strip()
        print(message)
