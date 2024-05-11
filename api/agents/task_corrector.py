import os
import json

from dotenv import load_dotenv
import anthropic

from utils.trace import store_agent_conversation_array
from utils.prompt import prompt_loader

load_dotenv()
anthropic_client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
CLAUDE_HAIKU=os.getenv("ANTHROPIC_CLAUDE_HAIKU")
CLAUDE_SONNET=os.getenv("ANTHROPIC_CLAUDE_SONNET")
CLAUDE_OPUS=os.getenv("ANTHROPIC_CLAUDE_OPUS")

def task_corrector_agent(userid, sessionid, task, app_list, os):
    """
    Correct the task using the Anthropics API.
    """

    prompt_templates = prompt_loader("task_corrector")
    system_prompt = prompt_templates['system_prompt'].format(os=os)
    message_array = prompt_templates['fewshot_messages']
    message_array[-1]['content'] = message_array[-1]['content'].format(task=task, app_list=app_list)
      
    # dump to a json file for debugging
    with open("temp/task_corrector_agent.json", "w") as f:
      json.dump(message_array, f, indent=2)

    response_message = anthropic_client.messages.create(
        model=CLAUDE_SONNET,
        system=system_prompt,
        messages=message_array,
        max_tokens=4096,
        metadata={"user_id": userid+"-"+sessionid},
        temperature=0.0
    )

    message_array.append(
        {
            "role": "assistant",
            "content": response_message.content[0].text
        }
    )
    store_agent_conversation_array(
      userid=userid,
      sessionid=sessionid,
      agent_name="task_corrector_agent",
      conversation_array=message_array
    )

    response_dict = json.loads(response_message.content[0].text)
    return response_dict
