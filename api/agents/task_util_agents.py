import json

from utils.trace import store_agent_conversation_array
from utils.prompt import prompt_loader
from utils.model import model_loader

def execute_agent(userid, sessionid, agent_name, system_prompt_params, fewshot_params, provider, model):
    """
    Execute an agent using the specified provider and model.
    """

    prompt_templates = prompt_loader(agent_name)
    system_prompt = prompt_templates['system_prompt'].format(**system_prompt_params)
    message_array = prompt_templates['fewshot_messages']
    message_array[-1]['content'] = message_array[-1]['content'].format(**fewshot_params)

    response_content = model_loader(provider, model, system_prompt, message_array, userid, sessionid)

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

    response_dict = json.loads(response_content)
    return response_dict