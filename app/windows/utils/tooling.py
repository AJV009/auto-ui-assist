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

keyboard_mouse = """
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

# Keyboard shortcuts in Excel

# Rules:
Use keyboard arrow keys to navigate through the cells.
For example, to move one cell up, press the Up arrow key.
To move ten cell down, press the Down arrow key 10 times.
Navigate the space efficiently by using the keyboard shortcuts.

# Frequently used shortcuts
frequently_used_shortcuts = {
    "Ctrl+W": "Close a workbook.",
    "Ctrl+O": "Open a workbook.",
    "Alt+H": "Go to the Home tab.",
    "Ctrl+S": "Save a workbook.",
    "Ctrl+C": "Copy selection.",
    "Ctrl+V": "Paste selection.",
    "Ctrl+Z": "Undo recent action.",
    "Delete": "Remove cell contents.",
    "Alt+H, H": "Choose a fill color.",
    "Ctrl+X": "Cut selection.",
    "Alt+N": "Go to the Insert tab.",
    "Ctrl+B": "Apply bold formatting.",
    "Alt+H, A, C": "Center align cell contents.",
    "Alt+P": "Go to the Page Layout tab.",
    "Alt+A": "Go to the Data tab.",
    "Alt+W": "Go to the View tab.",
    "Shift+F10": "Open the context menu.",
    "Alt+H, B": "Add borders.",
    "Alt+H, D, C": "Delete column.",
    "Alt+M": "Go to the Formula tab.",
    "Ctrl+9": "Hide the selected rows.",
    "Ctrl+0": "Hide the selected columns."
}

# Ribbon keyboard shortcuts
ribbon_keyboard_shortcuts = {
    "Alt+H": "Open the Home tab.",
    "Alt+Q": "Move to the Tell me or Search field.",
    "Alt+F": "Open the File menu.",
    "Alt+N": "Open the Insert tab.",
    "Alt+P": "Open the Page Layout tab.",
    "Alt+M": "Open the Formulas tab.",
    "Alt+A": "Open the Data tab.",
    "Alt+R": "Open the Review tab.",
    "Alt+W": "Open the View tab."
}

# Keyboard shortcuts for navigating in cells
navigation_shortcuts = {
    "Shift+Tab": "Move to the previous cell in a worksheet.",
    "Up arrow key": "Move one cell up in a worksheet.",
    "Down arrow key": "Move one cell down in a worksheet.",
    "Left arrow key": "Move one cell left in a worksheet.",
    "Right arrow key": "Move one cell right in a worksheet.",
    "Ctrl+Arrow key": "Move to the edge of the current data region.",
    "End, Arrow key": "Enter the End mode, move to the next nonblank cell.",
    "Ctrl+End": "Move to the last cell on a worksheet.",
    "Ctrl+Shift+End": "Extend the selection of cells to the last used cell.",
    "Home+Scroll lock": "Move to the cell in the upper-left corner with Scroll lock.",
    "Ctrl+Home": "Move to the beginning of a worksheet.",
    "Page down": "Move one screen down in a worksheet.",
    "Ctrl+Page down": "Move to the next sheet in a workbook.",
    "Alt+Page down": "Move one screen to the right in a worksheet.",
    "Page up": "Move one screen up in a worksheet.",
    "Alt+Page up": "Move one screen to the left in a worksheet.",
    "Ctrl+Page up": "Move to the previous sheet in a workbook.",
    "Tab key": "Move one cell to the right in a worksheet."
}

# Keyboard shortcuts for formatting cells
formatting_shortcuts = {
    "Ctrl+1": "Open the Format Cells dialog box.",
    "Ctrl+Shift+F": "Format fonts in the Format Cells dialog box.",
    "F2": "Edit the active cell.",
    "Shift+F2": "Insert a note.",
    "Ctrl+Shift+Plus sign (+)": "Open the Insert dialog box.",
    "Ctrl+Minus sign (-)": "Open the Delete dialog box.",
    "Ctrl+Shift+Colon (:)": "Enter the current time.",
    "Ctrl+Semicolon (;)": "Enter the current date.",
    "Ctrl+Grave accent (`)": "Switch between displaying cell values or formulas.",
    "Ctrl+Apostrophe (')": "Copy a formula from the cell above.",
    "Ctrl+X": "Move the selected cells.",
    "Ctrl+C": "Copy the selected cells.",
    "Ctrl+V": "Paste content at the insertion point.",
    "Ctrl+Alt+V": "Open the Paste Special dialog box.",
    "Ctrl+I": "Italicize text or remove italic formatting.",
    "Ctrl+B": "Bold text or remove bold formatting.",
    "Ctrl+U": "Underline text or remove underline.",
    "Ctrl+5": "Apply or remove strikethrough formatting.",
    "Ctrl+6": "Switch between hiding objects and displaying placeholders.",
    "Ctrl+Shift+Ampersand sign (&)": "Apply an outline border.",
    "Ctrl+Shift+Underscore (_)": "Remove the outline border.",
    "Ctrl+8": "Display or hide the outline symbols.",
    "Ctrl+D": "Use the Fill Down command.",
    "Ctrl+Shift+Tilde sign (~)": "Apply the General number format.",
    "Ctrl+Shift+Dollar sign ($)": "Apply the Currency format.",
    "Ctrl+Shift+Percent sign (%)": "Apply the Percentage format.",
    "Ctrl+Shift+Caret sign (^)": "Apply the Scientific number format.",
    "Ctrl+Shift+Number sign (#)": "Apply the Date format.",
    "Ctrl+Shift+At sign (@)": "Apply the Time format.",
    "Ctrl+Shift+Exclamation point (!)": "Apply the Number format.",
    "Ctrl+K": "Open the Insert hyperlink dialog box.",
    "F7": "Check spelling.",
    "Ctrl+Q": "Display the Quick Analysis options.",
    "Ctrl+L": "Display the Create Table dialog box.",
    "Ctrl+Shift+G": "Open the Workbook Statistics dialog box."
}

# Keyboard shortcuts for making selections and performing actions
selections_and_actions_shortcuts = {
    "Ctrl+A": "Select the entire worksheet.",
    "Ctrl+Shift+Page down": "Select the current and next sheet in a workbook.",
    "Ctrl+Shift+Page up": "Select the current and previous sheet in a workbook.",
    "Shift+Arrow key": "Extend the selection of cells by one cell.",
    "Ctrl+Shift+Arrow key": "Extend the selection of cells to the last nonblank cell.",
    "F8": "Turn extend mode on and use the arrow keys to extend a selection.",
    "Shift+F8": "Add a non-adjacent cell or range to a selection.",
    "Alt+Enter": "Start a new line in the same cell.",
    "Ctrl+Enter": "Fill the selected cell range with the current entry.",
    "Shift+Enter": "Complete a cell entry and select the cell above.",
    "Ctrl+Spacebar": "Select an entire column.",
    "Shift+Spacebar": "Select an entire row.",
    "Ctrl+Shift+Spacebar": "Select all objects on a worksheet.",
    "Ctrl+Shift+Home": "Extend the selection of cells to the beginning of the worksheet.",
    "Ctrl+Shift+Asterisk sign (*)": "Select the current region around the active cell.",
    "Home": "Select the first command on the menu.",
    "Ctrl+Y": "Repeat the last command or action.",
    "Ctrl+Z": "Undo the last action.",
    "Shift+Scroll down": "Expand grouped rows or columns.",
    "Shift+Scroll up": "Collapse grouped rows or columns."
}

# Keyboard shortcuts for working with data, functions, and the formula bar
data_functions_shortcuts = {
    "Ctrl+Alt+P": "Turn on or off tooltips for checking formulas.",
    "F2": "Edit the active cell.",
    "Ctrl+Shift+U": "Expand or collapse the formula bar.",
    "Esc": "Cancel an entry in the cell or formula bar.",
    "Enter": "Complete an entry in the formula bar and select the cell below.",
    "Ctrl+End": "Move the cursor to the end of the text in the formula bar.",
    "Ctrl+Shift+End": "Select all text in the formula bar from the cursor to the end.",
    "F9": "Calculate all worksheets.",
    "Shift+F9": "Calculate the active worksheet.",
    "Ctrl+Alt+F9": "Calculate all worksheets regardless of changes.",
    "Ctrl+Alt+Shift+F9": "Check dependent formulas and calculate all cells.",
    "Alt+Shift+F10": "Display the menu or message for an Error Checking button.",
    "Ctrl+A": "Display the Function Arguments dialog box.",
    "Ctrl+Shift+A": "Insert argument names and parentheses in a formula.",
    "Alt+Equal sign ( = )": "Insert the AutoSum formula.",
    "Ctrl+E": "Invoke Flash Fill.",
    "F4": "Cycle through all combinations of absolute and relative references.",
    "Shift+F3": "Insert a function.",
    "Ctrl+Shift+Straight quotation mark (\"")": "Copy the value from the cell above.",
    "Alt+F1": "Create an embedded chart.",
    "F11": "Create a chart in a separate Chart sheet.",
    "Alt+M, M, D": "Define a name to use in references.",
    "F3": "Paste a name from the Paste Name dialog box.",
    "Enter": "Calculate an array formula."
}

# Keyboard shortcuts for working with objects
objects_shortcuts = {
    "Ctrl+click": "Select an object that is under other objects.",
    "Shift+Tab": "Select the previous object.",
    "Tab key": "Select the next object.",
    "Ctrl+Shift+G": "Open the Group dialog box.",
    "Ctrl+Shift+H": "Open the Hyperlink dialog box.",
    "Ctrl+Shift+J": "Open the Justify dialog box.",
    "Ctrl+Shift+L": "Toggle Autofilter on and off.",
    "Ctrl+Shift+M": "Open the Insert Function dialog box.",
    "Ctrl+Shift+N": "Open the Name Manager dialog box.",
    "Ctrl+Shift+O": "Select all cells with comments.",
    "Ctrl+Shift+P": "Open the Print dialog box.",
    "Ctrl+Shift+Q": "Open the Sort dialog box.",
    "Ctrl+Shift+R": "Open the Remove Duplicates dialog box.",
    "Ctrl+Shift+S": "Open the Styles dialog box.",
    "Ctrl+Shift+T": "Open the Themes dialog box.",
    "Ctrl+Shift+U": "Expand or collapse the formula bar.",
    "Ctrl+Shift+V": "Open the Paste Special dialog box.",
    "Ctrl+Shift+W": "Open the Workbook Statistics dialog box.",
    "Ctrl+Shift+X": "Open the Delete dialog box.",
    "Ctrl+Shift+Y": "Repeat the last action.",
    "Ctrl+Shift+Z": "Undo the last action.",
    "Alt+Shift+Ctrl+F9": "Check dependent formulas and calculate all cells."
}

# To run a shortcut, use the following commands:

ACTION_SPACE = [
    {
        "action_type": "PRESS",
        "note": "press the specified key and release it",
        "parameters": {
            "key": {
                "type": str,
                "range": KEYBOARD_KEYS,
                "optional": False,
            }
        }
    },
    {
        "action_type": "KEY_DOWN",
        "note": "press the specified key",
        "parameters": {
            "key": {
                "type": str,
                "range": KEYBOARD_KEYS,
                "optional": False,
            }
        }
    },
    {
        "action_type": "KEY_UP",
        "note": "release the specified key",
        "parameters": {
            "key": {
                "type": str,
                "range": KEYBOARD_KEYS,
                "optional": False,
            }
        }
    },
    {
        "action_type": "HOTKEY",
        "note": "press the specified key combination",
        "parameters": {
            "keys": {
                "type": list,
                "range": [KEYBOARD_KEYS],
                "optional": False,
                # example: ["ctrl", "c"] for copy
            }
        }
    }
]

"""

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
        <action_type>
            PRESS
        </action_type>
        <parameters>
            <key_list>
                left
            </key_list>
        </parameters>
    </step_1>

    <step_2>
        <action_desc>
            Enter first column name - name
        </action_desc>
        <action_type>
            PRESS
        </action_type>
        <parameters>
            <text_list>
                name
            </text_list>
        </parameters>
    </step_2>

    <step_3>
        <action_desc>
            move to B1 cell
        </action_desc>
        <action_type>
            PRESS
        </action_type>
        <parameters>
            <key_list>
                right
            </key_list>
        </parameters>
    </step_3>

   <step_4>
        <action_desc>
            Enter the first subject - SCI column name
        </action_desc>
        <action_type>
            PRESS
        </action_type>
        <parameters>
            <text_list>
                sci
            </text_list>
        </parameters>
    </step_4>

    <step_5>
        <action_desc>
            move to C1 cell
        </action_desc>
        <action_type>
            PRESS
        </action_type>
        <parameters>
            <key_list>
                right
            </key_list>
        </parameters>
    </step_5>

   <step_6>
        <action_desc>
            Enter the second subject - Math column name
        </action_desc>
        <action_type>
            PRESS
        </action_type>
        <parameters>
            <text_list>
                math
            </text_list>
        </parameters>
    </step_6>

    <step_7>
        <action_desc>
            move to D1 cell
        </action_desc>
        <action_type>
            PRESS
        </action_type>
        <parameters>
            <key_list>
                right
            </key_list>
        </parameters>
    </step_7>

   <step_8>
        <action_desc>
            Enter the third subject - ENG column name
        </action_desc>
        <action_type>
            PRESS
        </action_type>
        <parameters>
            <text_list>
                ENG
            </text_list>
        </parameters>
    </step_8>

    <step_9>
        <action_desc>
            move to E1 cell
        </action_desc>
        <action_type>
            PRESS
        </action_type>
        <parameters>
            <key_list>
                right
            </key_list>
        </parameters>
    </step_9>

   <step_10>
        <action_desc>
            Enter the avg column name
        </action_desc>
        <action_type>
            PRESS
        </action_type>
        <parameters>
            <text_list>
                AVG
            </text_list>
        </parameters>
    </step_10>

    <step_11>
        <action_desc>
            move to F1 cell
        </action_desc>
        <action_type>
            PRESS
        </action_type>
        <parameters>
            <key_list>
                right
            </key_list>
        </parameters>
    </step_11>

   <step_12>
        <action_desc>
            Enter the grade column name
        </action_desc>
        <action_type>
            PRESS
        </action_type>
        <parameters>
            <text_list>
                grade
            </text_list>
        </parameters>
    </step_12>

    <step_13>
        <action_desc>
            move from F1 to A2 cell
        </action_desc>
        <action_type>
            PRESS
        </action_type>
        <parameters>
            <key_list>
                down
                left
                left
                left
                left
                left
            </key_list>
        </parameters>
    </step_13>

   <step_14>
        <action_desc>
            Enter the first student name
        </action_desc>
        <action_type>
            PRESS
        </action_type>
        <parameters>
            <text_list>
                john
            </text_list>
        </parameters>
    </step_14>

    <step_15>
        <action_desc>
            move to A3 cell
        </action_desc>
        <action_type>
            PRESS
        </action_type>
        <parameters>
            <key_list>
                down
            </key_list>
        </parameters>
    </step_15>

   <step_16>
        <action_desc>
            Enter the second student name
        </action_desc>
        <action_type>
            PRESS
        </action_type>
        <parameters>
            <text_list>
                mark
            </text_list>
        </parameters>
    </step_16>

    <step_17>
        <action_desc>
            move to A4 cell
        </action_desc>
        <action_type>
            PRESS
        </action_type>
        <parameters>
            <key_list>
                down
            </key_list>
        </parameters>
    </step_17>

   <step_18>
        <action_desc>
            Enter the second student name
        </action_desc>
        <action_type>
            PRESS
        </action_type>
        <parameters>
            <text_list>
                sam
            </text_list>
        </parameters>
    </step_18>

    <step_19>
        <action_desc>
            move from A4 to B2 cell
        </action_desc>
        <action_type>
            PRESS
        </action_type>
        <parameters>
            <key_list>
                right
                up
                up
            </key_list>
        </parameters>
    </step_19>

   <step_20>
        <action_desc>
            Enter a random number between 0-100
        </action_desc>
        <action_type>
            PRESS
        </action_type>
        <parameters>
            <text_list>
                90
            </text_list>
        </parameters>
    </step_20>

    <step_21>
        <action_desc>
            move to C2 cell
        </action_desc>
        <action_type>
            PRESS
        </action_type>
        <parameters>
            <key_list>
                right
            </key_list>
        </parameters>
    </step_21>

   <step_22>
        <action_desc>
            Enter a random number between 0-100
        </action_desc>
        <action_type>
            PRESS
        </action_type>
        <parameters>
            <text_list>
                80
            </text_list>
        </parameters>
    </step_22>

    <step_23>
        <action_desc>
            move to D2 cell
        </action_desc>
        <action_type>
            PRESS
        </action_type>
        <parameters>
            <key_list>
                right
            </key_list>
        </parameters>
    </step_23>

   <step_24>
        <action_desc>
            Enter a random number between 0-100
        </action_desc>
        <action_type>
            PRESS
        </action_type>
        <parameters>
            <text_list>
                70
            </text_list>
        </parameters>
    </step_24>

    <step_25>
        <action_desc>
            move from D2 to B3 cell
        </action_desc>
        <action_type>
            PRESS
        </action_type>
        <parameters>
            <key_list>
                down
                left
                left
            </key_list>
        </parameters>
    </step_25>

   <step_26>
        <action_desc>
            Enter a random number between 0-100
        </action_desc>
        <action_type>
            PRESS
        </action_type>
        <parameters>
            <text_list>
                60
            </text_list>
        </parameters>
    </step_26>

    <step_27>
        <action_desc>
            move to C3 cell
        </action_desc>
        <action_type>
            PRESS
        </action_type>
        <parameters>
            <key_list>
                right
            </key_list>
        </parameters>
    </step_27>

   <step_28>
        <action_desc>
            Enter a random number between 0-100
        </action_desc>
        <action_type>
            PRESS
        </action_type>
        <parameters>
            <text_list>
                50
            </text_list>
        </parameters>
    </step_28>

    <step_29>
        <action_desc>
            move to D3 cell
        </action_desc>
        <action_type>
            PRESS
        </action_type>
        <parameters>
            <key_list>
                right
            </key_list>
        </parameters>
    </step_29>

   <step_30>
        <action_desc>
            Enter a random number between 0-100
        </action_desc>
        <action_type>
            PRESS
        </action_type>
        <parameters>
            <text_list>
                40
            </text_list>
        </parameters>
    </step_30>

    <step_31>
        <action_desc>
            move from D3 to B4 cell
        </action_desc>
        <action_type>
            PRESS
        </action_type>
        <parameters>
            <key_list>
                down
                left
                left
            </key_list>
        </parameters>
    </step_31>

   <step_32>
        <action_desc>
            Enter a random number between 0-100
        </action_desc>
        <action_type>
            PRESS
        </action_type>
        <parameters>
            <text_list>
                30
            </text_list>
        </parameters>
    </step_32>

    <step_33>
        <action_desc>
            move to C4 cell
        </action_desc>
        <action_type>
            PRESS
        </action_type>
        <parameters>
            <key_list>
                right
            </key_list>
        </parameters>
    </step_33>

   <step_34>
        <action_desc>
            Enter a random number between 0-100
        </action_desc>
        <action_type>
            PRESS
        </action_type>
        <parameters>
            <text_list>
                20
            </text_list>
        </parameters>
    </step_34>

    <step_35>
        <action_desc>
            move to D4 cell
        </action_desc>
        <action_type>
            PRESS
        </action_type>
        <parameters>
            <key_list>
                right
            </key_list>
        </parameters>
    </step_35>

   <step_36>
        <action_desc>
            Enter a random number between 0-100
        </action_desc>
        <action_type>
            PRESS
        </action_type>
        <parameters>
            <text_list>
                10
            </text_list>
        </parameters>
    </step_36>

    <step_37>
        <action_desc>
            move to E2 from D4 cell
        </action_desc>
        <action_type>
            PRESS
        </action_type>
        <parameters>
            <key_list>
                right
                up
                up
            </key_list>
        </parameters>
    </step_37>

   <step_38>
        <action_desc>
            enter the formula for average
        </action_desc>
        <action_type>
            PRESS
        </action_type>
        <parameters>
            <text_list>
                =AVERAGE(B2:D2)
            </text_list>
        </parameters>
    </step_38>

    <step_39>
        <action_desc>
            run the formula
        </action_desc>
        <action_type>
            PRESS
        </action_type>
        <parameters>
            <key_list>
                enter
            </key_list>
        </parameters>
    </step_39>

   <step_40>
        <action_desc>
            enter by default move to the cell below, so no need to move to the next cell, enter the formula for average
        </action_desc>
        <action_type>
            PRESS
        </action_type>
        <parameters>
            <text_list>
                =AVERAGE(B3:D3)
            </text_list>
        </parameters>
    </step_40>

    <step_41>
        <action_desc>
            run the formula
        </action_desc>
        <action_type>
            PRESS
        </action_type>
        <parameters>
            <key_list>
                enter
            </key_list>
        </parameters>
    </step_41>

   <step_42>
        <action_desc>
            enter by default move to the cell below, so no need to move to the next cell, enter the formula for average
        </action_desc>
        <action_type>
            PRESS
        </action_type>
        <parameters>
            <text_list>
                =AVERAGE(B4:D4)
            </text_list>
        </parameters>
    </step_42>

    <step_43>
        <action_desc>
            enter by default move to the cell below, so extra up, move to F2 from E4 cell
        </action_desc>
        <action_type>
            PRESS
        </action_type>
        <parameters>
            <key_list>
                right
                up
                up
                up
            </key_list>
        </parameters>
    </step_43>

   <step_44>
        <action_desc>
            enter the formula for basic grading
        </action_desc>
        <action_type>
            PRESS
        </action_type>
        <parameters>
            <text_list>
                =IFS(E2>=90, "A", E2>=80, "B", E2>=70, "C", E2>=60, "D", TRUE, "F")
            </text_list>
        </parameters>
    </step_44>

    <step_45>
        <action_desc>
            enter to run the formula
        </action_desc>
        <action_type>
            PRESS
        </action_type>
        <parameters>
            <key_list>
                enter
            </key_list>
        </parameters>
    </step_45>

   <step_46>
        <action_desc>
            enter by default move to the cell below, so no need to move to the next cell, enter the formula for basic grading
        </action_desc>
        <action_type>
            PRESS
        </action_type>
        <parameters>
            <text_list>
                =IFS(E3>=90, "A", E3>=80, "B", E3>=70, "C", E3>=60, "D", TRUE, "F")
            </text_list>
        </parameters>
    </step_46>

    <step_47>
        <action_desc>
            enter to run the formula
        </action_desc>
        <action_type>
            PRESS
        </action_type>
        <parameters>
            <key_list>
                enter
            </key_list>
        </parameters>
    </step_47>

   <step_48>
        <action_desc>
            enter by default move to the cell below, so no need to move to the next cell, enter the formula for basic grading
        </action_desc>
        <action_type>
            PRESS
        </action_type>
        <parameters>
            <text_list>
                =IFS(E4>=90, "A", E4>=80, "B", E4>=70, "C", E4>=60, "D", TRUE, "F")
            </text_list>
        </parameters>
    </step_48>

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

    <step_2>
        <action_desc>
            Enter first column name - name
        </action_desc>
        <action_type>
            PRESS
        </action_type>
        <parameters>
            <text_list>
                name
            </text_list>
        </parameters>
    </step_2>

    <step_3>
        <action_desc>
            move to B1 cell
        </action_desc>
        <action_type>
            PRESS
        </action_type>
        <parameters>
            <key_list>
                right
            </key_list>
        </parameters>
    </step_3>

   <step_4>
        <action_desc>
            Enter the first subject - SCI column name
        </action_desc>
        <action_type>
            PRESS
        </action_type>
        <parameters>
            <text_list>
                sci
            </text_list>
        </parameters>
    </step_4>

    <step_5>
        <action_desc>
            move to C1 cell
        </action_desc>
        <action_type>
            PRESS
        </action_type>
        <parameters>
            <key_list>
                right
            </key_list>
        </parameters>
    </step_5>

   <step_6>
        <action_desc>
            Enter the second subject - Math column name
        </action_desc>
        <action_type>
            PRESS
        </action_type>
        <parameters>
            <text_list>
                math
            </text_list>
        </parameters>
    </step_6>

    <step_7>
        <action_desc>
            move to D1 cell
        </action_desc>
        <action_type>
            PRESS
        </action_type>
        <parameters>
            <key_list>
                right
            </key_list>
        </parameters>
    </step_7>

   <step_8>
        <action_desc>
            Enter the third subject - ENG column name
        </action_desc>
        <action_type>
            PRESS
        </action_type>
        <parameters>
            <text_list>
                ENG
            </text_list>
        </parameters>
    </step_8>

    <step_9>
        <action_desc>
            move to E1 cell
        </action_desc>
        <action_type>
            PRESS
        </action_type>
        <parameters>
            <key_list>
                right
            </key_list>
        </parameters>
    </step_9>

   <step_10>
        <action_desc>
            Enter the avg column name
        </action_desc>
        <action_type>
            PRESS
        </action_type>
        <parameters>
            <text_list>
                AVG
            </text_list>
        </parameters>
    </step_10>

    <step_11>
        <action_desc>
            move to F1 cell
        </action_desc>
        <action_type>
            PRESS
        </action_type>
        <parameters>
            <key_list>
                right
            </key_list>
        </parameters>
    </step_11>

   <step_12>
        <action_desc>
            Enter the grade column name
        </action_desc>
        <action_type>
            PRESS
        </action_type>
        <parameters>
            <text_list>
                grade
            </text_list>
        </parameters>
    </step_12>

    <step_13>
        <action_desc>
            move from F1 to A2 cell
        </action_desc>
        <action_type>
            PRESS
        </action_type>
        <parameters>
            <key_list>
                down
                left
                left
                left
                left
                left
            </key_list>
        </parameters>
    </step_13>

   <step_14>
        <action_desc>
            Enter the first student name
        </action_desc>
        <action_type>
            PRESS
        </action_type>
        <parameters>
            <text_list>
                john
            </text_list>
        </parameters>
    </step_14>

    <step_15>
        <action_desc>
            move to A3 cell
        </action_desc>
        <action_type>
            PRESS
        </action_type>
        <parameters>
            <key_list>
                down
            </key_list>
        </parameters>
    </step_15>

   <step_16>
        <action_desc>
            Enter the second student name
        </action_desc>
        <action_type>
            PRESS
        </action_type>
        <parameters>
            <text_list>
                mark
            </text_list>
        </parameters>
    </step_16>

    <step_17>
        <action_desc>
            move to A4 cell
        </action_desc>
        <action_type>
            PRESS
        </action_type>
        <parameters>
            <key_list>
                down
            </key_list>
        </parameters>
    </step_17>

   <step_18>
        <action_desc>
            Enter the second student name
        </action_desc>
        <action_type>
            PRESS
        </action_type>
        <parameters>
            <text_list>
                sam
            </text_list>
        </parameters>
    </step_18>

    <step_19>
        <action_desc>
            move from A4 to B2 cell
        </action_desc>
        <action_type>
            PRESS
        </action_type>
        <parameters>
            <key_list>
                right
                up
                up
            </key_list>
        </parameters>
    </step_19>

   <step_20>
        <action_desc>
            Enter a random number between 0-100
        </action_desc>
        <action_type>
            PRESS
        </action_type>
        <parameters>
            <text_list>
                90
            </text_list>
        </parameters>
    </step_20>

    <step_21>
        <action_desc>
            move to C2 cell
        </action_desc>
        <action_type>
            PRESS
        </action_type>
        <parameters>
            <key_list>
                right
            </key_list>
        </parameters>
    </step_21>

   <step_22>
        <action_desc>
            Enter a random number between 0-100
        </action_desc>
        <action_type>
            PRESS
        </action_type>
        <parameters>
            <text_list>
                80
            </text_list>
        </parameters>
    </step_22>

    <step_23>
        <action_desc>
            move to D2 cell
        </action_desc>
        <action_type>
            PRESS
        </action_type>
        <parameters>
            <key_list>
                right
            </key_list>
        </parameters>
    </step_23>

   <step_24>
        <action_desc>
            Enter a random number between 0-100
        </action_desc>
        <action_type>
            PRESS
        </action_type>
        <parameters>
            <text_list>
                70
            </text_list>
        </parameters>
    </step_24>

    <step_25>
        <action_desc>
            move from D2 to B3 cell
        </action_desc>
        <action_type>
            PRESS
        </action_type>
        <parameters>
            <key_list>
                down
                left
                left
            </key_list>
        </parameters>
    </step_25>

   <step_26>
        <action_desc>
            Enter a random number between 0-100
        </action_desc>
        <action_type>
            PRESS
        </action_type>
        <parameters>
            <text_list>
                60
            </text_list>
        </parameters>
    </step_26>

    <step_27>
        <action_desc>
            move to C3 cell
        </action_desc>
        <action_type>
            PRESS
        </action_type>
        <parameters>
            <key_list>
                right
            </key_list>
        </parameters>
    </step_27>

   <step_28>
        <action_desc>
            Enter a random number between 0-100
        </action_desc>
        <action_type>
            PRESS
        </action_type>
        <parameters>
            <text_list>
                50
            </text_list>
        </parameters>
    </step_28>

    <step_29>
        <action_desc>
            move to D3 cell
        </action_desc>
        <action_type>
            PRESS
        </action_type>
        <parameters>
            <key_list>
                right
            </key_list>
        </parameters>
    </step_29>

   <step_30>
        <action_desc>
            Enter a random number between 0-100
        </action_desc>
        <action_type>
            PRESS
        </action_type>
        <parameters>
            <text_list>
                40
            </text_list>
        </parameters>
    </step_30>

    <step_31>
        <action_desc>
            move from D3 to B4 cell
        </action_desc>
        <action_type>
            PRESS
        </action_type>
        <parameters>
            <key_list>
                down
                left
                left
            </key_list>
        </parameters>
    </step_31>

   <step_32>
        <action_desc>
            Enter a random number between 0-100
        </action_desc>
        <action_type>
            PRESS
        </action_type>
        <parameters>
            <text_list>
                30
            </text_list>
        </parameters>
    </step_32>

    <step_33>
        <action_desc>
            move to C4 cell
        </action_desc>
        <action_type>
            PRESS
        </action_type>
        <parameters>
            <key_list>
                right
            </key_list>
        </parameters>
    </step_33>

   <step_34>
        <action_desc>
            Enter a random number between 0-100
        </action_desc>
        <action_type>
            PRESS
        </action_type>
        <parameters>
            <text_list>
                20
            </text_list>
        </parameters>
    </step_34>

    <step_35>
        <action_desc>
            move to D4 cell
        </action_desc>
        <action_type>
            PRESS
        </action_type>
        <parameters>
            <key_list>
                right
            </key_list>
        </parameters>
    </step_35>

   <step_36>
        <action_desc>
            Enter a random number between 0-100
        </action_desc>
        <action_type>
            PRESS
        </action_type>
        <parameters>
            <text_list>
                10
            </text_list>
        </parameters>
    </step_36>

    <step_37>
        <action_desc>
            move to E2 from D4 cell
        </action_desc>
        <action_type>
            PRESS
        </action_type>
        <parameters>
            <key_list>
                right
                up
                up
            </key_list>
        </parameters>
    </step_37>

   <step_38>
        <action_desc>
            enter the formula for average
        </action_desc>
        <action_type>
            PRESS
        </action_type>
        <parameters>
            <text_list>
                =AVERAGE(B2:D2)
            </text_list>
        </parameters>
    </step_38>

    <step_39>
        <action_desc>
            move to E3
        </action_desc>
        <action_type>
            PRESS
        </action_type>
        <parameters>
            <key_list>
                down
            </key_list>
        </parameters>
    </step_39>

   <step_40>
        <action_desc>
            enter the formula for average
        </action_desc>
        <action_type>
            PRESS
        </action_type>
        <parameters>
            <text_list>
                =AVERAGE(B3:D3)
            </text_list>
        </parameters>
    </step_40>

    <step_41>
        <action_desc>
            move to E4
        </action_desc>
        <action_type>
            PRESS
        </action_type>
        <parameters>
            <key_list>
                down
            </key_list>
        </parameters>
    </step_41>

   <step_42>
        <action_desc>
            enter the formula for average
        </action_desc>
        <action_type>
            PRESS
        </action_type>
        <parameters>
            <text_list>
                =AVERAGE(B4:D4)
            </text_list>
        </parameters>
    </step_42>

    <step_43>
        <action_desc>
            move to F2 from E4 cell
        </action_desc>
        <action_type>
            PRESS
        </action_type>
        <parameters>
            <key_list>
                right
                up
                up
            </key_list>
        </parameters>
    </step_43>

   <step_44>
        <action_desc>
            enter the formula for basic grading
        </action_desc>
        <action_type>
            PRESS
        </action_type>
        <parameters>
            <text_list>
                =IF(E2>=90, "A", IF(E2>=80, "B", IF(E2>=70, "C", IF(E2>=60, "D", "F"))))
            </text_list>
        </parameters>
    </step_44>

    <step_45>
        <action_desc>
            move to F3
        </action_desc>
        <action_type>
            PRESS
        </action_type>
        <parameters>
            <key_list>
                down
            </key_list>
        </parameters>
    </step_45>

   <step_46>
        <action_desc>
            enter the formula for basic grading
        </action_desc>
        <action_type>
            PRESS
        </action_type>
        <parameters>
            <text_list>
                =IF(E3>=90, "A", IF(E3>=80, "B", IF(E3>=70, "C", IF(E3>=60, "D", "F"))))
            </text_list>
        </parameters>
    </step_46>

    <step_47>
        <action_desc>
            move to F4
        </action_desc>
        <action_type>
            PRESS
        </action_type>
        <parameters>
            <key_list>
                down
            </key_list>
        </parameters>
    </step_47>

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

