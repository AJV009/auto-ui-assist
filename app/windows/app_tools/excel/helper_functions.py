
import pyautogui
import time
import psutil
import os
from pywinauto import Application, Desktop

"""
Internal helper function
"""
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
    Launches Microsoft Excel.
    """
    pyautogui.hotkey('win', 'r')  # Open the Run dialog
    pyautogui.write('excel')  # Enter 'excel' to launch Excel
    pyautogui.press('enter')  # Confirm the launch
    time.sleep(5)  # Wait for Excel to open
    
    # Save the PID of the Excel process
    if extra_args:
        if 'temp_session_step_path' in extra_args:
            save_excel_pid(extra_args['temp_session_step_path'])

    pyautogui.press('enter')  # select empty workbook

def launch_excel_with_existing_workbook(file_name, extra_args=None):
    """
    Launches Microsoft Excel with an existing workbook.

    Args:
        file_name (str): A unique file name with the file extension.
    """
    pyautogui.hotkey('win', 'r')  # Open the Run dialog
    pyautogui.write('excel')  # Enter 'excel' to launch Excel
    pyautogui.press('enter')  # Confirm the launch
    time.sleep(5)  # Wait for Excel to open

    # Save the PID of the Excel process
    if extra_args:
        if 'temp_session_step_path' in extra_args:
            save_excel_pid(extra_args['temp_session_step_path'])

    pyautogui.hotkey('ctrl', 'o')  # Open an existing workbook
    pyautogui.press('enter') 
    pyautogui.press('enter') # double enter move to the search bar
    pyautogui.write(file_name)  # Enter the file name
    pyautogui.press('enter')  # Confirm the file name

# removed...
def open_blank_workbook(extra_args=None):
    """
    Opens a blank workbook in Excel.
    """
    pyautogui.hotkey('ctrl', 'n')  # Open a new workbook
    pyautogui.press('right') # Move to the "Blank workbook" option
    pyautogui.press('enter') # Confirm the selection

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

def select_range(start_cell, end_cell, extra_args=None):
    """
    Selects a range of cells in Excel.

    Args:
        start_cell (str): The address of the starting cell (e.g., 'A1', 'B3').
        end_cell (str): The address of the ending cell (e.g., 'C5', 'D10').
    """
    move_to_cell(start_cell)  # Move to the starting cell
    pyautogui.hotkey('shift', 'ctrl', 'g')  # Open the "Go To" dialog for range selection
    pyautogui.write(end_cell)  # Enter the ending cell address
    pyautogui.press('enter')  # Confirm the range selection

def create_table(extra_args=None):
    """
    Creates a table in Excel from the selected range of cells.
    """
    pyautogui.hotkey('ctrl', 't')
    pyautogui.press('enter')
    
def create_simple_chart(extra_args=None):
    """
    Creates a simple chart in Excel from the selected range of cells.
    """
    pyautogui.hotkey('alt', 'f1')  # Create a chart
    
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
        
def enable_auto_filter(extra_args=None):
    """
    Enables the autofilter option in Excel.
    Has to be called before using the filter/sort functions.
    """
    move_to_cell('A1')  # Move to the first cell
    pyautogui.hotkey('ctrl', 'shift', 'l')  # Auto filter the selected range
    

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

