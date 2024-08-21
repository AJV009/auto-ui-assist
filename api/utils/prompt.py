import os
import re

def prompt_loader(agent_name):
    """
    Load and parse prompt templates for a given agent.

    Args:
        agent_name (str): The name of the agent to load prompts for.

    Returns:
        dict: A dictionary containing the system prompt and few-shot messages,
              or None if the prompt file doesn't exist.

    The function reads a text file from the 'prompt_lib' directory and parses its content
    to extract the system prompt and few-shot examples for the specified agent.
    """
    file_name = f"prompt_lib/{agent_name}.txt"
    
    if not os.path.exists(file_name):
        return None
    
    with open(file_name, 'r') as file:
        content = file.read()
    # Replace newlines with escaped newlines for proper parsing
    content = re.sub(r'\n', '\\n', content)
    
    prompt_template = {
        'system_prompt': '',
        'fewshot_messages': []
    }
    
    # Extract system prompt
    system_prompt_pattern = r'\[\[prompt_template-system_prompt\]\](.*?)\[\[prompt_template-system_prompt\]\]'
    system_prompt_match = re.search(system_prompt_pattern, content, re.DOTALL)
    
    if system_prompt_match:
        prompt_template['system_prompt'] = system_prompt_match.group(1).replace('\\"', '"').strip()
    
    # Extract few-shot examples
    fewshot_pattern = r'\[\[prompt_template-fewshot\]\](.*?)\[\[prompt_template-fewshot\]\]'
    fewshot_match = re.search(fewshot_pattern, content, re.DOTALL)

    if fewshot_match:
        fewshot_content = fewshot_match.group(1).strip()
        fewshot_messages = re.split(r'\[\[prompt_template-fewshot-(?:user|assistant)\]\]', fewshot_content)
        
        current_role = None
        for message in fewshot_messages:
            message = message.replace('\\"', '"').strip()
            if message:
                if current_role is None:
                    current_role = 'user'
                else:
                    current_role = 'assistant' if current_role == 'user' else 'user'
                prompt_template['fewshot_messages'].append({'role': current_role, 'content': message})
    
    return prompt_template

# This utility file handles loading and parsing prompt templates for different agents.
# It reads a specially formatted text file and extracts the system prompt and few-shot examples.
# The extracted data is returned in a structured format for use in the main application.
