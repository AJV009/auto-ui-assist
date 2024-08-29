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
        "description": "Selects a range or multiple ranges of cells in Excel.",
        "parameters": {
            "range_string": {
                "type": "string",
                "description": "A string representing one or more cell ranges. Multiple ranges should be separated by commas. Example: 'A1:C5, E1:G5, I1:K5'."
            }
        },
        "required": ["range_string"],
        "function_path": "app_tools.excel.helper_functions"
    },
    {
        "name": "create_table",
        "description": "Creates a table in Excel from the selected range of cells.",
        "function_path": "app_tools.excel.helper_functions"
    },
    {
        "name": "create_chart",
        "description": "Creates a simple chart in Excel from the selected range of cells. Chart types:\n\n1. Bar Charts:\n   a) 2-D Column: bar_2_d_clustered_column (default), bar_2_d_stacked_column, bar_2_d_100_stacked_column\n   b) 3-D Column: bar_3_d_clustered_column, bar_3_d_stacked_column, bar_3_d_100_stacked_column, bar_3_d_column\n   c) 2-D Bar: bar_2_d_clustered_bar, bar_2_d_stacked_bar, bar_2_d_100_stacked_bar\n   d) 3-D Bar: bar_3_d_clustered_bar, bar_3_d_stacked_bar, bar_3_d_100_stacked_bar\n2. Hierarchy: hierarchy_treemap, hierarchy_sunbrust\n3. Line / Area:\n   a) 2-D Line: line_2_d_line, line_2_d_stacked_line, line_2_d_100_stacked_line, line_2_d_line_with_markers, line_2_d_stacked_line_with_markers, line_2_d_100_stacked_line_with_markers\n   b) 3-D Line: line_3_d_line\n   c) 2-D Area: line_2_d_area, line_2_d_stacked_area, line_2_d_100_stacked_area\n   d) 3-D Area: line_3_d_area, line_3_d_stacked_area, line_3_d_100_stacked_area\n4. Pie / Donut:\n   a) 2-D Pie: pie_2_d_pie, pie_2_d_pie_of_pie, pie_2_d_bar_of_pie\n   b) 3-D Pie: pie_3_d_pie\n   c) Doughnut: pie_doughnut\n5. Statistical: statistical_histogram, statistical_box_whisker, statistical_pareto\n6. Scatter / Bubble:\n   a) Scatter: scatter_scatter, scatter_straight_lines, scatter_smooth_lines, scatter_straight_lines_markers, scatter_smooth_lines_markers\n   b) Bubble: scatter_bubble, scatter_3_d_bubble\n7. Combo: combo_clustered_column_line, combo_clustered_column_line_secondary_axis, combo_stacked_area_clustered_column\n8. Extra:\n   a) Waterfall: extra_waterfall\n   b) Funnel: extra_funnel\n   c) Surface: extra_3_d_surface, extra_wireframe_3_d_surface, extra_contour, extra_wireframe_contour\n   d) Radar: extra_radar, extra_radar_markers, extra_filled_radar\n9. Recommended pivot tables / Standard Automatic Pivot Table: recommended_pivot_tables\n\nUsage: Specify the desired chart_type as a string parameter. If not specified, defaults to 'bar_2_d_clustered_column'. For multi-range selection charts, select the range before calling this function. Ensure Excel window is active and visible when calling.",
        "parameters": {
            "chart_type": {
                "type": "string",
                "description": "The type of chart to be created."
            }
        },
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
        "description": "Enables the auto filter feature in Excel. If a range is specified (e.g., 'A1:D10'), it applies to that range. If no range is provided, it applies to the complete sheet.",
        "parameters": {
            "range_string": {
                "type": "string",
                "description": "Optional. A string representing the range to apply auto filter (e.g., 'A1:D10')."
            }
        },
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
