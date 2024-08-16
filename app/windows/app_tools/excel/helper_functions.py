
import pyautogui
import time
import psutil
import os
from pywinauto import Application, Desktop

"""
Internal helper function
"""
def is_excel_running():
    """Check if Excel is already running."""
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] == 'EXCEL.EXE':
            return True
    return False

def focus_existing_excel():
    """Focus on the existing Excel window."""
    app = Application(backend="uia").connect(title_re=".*Excel.*")
    window = app.top_window()
    window.set_focus()

def save_excel_pid(session_path):
    """
    Returns the PID of the most recently started Excel process.
    """
    excel_pid = None
    for proc in psutil.process_iter(['pid', 'name', 'create_time']):
        if proc.info['name'] == 'EXCEL.EXE':
            excel_pid = proc.info['pid']
    
    file_path = session_path + "/current_app_pid.txt"
    with open(file_path, 'w') as f:
        f.write(str(excel_pid))

def retrieve_excel_pid(session_path):
    """
    Retrieves the PID of the Excel process from the session path.
    """
    file_path = session_path + "/current_app_pid.txt"
    with open(file_path, 'r') as f:
        excel_pid = int(f.read())
    return excel_pid

def switch_to_app(extra_args=None):
    # get the PID of the Excel process and switch to it
    try:
        if extra_args:
            if 'temp_session_step_path' in extra_args:
                excel_pid = retrieve_excel_pid(extra_args['temp_session_step_path'])
                app = Application(backend="uia").connect(process=excel_pid)
                window = app.top_window()
                window.set_focus()
    except Exception:
        app_title = "Excel"
        try:
            windows = Desktop(backend="uia").windows(title_re=".*" + app_title + ".*")
            topmost_window = sorted(windows, key=lambda w: w.rectangle().top)[0]
            app = Application(backend="uia").connect(handle=topmost_window.handle)
            window = app.top_window()
            window.set_focus()
        except Exception:
            try:
                app = Application(backend="uia").connect(title_re=".*" + app_title + ".*")
                window = app.window(title_re=".*" + app_title + ".*")
                window.set_focus()
            except Exception:
                pass

"""
External helper functions
"""
def launch_excel_with_new_workbook(extra_args=None):
    """
    Launches Microsoft Excel or focuses on an existing instance.
    Ensures only one instance of Excel is running.
    """
    if is_excel_running():
        focus_existing_excel()
    else:
        pyautogui.hotkey('win', 'r')  # Open the Run dialog
        pyautogui.write('excel')  # Enter 'excel' to launch Excel
        pyautogui.press('enter')  # Confirm the launch
        time.sleep(5)  # Wait for Excel to open
    
    # Save the PID of the Excel process
    if extra_args and 'temp_session_step_path' in extra_args:
        save_excel_pid(extra_args['temp_session_step_path'])

    pyautogui.press('enter')  # select empty workbook

def launch_excel_with_existing_workbook(file_name, extra_args=None):
    """
    Launches Microsoft Excel with an existing workbook or focuses on an existing instance.
    Ensures only one instance of Excel is running.

    Args:
        file_name (str): A unique file name with the file extension.
    """
    if is_excel_running():
        focus_existing_excel()
    else:
        pyautogui.hotkey('win', 'r')  # Open the Run dialog
        pyautogui.write('excel')  # Enter 'excel' to launch Excel
        pyautogui.press('enter')  # Confirm the launch
        time.sleep(5)  # Wait for Excel to open

    # Save the PID of the Excel process
    if extra_args and 'temp_session_step_path' in extra_args:
        save_excel_pid(extra_args['temp_session_step_path'])

    pyautogui.hotkey('ctrl', 'o')  # Open an existing workbook
    pyautogui.press('enter') 
    pyautogui.press('enter')  # double enter move to the search bar
    pyautogui.write(file_name)  # Enter the file name
    pyautogui.press('enter')  # Confirm the file name

