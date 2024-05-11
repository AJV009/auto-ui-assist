'''
We will have the following functions:
- user based token tracker and logger
- session based token tracker and logger

Temperorly we will use the following folder structure:
temp/user-<userid> to store common artifacts
temp/user-<userid>/session-<sessionid> to store session artifacts
'''
import os
import json

def agent_log(userid, sessionid, agent_name, model, conversation_array, response_array):
    pass

def fetch_agent_conversation_array(userid, sessionid, agent_name):
    agent_conversation_array = f'temp/user-{userid}/session-{sessionid}/agent-{agent_name}-conversation_array.json'
    if os.path.exists(agent_conversation_array):
        return json.load(open(agent_conversation_array)) 
    else:
        return None

def store_agent_conversation_array(userid, sessionid, agent_name, conversation_array):
    root_path = f'temp/user-{userid}/session-{sessionid}'
    os.makedirs(root_path, exist_ok=True)
    agent_conversation_array = f"{root_path}/agent-{agent_name}-conversation_array.json"
    existing_conversation_array = fetch_agent_conversation_array(userid, sessionid, agent_name)
    if existing_conversation_array:
        conversation_array = existing_conversation_array + conversation_array
    with open(agent_conversation_array, 'w') as f:
        json.dump(conversation_array, f)

