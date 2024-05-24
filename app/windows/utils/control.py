from typing import Any, Dict
import random

import pyautogui

from utils.actions import KEYBOARD_KEYS

def execute_action(action: Dict[str, Any]):
    """
    Executes an action on the server computer.
    
    Parameters:
        - action (Dict[str, Any]): A dictionary representing the action to be executed.
            - action_type (str): The type of action to be executed.
            - parameters (Dict[str, Any], optional): Additional parameters specific to the action type.
    
    Returns:
        - None
    
    Possible action types and their parameters:
        - MOVE_TO:
            - x (int): The x-coordinate to move the mouse to.
            - y (int): The y-coordinate to move the mouse to.
        - CLICK:
            - button (str, optional): The mouse button to click. Defaults to left button.
            - x (int, optional): The x-coordinate to click at.
            - y (int, optional): The y-coordinate to click at.
            - num_clicks (int, optional): The number of clicks to perform. Defaults to 1.
        - MOUSE_DOWN:
            - button (str, optional): The mouse button to press down. Defaults to left button.
        - MOUSE_UP:
            - button (str, optional): The mouse button to release. Defaults to left button.
        - RIGHT_CLICK:
            - x (int, optional): The x-coordinate to right-click at.
            - y (int, optional): The y-coordinate to right-click at.
        - DOUBLE_CLICK:
            - x (int, optional): The x-coordinate to double-click at.
            - y (int, optional): The y-coordinate to double-click at.
        - DRAG_TO:
            - x (int): The x-coordinate to drag the mouse to.
            - y (int): The y-coordinate to drag the mouse to.
        - SCROLL:
            - dx (int, optional): The amount to scroll horizontally.
            - dy (int, optional): The amount to scroll vertically.
        - TYPING:
            - text (str): The text to type.
        - PRESS:
            - key (str): The key to press.
        - KEY_DOWN:
            - key (str): The key to press down.
        - KEY_UP:
            - key (str): The key to release.
        - HOTKEY:
            - keys (List[str]): A list of keys to press as a hotkey combination.
        - WAIT:
            - No additional parameters required.
        - FAIL:
            - No additional parameters required.
        - DONE:
            - No additional parameters required.
    
    Example usage:
        # Move the mouse to coordinates (100, 200)
        execute_action({"action_type": "MOVE_TO", "parameters": {"x": 100, "y": 200}})
        
        # Click the left mouse button at coordinates (300, 400)
        execute_action({"action_type": "CLICK", "parameters": {"x": 300, "y": 400}})
        
        # Type the text "Hello, World!"
        execute_action({"action_type": "TYPING", "parameters": {"text": "Hello, World!"}})
        
        # Press the hotkey combination Ctrl+Alt+Delete
        execute_action({"action_type": "HOTKEY", "parameters": {"keys": ["ctrl", "alt", "delete"]}})
    """
    if action in ['WAIT', 'FAIL', 'DONE']:
        return

    action_type = action["action_type"]
    parameters = action["parameters"] if "parameters" in action else {}
    move_mode = random.choice(
        ["pyautogui.easeInQuad", "pyautogui.easeOutQuad", "pyautogui.easeInOutQuad", "pyautogui.easeInBounce",
         "pyautogui.easeInElastic"])
    duration = random.uniform(0.5, 1)

    if action_type == "MOVE_TO":
        if parameters == {} or None:
            pyautogui.moveTo()
        elif "x" in parameters and "y" in parameters:
            x = parameters["x"]
            y = parameters["y"]
            pyautogui.moveTo(x, y, duration, move_mode)
        else:
            raise Exception(f"Unknown parameters: {parameters}")

    elif action_type == "CLICK":
        if parameters == {} or None:
            pyautogui.click()
        elif "button" in parameters and "x" in parameters and "y" in parameters:
            button = parameters["button"]
            x = parameters["x"]
            y = parameters["y"]
            if "num_clicks" in parameters:
                num_clicks = parameters["num_clicks"]
                pyautogui.click(button=button, x=x, y=y, clicks=num_clicks)
            else:
                pyautogui.click(button=button, x=x, y=y)
        elif "button" in parameters and "x" not in parameters and "y" not in parameters:
            button = parameters["button"]
            if "num_clicks" in parameters:
                num_clicks = parameters["num_clicks"]
                pyautogui.click(button=button, clicks=num_clicks)
            else:
                pyautogui.click(button=button)
        elif "button" not in parameters and "x" in parameters and "y" in parameters:
            x = parameters["x"]
            y = parameters["y"]
            if "num_clicks" in parameters:
                num_clicks = parameters["num_clicks"]
                pyautogui.click(x=x, y=y, clicks=num_clicks)
            else:
                pyautogui.click(x=x, y=y)
        else:
            raise Exception(f"Unknown parameters: {parameters}")

    elif action_type == "MOUSE_DOWN":
        if parameters == {} or None:
            pyautogui.mouseDown()
        elif "button" in parameters:
            button = parameters["button"]
            pyautogui.mouseDown(button=button)
        else:
            raise Exception(f"Unknown parameters: {parameters}")

    elif action_type == "MOUSE_UP":
        if parameters == {} or None:
            pyautogui.mouseUp()
        elif "button" in parameters:
            button = parameters["button"]
            pyautogui.mouseUp(button=button)
        else:
            raise Exception(f"Unknown parameters: {parameters}")

    elif action_type == "RIGHT_CLICK":
        if parameters == {} or None:
            pyautogui.rightClick()
        elif "x" in parameters and "y" in parameters:
            x = parameters["x"]
            y = parameters["y"]
            pyautogui.rightClick(x=x, y=y)
        else:
            raise Exception(f"Unknown parameters: {parameters}")
    
    elif action_type == "DOUBLE_CLICK":
        if parameters == {} or None:
            pyautogui.doubleClick()
        elif "x" in parameters and "y" in parameters:
            x = parameters["x"]
            y = parameters["y"]
            pyautogui.doubleClick(x=x, y=y)
        else:
            raise Exception(f"Unknown parameters: {parameters}")

    elif action_type == "DRAG_TO":
        if "x" in parameters and "y" in parameters:
            x = parameters["x"]
            y = parameters["y"]
            pyautogui.dragTo(x, y, duration=1.0, button='left', mouseDownUp=True)
        else:
            raise Exception(f"Unknown parameters: {parameters}")

    elif action_type == "SCROLL":
        if "dx" in parameters and "dy" in parameters:
            dx = parameters["dx"]
            dy = parameters["dy"]
            pyautogui.hscroll(dx)
            pyautogui.vscroll(dy)
        elif "dx" in parameters and "dy" not in parameters:
            dx = parameters["dx"]
            pyautogui.hscroll(dx)
        elif "dx" not in parameters and "dy" in parameters:
            dy = parameters["dy"]
            pyautogui.vscroll(dy)
        else:
            raise Exception(f"Unknown parameters: {parameters}")

    elif action_type == "TYPING":
        if "text" in parameters:
            text = parameters["text"]
            pyautogui.typewrite(text)
        else:
            raise Exception(f"Unknown parameters: {parameters}")

    elif action_type == "PRESS":
        if "keys" in parameters:
            keys = parameters["keys"]
            if not isinstance(keys, list):
                raise Exception("Keys must be a list of keys")
            for key in keys:
                if key.lower() not in KEYBOARD_KEYS:
                    raise Exception(f"Key must be one of {KEYBOARD_KEYS}")
            pyautogui.press(keys, interval=0.5)
        elif "key" in parameters:
            key = parameters["key"]
            if key.lower() not in KEYBOARD_KEYS:
                raise Exception(f"Key must be one of {KEYBOARD_KEYS}")
            pyautogui.press(key)
        else:
            raise Exception(f"Unknown parameters: {parameters}")

    elif action_type == "KEY_DOWN":
        if "key" in parameters:
            key = parameters["key"]
            if key.lower() not in KEYBOARD_KEYS:
                raise Exception(f"Key must be one of {KEYBOARD_KEYS}")
            pyautogui.keyDown(key)
        else:
            raise Exception(f"Unknown parameters: {parameters}")

    elif action_type == "KEY_UP":
        if "key" in parameters:
            key = parameters["key"]
            if key.lower() not in KEYBOARD_KEYS:
                raise Exception(f"Key must be one of {KEYBOARD_KEYS}")
            pyautogui.keyUp(key)
        else:
            raise Exception(f"Unknown parameters: {parameters}")

    elif action_type == "HOTKEY":
        if "keys" in parameters:
            keys = parameters["keys"]
            if not isinstance(keys, list):
                raise Exception("Keys must be a list of keys")
            for key in keys:
                if key.lower() not in KEYBOARD_KEYS:
                    raise Exception(f"Key must be one of {KEYBOARD_KEYS}")
            pyautogui.hotkey(*keys)
        else:
            raise Exception(f"Unknown parameters: {parameters}")

    elif action_type in ['WAIT', 'FAIL', 'DONE']:
        pass

    else:
        raise Exception(f"Unknown action type: {action_type}")