def save_workbook_to_path(file_name, ideal_location='default', extra_args=None):
    """
    Saves the active file in Excel to a specific file path.
    If the file already exists, it will be overwritten.
    If only file name is provided, the file will be saved in the default directory.

    Args:
        file_name (str): The file name or path to save the file to.
        ideal_location (str): The ideal location to save the file to. Can be one of the following: 'desktop', 'documents', 'downloads', ''pictures', 'music', 'videos', 'default'.
    """
    pyautogui.hotkey('f12')  # Open the "Save As" dialog

    time.sleep(3)  # Wait for the dialog to open
    # Get and write the file path
    file_name = file_name.split('/')[-1]
    current_user = os.environ['USERNAME']
    ideal_locations = {
        'desktop': 'Desktop',
        'documents': 'Documents',
        'downloads': 'Downloads',
        'pictures': 'Pictures',
        'music': 'Music',
        'videos': 'Videos',
        'default': 'default'
    }
    ideal_location_path = ""
    if ideal_location == 'default':
        pyautogui.write(file_name)  # Enter the file name
    else:
        if ideal_location in ideal_locations:
            ideal_location_path = "C:/Users/" + current_user + "/" + ideal_locations[ideal_location] + "/"
            pyautogui.write(ideal_location_path + file_name)  # Enter the file path
        else:
            pyautogui.write(file_name)

    pyautogui.press('enter')  # Confirm the file path
    pyautogui.press('enter')  # Confirm the file overwrite if it already exists

def move_to_cell(cell_address, extra_args=None):
    """
    Moves the cursor to a specific cell in Excel.

    Args:
        cell_address (str): The address of the cell (e.g., 'A1', 'B3').
    """
    pyautogui.press('esc')  # Ensure we're in normal mode
    pyautogui.hotkey('ctrl', 'g')  # Open the "Go To" dialog
    pyautogui.write(cell_address)  # Enter the cell address
    pyautogui.press('enter')  # Confirm the cell address

def input_data_in_cell(data, extra_args=None):
    """
    Inputs data into the currently active cell in Excel.

    Args:
        data (str): The data to be entered into the cell.
    """
    pyautogui.write(data)
    pyautogui.press('enter')  # Confirm the data entry

def move_and_input_data(cell_address, data, extra_args=None):
    """
    Moves the cursor to a specific cell and inputs data into it.

    Args:
        cell_address (str): The address of the cell (e.g., 'A1', 'B3').
        data (str): The data to be entered into the cell.
    """
    move_to_cell(cell_address)  # Move to the specified cell
    input_data_in_cell(data)  # Input the data into the cell

def select_range(range_string, extra_args=None):
    """
    Selects a range or multiple ranges of cells in Excel.

    Args:
        range_string (str): A string representing one or more cell ranges.
                            Multiple ranges should be separated by commas.
                            Example: 'A1:C5, E1:G5, I1:K5'
    """
    # Use the Go To dialog to select the range(s)
    pyautogui.hotkey('ctrl', 'g')  # Open the "Go To" dialog
    pyautogui.write(range_string)  # Enter the range(s)
    pyautogui.press('enter')  # Confirm the selection

def create_table(extra_args=None):
    """
    Creates a table in Excel from the selected range of cells.
    """
    pyautogui.hotkey('ctrl', 't')
    pyautogui.press('enter')
    
