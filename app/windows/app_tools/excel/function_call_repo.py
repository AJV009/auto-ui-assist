# build function calling context here
TOOLING = [
    {
        "name": "launch_excel_with_new_workbook",
        "description": "Launches Microsoft Excel with a new workbook.",
        "function_path": "app_tools.excel.helper_functions"
    },
    {
        "name": "launch_excel_with_existing_workbook",
        "description": "Launches Microsoft Excel with an existing workbook.",
        "parameters": {
            "file_name": {
                "type": "string",
                "description": "A unique file name with the file extension.",
            }
        },
        "required": ["file_name"],
        "function_path": "app_tools.excel.helper_functions"    
    },
    {
        "name": "open_blank_workbook",
        "description": "Opens a blank workbook in Excel",
        "function_path": "app_tools.excel.helper_functions"
    },
    {
        "name": "move_to_cell",
        "description": "Moves the cursor to a specific cell in Excel. ",
        "parameters": {
            "cell_address": {
                "type": "string",
                "description": "The address of the cell (e.g., 'A1', 'B3').",
            }
        },
        "required": ["cell_address"],
        "function_path": "app_tools.excel.helper_functions"
    },
    {
        "name": "input_data_in_cell",
        "description": "Inputs data into the currently active cell in Excel.",
        "parameters": {
            "data": {
                "type": "string",
                "description": "The data to be entered into the cell.",
            }
        },
        "required": ["data"],
        "function_path": "app_tools.excel.helper_functions"
    },
    {
        "name": "move_and_input_data",
        "description": "Moves the cursor to a specific cell and inputs data into it.",
        "parameters": {
            "cell_address": {
                "type": "string",
                "description": "The address of the cell (e.g., 'A1', 'B3').",
            },
            "data": {
                "type": "string",
                "description": "The data to be entered into the cell.",
            }
        },
        "required": ["cell_address", "data"],
        "function_path": "app_tools.excel.helper_functions"
    },
    {
        "name": "select_range",
        "description": "Selects a range of cells in Excel.",
        "parameters": {
            "start_cell": {
                "type": "string",
                "description": "The address of the starting cell (e.g., 'A1', 'B3').",
            },
            "end_cell": {
                "type": "string",
                "description": "The address of the ending cell (e.g., 'C5', 'D10').",
            }
        },
        "required": ["start_cell", "end_cell"],
        "function_path": "app_tools.excel.helper_functions"
    },
    {
        "name": "create_table",
        "description": "Creates a table in Excel from the selected range of cells.",
        "function_path": "app_tools.excel.helper_functions"
    },
    {
        "name": "execute_hotkey",
        "description": "Presses a specific hotkey combination in Excel.",
        "parameters": {
            "hotkey": {
                "type": "string",
                "description": "The hotkey combination to be executed (e.g., 'ctrl+c', 'alt+f4').",
            }
        },
        "required": ["hotkey"],
        "function_path": "app_tools.excel.helper_functions"
    },
    {
        "name": "input_key",
        "description": "Inputs a specific key in Excel.",
        "parameters": {
            "key": {
                "type": "string",
                "description": "The key to be entered (e.g., 'enter', 'esc').",
            }
        },
        "required": ["key"],
        "function_path": "app_tools.excel.helper_functions"
    },
    {
        "name": "drag_fill_cells",
        "description": "Drags and fills cells in Excel from the starting cell to the ending cell.",
        "parameters": {
            "start_cell": {
                "type": "string",
                "description": "The address of the starting cell (e.g., 'A1', 'B3').",
            },
            "direction": {
                "type": "string",
                "description": "The direction of the fill (e.g., 'down', 'right').",
            },
            "num_cells": {
                "type": "integer",
                "description": "The number of cells to fill.",
            }
        },
        "required": ["start_cell", "direction", "num_cells"],
        "function_path": "app_tools.excel.helper_functions"
    }
]
