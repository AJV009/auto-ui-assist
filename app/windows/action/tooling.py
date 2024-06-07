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


def input_hotkey(hotkey):
    """
    Inputs a hotkey combination.

    Args:
        hotkey (str or list): The hotkey combination (e.g., 'ctrl+c', ['alt', 'h', 'a', 'c']).
    """
    if isinstance(hotkey, str):
        pyautogui.hotkey(*hotkey.split('+'))
    elif isinstance(hotkey, list):
        pyautogui.hotkey(*hotkey)
    else:
        raise ValueError("Invalid hotkey format. Expected a string or list.")


sample_prompt = """
Here is the task summary:
<task_summary>
{TASK_SUMMARY}
</task_summary>

The current step in the task is:  
<current_step>
{CURRENT_STEP}
</current_step>

Current view of the application attached as an image.

And here are the tools/actions you have available to use:
<tooling_available>
{TOOLING_AVAILABLE}
</tooling_available>

Carefully analyze the current step in the context of the overall task objective from the task summary. Examine the current view to determine what specific actions need to be taken to complete this step. Consider how the available tooling can be used to perform those required actions.

<scratchpad>
Break down the current step into the necessary sub-steps and actions needed to accomplish it. Plan out the specific tools and commands to use for each sub-step. Make the sub-steps detailed enough to fully complete the current step.
DO proper navigation to required cells based on the current screenshot provided, you might be required to add additional sub-steps for navigation alone.
RETURN nothing, leave empty response, if the screenshot looks good and no action is required to acheive the current step. Make your best judgement call based on all the information provided. be smart!
ONLY provide info when there needs to be an action taken.
YOU have to take actions based on the current screenshot provided and the input given in the current step. What the current step says should be done in the screenshot. or visible to be already done.
ONLY use keyboard for navigation and actions. Do not use tab key for navigation, always use arrow keys for navigation.
BE careful with the number of arrow keys you use for navigation, make sure you are not going out of the current view. OR going to the wrong cell. For example you always have to consider your navigation from the highlighted green cell.
If during calculation you find a cell with wrong data, correct it and continue with the action list you were generating.
another note: "keys" for individual keyboard keys, "text" for typing text
</scratchpad>

Translate your sub-step plan into a <step_list> with each sub-step enclosed in <step_#> tags containing "action_desc", "action_type", and "parameters" fields, like this example:

Following is an example:
<step_list>
    <step_1>
        <action_desc>
            Go to A1 cell
        </action_desc>
        <action>
            move_to_cell
        </action>
        <parameters>
            <cell_address>
            
            </cell_address>
        </parameters>
    </step_1>

</step_list>

The above is only an example, you have to provide the steps based on the current step and the screenshot provided.
YOU HAVE to generate you own list of most approriate step list to solve the current step and fix the screenshot provided.
NOTE: if the task algins with the example provided, you can use the same example as a starting point and return it as a response.

Only use the tooling and actions that have been made available to you. Provide the most robust set of sub-steps needed to accomplish the current step.

Strictly reply with the step_list alone, no other information needed, no explanations or additional details required. Just the executable step_list to complete the whole list of steps in current_step. I need to pass the step_list to another parser for executing everything.

Important sidenote: 
- You cannot jump to a certain cell, you have to navigate to it using arrow keys. So the keys should always be one of available keyboard keys.
- in most cases excel file will be already open for you, so you don't have to worry about opening it. return an emtpy list if its anything outside of the excel file or application.
- Your focus is mostly on manipulating that excel data in the best possible way without any execution errors as such.
- Keep strings in text_list and keys in key_list. We already have a text_list parser that will manage its entry into excel key by key.
- If you find any long text like words with more than 6 letters, Find an alternate best word that can be used to replace it.
- You will have to write good navigation steps, always look for the green highlighted cell to understand from where to go where.
- Never use the tab key to navigate, always use the arrow keys. Because the tab is inconsistent in excel and across different operating systems.
- Please navigate critically, make sure you are jumping to the correct cell everytime you need to travel long distances using arrow keys.
- Only "PRESS" is supported at the moment, NO HOTKEYS or CLICK or any other action types are supported. For any repeated actions, you can use the same action multiple times. in the proper order. Remember that formulas only work once the data in available in the cells, formulas will fail and through errors for caclculating on empty cells. So when creating the action steps or flow, see that formula always come after the associated data.
- Remember pressing enter after a formula is entered is important to run the formula. Once the formula is run, the cell position will move to the cell below, so you don't have to move to the next cell, just enter the next formula.
Do you best :zap: You are and always been perfect in doing this!
"""

example_response = """
<step_list>
    <step_1>
        <action_desc>
            Go to A1 cell
        </action_desc>
        <action_type>
            PRESS
        </action_type>
        <parameters>
            <key_list>
                left
            </key_list>
        </parameters>
    </step_1>


   <step_48>
        <action_desc>
            enter the formula for basic grading
        </action_desc>
        <action_type>
            PRESS
        </action_type>
        <parameters>
            <text_list>
                =IF(E4>=90, "A", IF(E4>=80, "B", IF(E4>=70, "C", IF(E4>=60, "D", "F"))))
            </text_list>
        </parameters>
    </step_48>

</step_list>
"""