def create_chart(chart_type="bar_2_d_clustered_column",extra_args=None):
    """
    Creates a simple chart in Excel from the selected range of cells.

    Args:
        chart_type (str): The type of chart to be created
    
    Supported types:
    - Bar Charts
        - 2-D Column
            - Clustered Column: 'bar_2_d_clustered_column'
            - Stacked Column: 'bar_2_d_stacked_column'
            - 100% Stacked Column: 'bar_2_d_100_stacked_column'
        - 3-D Column
            - Clustered Column: 'bar_3_d_clustered_column'
            - Stacked Column: 'bar_3_d_stacked_column'
            - 100% Stacked Column: 'bar_3_d_100_stacked_column'
            - 3-D Column: 'bar_3_d_column'
        - 2-D Bar
            - Clustered Bar: 'bar_2_d_clustered_bar'
            - Stacked Bar: 'bar_2_d_stacked_bar'
            - 100% Stacked Bar: 'bar_2_d_100_stacked_bar'
        - 3-D Bar
            - Clustered Bar: 'bar_3_d_clustered_bar'
            - Stacked Bar: 'bar_3_d_stacked_bar'
            - 100% Stacked Bar: 'bar_3_d_100_stacked_bar'
    - Hierarchy
        - Treemap: 'hierarchy_treemap'
        - Sunburst: 'hierarchy_sunbrust'
    - Line / Area
        - 2-D Line
            - Line: 'line_2_d_line'
            - Stacked Line: 'line_2_d_stacked_line'
            - 100% Stacked Line: 'line_2_d_100_stacked_line'
            - Line with Markers: 'line_2_d_line_with_markers'
            - Stacked Line with Markers: 'line_2_d_stacked_line_with_markers'
            - 100% Stacked Line with Markers: 'line_2_d_100_stacked_line_with_markers'
        - 3-D Line
            - Line: 'line_3_d_line'
        - 2-D Area
            - Area: 'line_2_d_area'
            - Stacked Area: 'line_2_d_stacked_area'
            - 100% Stacked Area: 'line_2_d_100_stacked_area'
        - 3-D Area
            - Area: 'line_3_d_area'
            - Stacked Area: 'line_3_d_stacked_area'
            - 100% Stacked Area: 'line_3_d_100_stacked_area'
    - Pie / Donut
        - 2-D Pie
            - Pie: 'pie_2_d_pie'
            - Pie of Pie: 'pie_2_d_pie_of_pie'
            - Bar of Pie: 'pie_2_d_bar_of_pie'
        - 3-D Pie
            - Pie: 'pie_3_d_pie'
        - Doughnut: 'pie_doughnut'
    - Statistical
        - Histogram: 'statistical_histogram'
        - Box & Whisker: 'statistical_box_whisker'
        - Pareto: 'statistical_pareto'
    - Scatter / Bubble
        - Scatter
            - Scatter: 'scatter_scatter'
            - Scatter with Straight Lines: 'scatter_straight_lines'
            - Scatter with Smooth Lines: 'scatter_smooth_lines'
            - Scatter with Straight Lines & Markers: 'scatter_straight_lines_markers'
            - Scatter with Smooth Lines & Markers: 'scatter_smooth_lines_markers'
        - Bubble
            - Bubble: 'scatter_bubble'
            - 3-D Bubble: 'scatter_3_d_bubble'
    - Combo
        - Clustered Column - Line: 'combo_clustered_column_line'
        - Clustered Column - Line on Secondary Axis: 'combo_clustered_column_line_secondary_axis'
        - Stacked Area - Clustered Column: 'combo_stacked_area_clustered_column'
    - Extra
        - Waterfall: 'extra_waterfall'
        - Funnel: 'extra_funnel'
        - Surface
            - 3-D Surface: 'extra_3_d_surface'
            - Wireframe 3-D Surface: 'extra_wireframe_3_d_surface'
            - Contour: 'extra_contour'
            - Wireframe Contour: 'extra_wireframe_contour'
        - Radar
            - Radar: 'extra_radar'
            - Radar with Markers: 'extra_radar_markers'
            - Filled Radar: 'extra_filled_radar'
    - Recommended pivot tables: 'recommended_pivot_tables'

    Note: If selecting a chart that needs multi range selection, please select the range before calling this function.
    """
    CHART_TYPE_COMBOS = [
        # Bar Charts
        {"type": "bar", "combo": "alt+n+c+2"},
        {"type": "bar_2_d_clustered_column", "combo": [""]},
        {"type": "bar_2_d_stacked_column", "combo": ["right"]},
        {"type": "bar_2_d_100_stacked_column", "combo": ["right", "right"]},
        {"type": "bar_3_d_clustered_column", "combo": ["down"]},
        {"type": "bar_3_d_stacked_column", "combo": ["down", "right"]},
        {"type": "bar_3_d_100_stacked_column", "combo": ["down", "right", "right"]},
        {"type": "bar_3_d_column", "combo": ["down", "right", "right", "right"]},
        {"type": "bar_2_d_clustered_bar", "combo": ["down", "down"]},
        {"type": "bar_2_d_stacked_bar", "combo": ["down", "down", "right"]},
        {"type": "bar_2_d_100_stacked_bar", "combo":  ["down", "down", "right", "right"]},
        {"type": "bar_3_d_clustered_bar", "combo": ["down", "down", "down"]},
        {"type": "bar_3_d_stacked_bar", "combo": ["down", "down", "down", "right"]},
        {"type": "bar_3_d_100_stacked_bar", "combo": ["down", "down", "down", "right", "right"]},

        # Hierarchy Charts
        {"type": "hierarchy", "combo": "alt+n+h+i"},
        {"type": "hierarchy_treemap", "combo": [""]},
        {"type": "hierarchy_sunbrust", "combo": ["right"]},

        # Line / Area Charts
        {"type": "line", "combo": "alt+n+n+1"},
        {"type": "line_2_d_line", "combo": [""]},
        {"type": "line_2_d_stacked_line", "combo": ["right"]},
        {"type": "line_2_d_100_stacked_line", "combo": ["right", "right"]},
        {"type": "line_2_d_line_with_markers", "combo": ["right", "right", "right"]},
        {"type": "line_2_d_stacked_line_with_markers", "combo": ["right", "right", "right", "right"]},
        {"type": "line_2_d_100_stacked_line_with_markers", "combo": ["right", "right", "right", "right", "right"]},
        {"type": "line_3_d_line", "combo": ["down", "down"]},
        {"type": "line_2_d_area", "combo": ["down", "down", "down"]},
        {"type": "line_2_d_stacked_area", "combo": ["down", "down", "down", "right"]},
        {"type": "line_2_d_100_stacked_area", "combo": ["down", "down", "down", "right", "right"]},
        {"type": "line_3_d_area", "combo": ["down", "down", "down", "down"]},
        {"type": "line_3_d_stacked_area", "combo": ["down", "down", "down", "down", "right"]},
        {"type": "line_3_d_100_stacked_area", "combo": ["down", "down", "down", "down", "right", "right"]},

        # Pie / Donut Charts
        {"type": "pie", "combo": "alt+n+q"},
        {"type": "pie_2_d_pie", "combo": [""]},
        {"type": "pie_2_d_pie_of_pie", "combo": ["right"]},
        {"type": "pie_2_d_bar_of_pie", "combo": ["right", "right"]},
        {"type": "pie_3_d_pie", "combo": ["down"]},
        {"type": "pie_doughnut", "combo": ["down", "down"]},

        # Statistical Charts
        {"type": "statistical", "combo": "alt+n+s+a"},
        {"type": "statistical_histogram", "combo": [""]},
        {"type": "statistical_pareto", "combo": ["right"]},
        {"type": "statistical_box_whisker", "combo": ["down"]},

        # Scatter / Bubble Charts
        {"type": "scatter", "combo": "alt+n+d"},
        {"type": "scatter_scatter", "combo": [""]},
        {"type": "scatter_smooth_lines_markers", "combo": ["right"]},
        {"type": "scatter_smooth_lines", "combo": ["right", "right", "right"]},
        {"type": "scatter_straight_lines_markers", "combo": ["right", "right", "right", "right"]},
        {"type": "scatter_straight_lines", "combo": ["right", "right", "right", "right", "right"]},
        {"type": "scatter_bubble", "combo": ["down", "down"]},
        {"type": "scatter_3_d_bubble", "combo": ["down", "down", "right"]},

        # Combo Charts
        {"type": "combo", "combo": "alt+n+s+d"},
        {"type": "combo_clustered_column_line", "combo": [""]},
        {"type": "combo_clustered_column_line_secondary_axis", "combo": ["right"]},
        {"type": "combo_stacked_area_clustered_column", "combo": ["right", "right"]},

        # Extra Charts
        {"type": "extra", "combo": "alt+n+i+1"},
        {"type": "extra_waterfall", "combo": [""]},
        {"type": "extra_funnel", "combo": ["down"]},
        {"type": "extra_3_d_surface", "combo": ["down", "down", "down"]},
        {"type": "extra_wireframe_3_d_surface", "combo": ["down", "down", "down", "right"]},
        {"type": "extra_contour", "combo": ["down", "down", "down", "right", "right"]},
        {"type": "extra_wireframe_contour", "combo": ["down", "down", "down", "right", "right", "right"]},
        {"type": "extra_radar", "combo": ["down", "down", "down", "down"]},
        {"type": "extra_radar_markers", "combo": ["down", "down", "down", "down", "right"]},
        {"type": "extra_filled_radar", "combo": ["down", "down", "down", "down", "right", "right"]},

        # Recommended Pivot Tables
        {"type": "recommended_pivot_tables", "combo":  "alt+n+s+p+tab+tab+tab"}
    ]
    # Extract the first word from chart_type
    chart_category = chart_type.split('_')[0]

    # Find the initial combo for the chart category
    initial_combo = next((item['combo'] for item in CHART_TYPE_COMBOS if item['type'] == chart_category), None)

    if initial_combo:
        # Execute the initial combo
        pyautogui.hotkey(*initial_combo.split('+'))

        # Find the specific chart type combo
        specific_combo = next((item['combo'] for item in CHART_TYPE_COMBOS if item['type'] == chart_type), None)

        if specific_combo:
            # Execute each key in the specific combo sequentially
            for key in specific_combo:
                if key:  # Skip empty strings
                    pyautogui.press(key)
        
        # Press enter to confirm the chart selection
        pyautogui.press('enter')
    else:
        print(f"No combo found for chart type: {chart_type}")
    
