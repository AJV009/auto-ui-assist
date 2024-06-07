import pyautogui

width, height= pyautogui.size()
X_MAX = width
Y_MAX = height

KEYBOARD_KEYS = [
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

ACTION_SPACE = [
    {
        "action_type": "MOVE_TO",
        "note": "move the cursor to the specified position",
        "parameters": {
            "x": {
                "type": float,
                "range": [0, X_MAX],
                "optional": False,
            },
            "y": {
                "type": float,
                "range": [0, Y_MAX],
                "optional": False,
            }
        }
    },
    {
        "action_type": "CLICK",
        "note": "click the left button if the button not specified, otherwise click the specified button; click at the current position if x and y are not specified, otherwise click at the specified position",
        "parameters": {
            "button": {
                "type": str,
                "range": ["left", "right", "middle"],
                "optional": True,
            },
            "x": {
                "type": float,
                "range": [0, X_MAX],
                "optional": True,
            },
            "y": {
                "type": float,
                "range": [0, Y_MAX],
                "optional": True,
            },
            "num_clicks": {
                "type": int,
                "range": [1, 2, 3],
                "optional": True,
            },
        }
    },
    {
        "action_type": "MOUSE_DOWN",
        "note": "press the left button if the button not specified, otherwise press the specified button",
        "parameters": {
            "button": {
                "type": str,
                "range": ["left", "right", "middle"],
                "optional": True,
            }
        }
    },
    {
        "action_type": "MOUSE_UP",
        "note": "release the left button if the button not specified, otherwise release the specified button",
        "parameters": {
            "button": {
                "type": str,
                "range": ["left", "right", "middle"],
                "optional": True,
            }
        }
    },
    {
        "action_type": "RIGHT_CLICK",
        "note": "right click at the current position if x and y are not specified, otherwise right click at the specified position",
        "parameters": {
            "x": {
                "type": float,
                "range": [0, X_MAX],
                "optional": True,
            },
            "y": {
                "type": float,
                "range": [0, Y_MAX],
                "optional": True,
            }
        }
    },
    {
        "action_type": "DOUBLE_CLICK",
        "note": "double click at the current position if x and y are not specified, otherwise double click at the specified position",
        "parameters": {
            "x": {
                "type": float,
                "range": [0, X_MAX],
                "optional": True,
            },
            "y": {
                "type": float,
                "range": [0, Y_MAX],
                "optional": True,
            }
        }
    },
    {
        "action_type": "DRAG_TO",
        "note": "drag the cursor to the specified position with the left button pressed",
        "parameters": {
            "x": {
                "type": float,
                "range": [0, X_MAX],
                "optional": False,
            },
            "y": {
                "type": float,
                "range": [0, Y_MAX],
                "optional": False,
            }
        }
    },
    {
        "action_type": "SCROLL",
        "note": "scroll the mouse wheel up or down",
        "parameters": {
            "dx": {
                "type": int,
                "range": None,
                "optional": False,
            },
            "dy": {
                "type": int,
                "range": None,
                "optional": False,
            }
        }
    },
    {
        "action_type": "TYPING",
        "note": "type the specified text",
        "parameters": {
            "text": {
                "type": str,
                "range": None,
                "optional": False,
            }
        }
    },
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
            }
        }
    },
    ############################################################################################################
    {
        "action_type": "WAIT",
        "note": "wait until the next action",
    },
    {
        "action_type": "FAIL",
        "note": "decide the task can not be performed",
    },
    {
        "action_type": "DONE",
        "note": "decide the task is done",
    }
]