correction_prompt = """
You are an AI assistant that specializes in analyzing OS automation tasks and generating steps to fix issues and prepare for upcoming actions. I will provide you with a concatenated before/after image showing the state before an action was performed and the problematic state after, as well as details on the performed action, the next action to prepare for, and the tooling available to you.

Folloing is the task summary:
<task_summary>
{TASK_SUMMARY}
</task_summary>

Here is the concatenated before/after image showing the automation task failure attached as an image. (left side is the before and right side is the after)

Here are the tools you have available to use in your fix and preparation steps:
<tooling>
{TOOLING}
</tooling>

The following step that was performed leading to the failure was:  
<performed_step>
{PERFORMED_STEP}
</performed_step>

FOllowing is the associated action list for the performed step:
<action_list>
{PERFORMED_ACTION_LIST}
</action_list>

The next step in the queue that we need to prepare for is:
<prepare_for_next_action>
{PREPARE_FOR_NEXT_STEP}
</prepare_for_next_action>

First, carefully examine the before and after images, taking note of all UI elements and how they changed after the performed action. Consider how the performed action may have caused the observed failure. Think through how you can use the available tooling to remedy the failure and get the UI into an appropriate state for the next queued action.

Now, list out the specific steps to first fix the output from the failure and then prepare the UI state for the next action. Be as detailed as possible, referring to specific UI elements and tools used. Only use tools from the provided tooling list.

Following is an example response format:
<step_list>
    <step_1>
        <action_desc>
            Enter info in the first cell
        </action_desc>
        <action_type>
            PRESS
        </action_type>
        <parameters>
            <text_list>
                name
            </text_list>
        </parameters>
    </step_1>

    <step_2>
        <action_desc>
            Move to the right column
        </action_desc>
        <action_type>
            PRESS
        </action_type>
        <parameters>
            <key_list>
                right
            </key_list>
        </parameters>
    </step_2>

    <step_3>
        <action_desc>
            Enter some info in the new cell
        </action_desc>
        <action_type>
            PRESS
        </action_type>
        <parameters>
            <text_list>
                address
            </text_list>
        </parameters>
    </step_3>
...
<step_list>

Only and only respond in the above shown format, no other information needed, no explanations or additional details required. Just the executable step_list to fix the failure and prepare for the next action. I need to pass the step_list to another parser for executing everything.

Remember, your goal is to get the automation sequence back on track by fixing the current failure and proactively preventing the next action from failing as well. Restrict yourself to only the tooling provided. If the failure cannot be fixed or the next action cannot be prepared for with the given tools, say so.

Analyze the images and generate your fix and preparation steps for this OS automation error scenario.

Important sidenote: 
- You cannot jump to a certain cell, you have to navigate to it using arrow keys. So the keys should always be one of available keyboard keys.
- in most cases excel will be already open for you, so you don't have to worry about opening it. return an emtpy list if its anything outside of the excel file or application.
- Keep strings in text_list and keys in key_list. We already have a text_list parser that will manage its entry into excel key by key.
- "keys" for individual keyboard keys, "text" for typing text
- Never use the tab key to navigate, always use the arrow keys. Because the tab is inconsistent in excel and across different operating systems.
- Every step has an associated action plan generated by the next agent, so you have to prepare the UI for the next action to be executed by another agent.
- DO NOT CREATE steps to execute the new action or the next action, only realign or prepare the UI for the next action to be executed by another agent. For example, if the next action is to move from cell A to cell B, you should prepare the UI to be in cell A. OR if a certain cell has wrong information, delete & correct that and travel back to the correct cell so that the next action executes without an issue
"""

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