def execute_hotkey(hotkey, extra_args=None):
    """
    Presses a specific hotkey combination in Excel.
    
    Args:
        key (str): The hotkey combination to be executed (e.g., 'ctrl+c', 'alt+f4').
    """
    key = hotkey.split('+')
    pyautogui.hotkey(key)

def input_key(key, extra_args=None):
    """
    Inputs a key in Excel.
    
    Args:
        key (str): The key to be inputted. (e.g., 'enter', 'backspace')
    """
    pyautogui.press(key)

def drag_fill_cells(start_cell, direction, num_cells, extra_args=None):
    """
    Drags and fills cells in Excel from the starting cell to the ending cell.
    
    Args:
        start_cell (str): The address of the starting cell (e.g., 'A1', 'B3').
        direction (str): The direction of the fill (e.g., 'down', 'right').
        num_cells (int): The number of cells to fill.
    """
    pyautogui.hotkey('ctrl', 'g')  # Open the "Go To" dialog
    pyautogui.write(start_cell)  # Enter the cell address
    pyautogui.press('enter')  # Confirm the cell address

    pyautogui.keyDown('shiftleft')
    pyautogui.keyDown('shiftright')

    for _ in range(int(num_cells)):
        pyautogui.press(direction)
    
    pyautogui.keyUp('shiftleft')
    pyautogui.keyUp('shiftright')
    
    if direction == 'down':
        pyautogui.hotkey('ctrl', 'd')  # Fill down
    elif direction == 'right':
        pyautogui.hotkey('ctrl', 'r')  # Fill right
        
