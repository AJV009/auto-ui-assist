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
        "name": "save_workbook_to_path",
        "description": "Saves the current workbook in Excel to a specific file path. Any complicated file paths should be transformed into just file name and ideal location.",
        "parameters": {
            "file_name": {
                "type": "string",
                "description": "The file name or path where the workbook will be saved. If the file already exists, it will be overwritten. If only the file name is provided, the file will be saved in the default directory.",
            },
            "ideal_location": {
                "type": "string",
                "description": "The ideal location to save the file (e.g., 'desktop', 'documents', 'default').",
                "default": "default"
            }
        },
        "required": ["file_name"],
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
        "name": "create_simple_chart",
        "description": "Creates a simple chart in Excel from the selected range of cells.",
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
    },
    {
        "name": "enable_auto_filter",
        "description": "Enables the auto filter feature in Excel for the selected range of cells.",
        "function_path": "app_tools.excel.helper_functions"
    },
    {
        "name": "simple_sort",
        "description": "Sorts the selected range of cells in Excel in ascending or descending order.",
        "parameters": {
            "sort_order": {
                "type": "string",
                "description": "The sort order ('ascending' or 'descending').",
            },
            "sort_col": {
                "type": "string",
                "description": "The column to sort by (e.g., 'A', 'B').",
            }
        },
        "required": ["sort_order", "sort_col"],
        "function_path": "app_tools.excel.helper_functions"
    },
    {
        "name": "simple_filter",
        "description": "Filters the selected range of cells in Excel based on a specific criteria.",
        "parameters": {
            "filter_col": {
                "type": "string",
                "description": "The column to filter by (e.g., 'A', 'B').",
            },
            "filter_value": {
                "type": "string",
                "description": "The value to filter by.",
            }
        },
        "required": ["filter_col", "filter_value"],
        "function_path": "app_tools.excel.helper_functions"
    },
    {
        "name": "run_predefined_macro",
        "description": "Runs a predefined macro in Excel.",
        "parameters": {
            "macro_name": {
                "type": "string",
                "description": "The name of the macro to run.",
            }
        },
        "required": ["macro_name"],
        "function_path": "app_tools.excel.helper_functions"
    },
    {
        "name": "click_button",
        "description": "Clicks a specific button in Excel.",
        "parameters": {
            "button_name": {
                "type": "string",
                "description": "The name of the button to click.",
            }
        },
        "required": ["button_name"],
        "function_path": "app_tools.excel.helper_functions"
    }
]
