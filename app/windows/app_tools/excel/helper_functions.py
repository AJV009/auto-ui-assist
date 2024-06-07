
import pyautogui

def launch_excel():
    """
    Launches Microsoft Excel.
    """
    pyautogui.hotkey('win', 'r')  # Open the Run dialog
    pyautogui.write('excel')  # Enter 'excel' to launch Excel
    pyautogui.press('enter')  # Confirm the launch
    
def open_blank_workbook():
    """
    Opens a blank workbook in Excel.
    """
    pyautogui.hotkey('ctrl', 'n')  # Open a new workbook
    pyautogui.press('right') # Move to the "Blank workbook" option
    pyautogui.press('enter') # Confirm the selection

def move_to_cell(cell_address):
    """
    Moves the cursor to a specific cell in Excel.

    Args:
        cell_address (str): The address of the cell (e.g., 'A1', 'B3').
    """
    pyautogui.press('esc')  # Ensure we're in normal mode
    pyautogui.hotkey('ctrl', 'g')  # Open the "Go To" dialog
    pyautogui.write(cell_address)  # Enter the cell address
    pyautogui.press('enter')  # Confirm the cell address

def input_data_in_cell(data):
    """
    Inputs data into the currently active cell in Excel.

    Args:
        data (str): The data to be entered into the cell.
    """
    pyautogui.write(data)
    pyautogui.press('enter')  # Confirm the data entry

def select_range(start_cell, end_cell):
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

def create_table():
    """
    Creates a table in Excel from the selected range of cells.
    """
    pyautogui.hotkey('ctrl', 't')
    pyautogui.press('enter')
    
def create_simple_chart():
    """
    Creates a simple chart in Excel from the selected range of cells.
    """
    pyautogui.hotkey('alt', 'f1')  # Create a chart

# def create_pivot_table():
#     """
#     Creates a pivot table in Excel from the selected range of cells.
#     """
#     pyautogui.hotkey('alt', 'n', 'v')  # Open the "Insert" menu and select "PivotTable"
#     pyautogui.press('enter')  # Confirm the selection