def enable_auto_filter(range_string=None, extra_args=None):
    """
    Enables the auto filter feature in Excel for selected range or complete sheet if no range passed.
    
    Args:
        range_string (str, optional): A string representing the range to apply auto filter.
                                      Example: 'A1:D10'. If not provided, applies to the entire sheet.
    """
    if range_string:
        # Use the Go To dialog to select the range
        pyautogui.hotkey('ctrl', 'g')  # Open the "Go To" dialog
        pyautogui.write(range_string)  # Enter the range
        pyautogui.press('enter')  # Confirm the selection
    else:
        # Move to the first cell to apply filter to the entire sheet
        pyautogui.hotkey('ctrl', 'home')  # Move to cell A1

    # Enable auto filter
    pyautogui.hotkey('ctrl', 'shift', 'l')  # Auto filter the selected range or entire sheet

    # If a range was specified, move back to A1 to avoid leaving the cursor in the filtered range
    if range_string:
        pyautogui.hotkey('ctrl', 'home')
    

def simple_sort(sort_order, sort_col, extra_args=None):
    """
    Sorts the selected range of cells in Excel.
    
    Args:
        sort_order (str): The sort order ('ascending' or 'descending').
        sort_col (str): The column to be sorted (e.g., 'A', 'B').
    """
    move_to_cell(sort_col + '1')  # Move to the specified column
    pyautogui.hotkey('alt', 'down')  # Open the filter dropdown
    if sort_order == 'ascending':
        pyautogui.press('down')  # Select "Sort A to Z"
    elif sort_order == 'descending':
        pyautogui.press('down')
        pyautogui.press('down')  # Select "Sort Z to A"
    pyautogui.press('enter')  # Confirm the sort order
    
