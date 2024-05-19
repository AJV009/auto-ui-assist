import os
import re

def prompt_loader(agent_name):
    file_name = f"prompt_lib/{agent_name}.txt"
    
    if not os.path.exists(file_name):
        return None
    
    with open(file_name, 'r') as file:
        content = file.read()
    content = re.sub(r'\n', '\\n', content)
    
    prompt_template = {
        'system_prompt': '',
        'fewshot_messages': []
    }
    
    system_prompt_pattern = r'\[\[prompt_template-system_prompt\]\](.*?)\[\[prompt_template-system_prompt\]\]'
    system_prompt_match = re.search(system_prompt_pattern, content, re.DOTALL)
    
    if system_prompt_match:
        prompt_template['system_prompt'] = system_prompt_match.group(1).replace('\\"', '"').strip()
    
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
