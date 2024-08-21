import json
import re

from utils.trace import store_agent_conversation_array
from utils.prompt import prompt_loader
from utils.model import model_loader
from utils.response import xmlResponseToDict

def multiline_string_handler(obj):
    """
    Handle multiline strings in a dictionary by replacing '\\n' with actual newlines.
    
    Args:
        obj (dict): A dictionary potentially containing multiline string values.
    
    Returns:
        dict: The input dictionary with multiline strings properly formatted.
    """
    for key, value in obj.items():
        if isinstance(value, str) and '\n' in value:
            obj[key] = re.sub(r'\\n', '\n', value)
    return obj

def execute_agent(userid, sessionid, agent_name, system_prompt_params, fewshot_params, provider, model, image_base64=None):
    """
    Execute an AI agent using the specified provider and model.
    
    Args:
        userid (str): The user's identifier.
        sessionid (str): The current session identifier.
        agent_name (str): The name of the agent to execute.
        system_prompt_params (dict): Parameters for the system prompt.
        fewshot_params (dict): Parameters for few-shot learning examples.
        provider (str): The AI provider to use (e.g., "anthropic" or "openai").
        model (str): The specific model to use from the provider.
        image_base64 (str, optional): Base64 encoded image data, if applicable.
    
    Returns:
        dict: The response from the AI model, parsed from XML to a dictionary.
    """
    # Load prompt templates for the specified agent
    prompt_templates = prompt_loader(agent_name)
    
    # Format the system prompt with provided parameters
    system_prompt = prompt_templates['system_prompt'].format(**system_prompt_params)
    
    # Prepare the message array with few-shot examples
    message_array = prompt_templates['fewshot_messages']
    message_array[-1]['content'] = message_array[-1]['content'].format(**fewshot_params)

    # Get the response from the AI model
    response_content = model_loader(provider, model, system_prompt, message_array, userid, sessionid, image_base64=image_base64)

    # Append the AI's response to the message array
    message_array.append(
        {
            "role": "assistant",
            "content": response_content
        }
    )
    
    # Store the conversation for logging or future reference
    store_agent_conversation_array(
      userid=userid,
      sessionid=sessionid,
      agent_name=agent_name,
      conversation_array=message_array
    )

    # Parse the XML response to a dictionary and return it
    response_dict = xmlResponseToDict(response_content)
    return response_dict

# This file contains the core logic for executing AI agents in the Auto UI Assist application.
# It handles loading prompts, formatting messages, calling AI models, and processing responses.
# The execute_agent function is the main entry point for running different AI tasks within the application.