def simple_filter(filter_col, filter_value, extra_args=None):
    """
    Filters the selected range of cells in Excel.
    
    Args:
        filter_col (str): The column to be filtered (e.g., 'A', 'B').
        filter_value (str): The value to be filtered.
    """
    move_to_cell(filter_col + '1')  # Move to the specified column
    pyautogui.hotkey('alt', 'down')  # Open the filter dropdown
    for _ in range(8):
        pyautogui.press('down')
    pyautogui.write(filter_value)  # Enter the filter value
    pyautogui.press('enter')  # Confirm the filter value

def run_predefined_macro(macro_name, extra_args=None):
    """
    Runs a prerecorded macro in Excel.
    
    Args:
        macro_name (str): The name of the macro to be executed.
    """
    pyautogui.hotkey('alt', 'f8')  # Open the "Macro" dialog
    pyautogui.write(macro_name)  # Enter the macro name
    pyautogui.press('enter')  # Confirm the macro name
    pyautogui.press('enter')  # Run the macro

def click_button(button_name, extra_args=None):
    """
    Clicks a button with the specified text in Microsoft Excel.
    If multiple buttons with the same text are found, it will click the first one.

    Args:
        button_name (str): The text displayed on the button to be clicked.
        extra_args (dict, optional): Additional arguments, such as 'temp_session_step_path' for retrieving the Excel process ID.
    """
    try:
        # Retrieve the Excel process ID, if provided
        if extra_args and 'temp_session_step_path' in extra_args:
            excel_pid = retrieve_excel_pid(extra_args['temp_session_step_path'])
            app = Application(backend="uia").connect(process=excel_pid)
        else:
            app = Application(backend="uia").connect(title_re=".*Microsoft Excel.*")

        # Find all buttons with the specified text
        window = app.top_window()
        buttons = window.children(title_re=f".*{button_name}.*")

        if buttons:
            # Click the first button found
            buttons[0].click()
        else:
            print(f"No button found with the text '{button_name}'")

    except Exception as e:
        print(f"Error clicking button '{button_name}': {e}")

