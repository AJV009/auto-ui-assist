import json
import re

from utils.trace import store_agent_conversation_array
from utils.prompt import prompt_loader
from utils.model import model_loader
from utils.response import xmlResponseToDict

def multiline_string_handler(obj):
    for key, value in obj.items():
        if isinstance(value, str) and '\n' in value:
            obj[key] = re.sub(r'\\n', '\n', value)
    return obj

def execute_agent(userid, sessionid, agent_name, system_prompt_params, fewshot_params, provider, model, image_base64=None):
    """
    Execute an agent using the specified provider and model.
    """

    prompt_templates = prompt_loader(agent_name)
    system_prompt = prompt_templates['system_prompt'].format(**system_prompt_params)
    message_array = prompt_templates['fewshot_messages']
    message_array[-1]['content'] = message_array[-1]['content'].format(**fewshot_params)

    response_content = model_loader(provider, model, system_prompt, message_array, userid, sessionid, image_base64=image_base64)

    message_array.append(
        {
            "role": "assistant",
            "content": response_content
        }
    )
    store_agent_conversation_array(
      userid=userid,
      sessionid=sessionid,
      agent_name=agent_name,
      conversation_array=message_array
    )

    response_dict = xmlResponseToDict(response_content)
    return response_dict
