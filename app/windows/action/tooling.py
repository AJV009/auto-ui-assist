'''
Must Need Agents:
- Keyboard + Mouse Agent (for general purpose)

Additional LLM based agents:
- Search Info (google search tool)
- Launch App (launch the most suitable app)
- Launch URL (launch or fix URLs automatically and launch), 
- Content Generation (generate content based on the given context / Ask ChatGPT)
- 
'''

import pyautogui

width, height= pyautogui.size()
X_MAX = width
Y_MAX = height

SUPPORTED_KEYBOARD_KEYS = [
    '\\t', '\\n', '\\r', ' ', '!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/',
    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', 
    '^', '_', '`', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 
    'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K',
    'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '{', '|', '}', '~',
    'alt', 'altleft', 'altright', 'backspace', 'capslock', 'ctrl', 'ctrlleft', 'ctrlright', 'decimal', 
    'del', 'delete', 'divide', 'down', 'end', 'enter', 'esc', 'escape', 'f1', 'f10', 'f11', 'f12', 
    'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'help', 'home', 'insert', 'left', 'multiply', 
    'num0', 'num1', 'num2', 'num3', 'num4', 'num5', 'num6', 'num7', 'num8', 'num9', 'numlock', 
    'pagedown', 'pageup', 'pause', 'pgdn', 'pgup', 'printscreen', 'prtsc', 'prtscr', 'return', 
    'right', 'scrolllock', 'shift', 'shiftleft', 'shiftright', 'space', 'tab', 'volumedown', 
    'volumemute', 'volumeup', 'win', 'winleft', 'winright', 'down', 'left', 'right', 'up'
]

import re

def xmlResponseToDict(xml_response):
    def parse_tag(tag_content):
        if not tag_content:
            return None
        
        tag_pattern = re.compile(r'<(\w+)>(.*?)</\1>', re.DOTALL)
        tag_match = tag_pattern.match(tag_content)
        
        if tag_match:
            tag_name = tag_match.group(1)
            tag_value = tag_match.group(2).strip()
            
            if tag_name.endswith('_list'):
                items = re.findall(r'<(\w+)>(.*?)</\1>', tag_value, re.DOTALL)
                
                if items:
                    parsed_items = []
                    for item_name, item_content in items:
                        parsed_item = parse_tag(f'<{item_name}>{item_content}</{item_name}>')
                        if parsed_item:
                            parsed_items.append(parsed_item)
                    
                    return {tag_name: parsed_items}
                else:
                    items = re.split(r'\s*\n\s*', tag_value)
                    items = [item.strip() for item in items if item.strip()]
                    return {tag_name: items}
            else:
                # Recursively parse nested tags
                nested_tags = re.findall(r'<(\w+)>(.*?)</\1>', tag_value, re.DOTALL)
                if nested_tags:
                    parsed_nested_tags = {}
                    for nested_tag_name, nested_tag_content in nested_tags:
                        parsed_nested_tag = parse_tag(f'<{nested_tag_name}>{nested_tag_content}</{nested_tag_name}>')
                        if parsed_nested_tag:
                            parsed_nested_tags.update(parsed_nested_tag)
                    return {tag_name: parsed_nested_tags}
                else:
                    return {tag_name: tag_value}
        
        return None

    tags = re.findall(r'<(\w+)>(.*?)</\1>', xml_response, re.DOTALL)
    result = {}
    
    for tag_name, tag_content in tags:
        parsed_tag = parse_tag(f'<{tag_name}>{tag_content}</{tag_name}>')
        if parsed_tag:
            result.update(parsed_tag)
    
    return result