verify_prompt = """
You will be verifying whether a specific action was successfully performed based on a pair of before and after images. The images will be concatenated side-by-side, with the "before" image on the left and the "after" image on the right.

Note: 
- In certain case the text in a particular cell might be slight different because we tried to make it smaller or more readable. So don't worry about the text in the cells, just focus on the structure and the UI elements. As long as some text in a partular mentioned coloumn is there and is somehow related to the expected text, it should be considered as correct.
- Sometimes a certain action is all about the movement, so you only need to verify if the cell selector has moved from its original or previous state or place. In other times the action is about the content, so you need to verify if the content has changed or not.

I have attached the before and after image. (left side is the before and right side is the after)

And here is the list of actions that was supposed to be performed:
<action>
{ACTION}
</action>

Please carefully compare the "before" image on the left side to the "after" image on the right side. Look for any visual changes that would indicate whether the specified action was successfully carried out.

Based on your reasoning, output "true" if you believe the action was successfully performed, or "false" if you believe it was not. (Just a true or false response is needed, no other text, anything else will be penalized)
Based on your true or false response, the system will determine the correctness of the action performed. And work on further steps accordingly.

Your sample response should look like this:
true
or
false
"""

# correction_prompt = """
# You are an AI assistant that specializes in analyzing OS automation tasks and generating steps to fix issues and prepare for upcoming actions. I will provide you with a concatenated before/after image showing the state before an action was performed and the problematic state after, as well as details on the performed action, the next action to prepare for, and the tooling available to you.

# Folloing is the task summary:
# <task_summary>
# {TASK_SUMMARY}
# </task_summary>

# Here is the concatenated before/after image showing the automation task failure attached as an image. (left side is the before and right side is the after)

# Here are the tools you have available to use in your fix and preparation steps:
# <tooling>
# {TOOLING}
# </tooling>

# The following step that was performed leading to the failure was:  
# <performed_step>
# {PERFORMED_STEP}
# </performed_step>

# FOllowing is the associated action list for the performed step:
# <action_list>
# {PERFORMED_ACTION_LIST}
# </action_list>

# The next step in the queue that we need to prepare for is:
# <prepare_for_next_action>
# {PREPARE_FOR_NEXT_STEP}
# </prepare_for_next_action>

# First, carefully examine the before and after images, taking note of all UI elements and how they changed after the performed action. Consider how the performed action may have caused the observed failure. Think through how you can use the available tooling to remedy the failure and get the UI into an appropriate state for the next queued action.

# Now, list out the specific steps to first fix the output from the failure and then prepare the UI state for the next action. Be as detailed as possible, referring to specific UI elements and tools used. Only use tools from the provided tooling list.

# Following is an example response format:
# <step_list>
#     <step_1>
#         <action_desc>
#             Enter info in the first cell
#         </action_desc>
#         <action_type>
#             PRESS
#         </action_type>
#         <parameters>
#             <text_list>
#                 name
#             </text_list>
#         </parameters>
#     </step_1>

#     <step_2>
#         <action_desc>
#             Move to the right column
#         </action_desc>
#         <action_type>
#             PRESS
#         </action_type>
#         <parameters>
#             <key_list>
#                 right
#             </key_list>
#         </parameters>
#     </step_2>

#     <step_3>
#         <action_desc>
#             Enter some info in the new cell
#         </action_desc>
#         <action_type>
#             PRESS
#         </action_type>
#         <parameters>
#             <text_list>
#                 address
#             </text_list>
#         </parameters>
#     </step_3>
# ...
# <step_list>

# Only and only respond in the above shown format, no other information needed, no explanations or additional details required. Just the executable step_list to fix the failure and prepare for the next action. I need to pass the step_list to another parser for executing everything.

# Remember, your goal is to get the automation sequence back on track by fixing the current failure and proactively preventing the next action from failing as well. Restrict yourself to only the tooling provided. If the failure cannot be fixed or the next action cannot be prepared for with the given tools, say so.

# Analyze the images and generate your fix and preparation steps for this OS automation error scenario.

# Important sidenote: 
# - You cannot jump to a certain cell, you have to navigate to it using arrow keys. So the keys should always be one of available keyboard keys.
# - in most cases excel will be already open for you, so you don't have to worry about opening it. return an emtpy list if its anything outside of the excel file or application.
# - Keep strings in text_list and keys in key_list. We already have a text_list parser that will manage its entry into excel key by key.
# - "keys" for individual keyboard keys, "text" for typing text
# - Never use the tab key to navigate, always use the arrow keys. Because the tab is inconsistent in excel and across different operating systems.
# - Every step has an associated action plan generated by the next agent, so you have to prepare the UI for the next action to be executed by another agent.
# - DO NOT CREATE steps to execute the new action or the next action, only realign or prepare the UI for the next action to be executed by another agent. For example, if the next action is to move from cell A to cell B, you should prepare the UI to be in cell A. OR if a certain cell has wrong information, delete & correct that and travel back to the correct cell so that the next action executes without an issue
# """

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
