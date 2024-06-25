# import os
# import json
# from datetime import datetime

# from utils.screenshot import capture_screenshot

# def test_capture_screenshot():
#     # Set the temporary session step path
#     temp_session_step_path = "temp_screenshots"
#     os.makedirs(temp_session_step_path, exist_ok=True)

#     # Create a dictionary to store all the coordinate dictionaries
#     coordinate_dicts = {}

#     # Test app window screenshot
#     temp_session_step_path_test = temp_session_step_path + "/test1"
#     app_window_ann_screenshot_path, app_window_coordinate_dict = capture_screenshot(
#         screenshot_type="app_window",
#         app_title="Excel",
#         # sub_control_titles=["New"],
#         # output_format="annotation",
#         temp_session_step_path=temp_session_step_path_test
#     )
#     assert os.path.exists(app_window_ann_screenshot_path), "App window screenshot file does not exist"
#     assert isinstance(app_window_coordinate_dict, dict), "App window coordinate dictionary is not a dictionary"
#     coordinate_dicts["app_window_ann"] = app_window_coordinate_dict

#     # # Test app window screenshot
#     # temp_session_step_path_test = temp_session_step_path + "/test2"
#     # app_window_rect_screenshot_path, app_window_coordinate_dict = capture_screenshot(
#     #     screenshot_type="app_window",
#     #     app_title="Excel",
#     #     sub_control_titles=["New"],
#     #     output_format="rectangle",
#     #     temp_session_step_path=temp_session_step_path_test
#     # )
#     # assert os.path.exists(app_window_rect_screenshot_path), "App window screenshot file does not exist"
#     # assert isinstance(app_window_coordinate_dict, dict), "App window coordinate dictionary is not a dictionary"
#     # coordinate_dicts["app_window_rect"] = app_window_coordinate_dict

#     # # Test app window screenshot with rectangle and annotation
#     # temp_session_step_path_test = temp_session_step_path + "/test3"
#     # app_window_rect_ann_screenshot_path, app_window_rect_ann_coordinate_dict = capture_screenshot(
#     #     screenshot_type="app_window",
#     #     app_title="Excel",
#     #     sub_control_titles=["New"],
#     #     output_format="rectangle_annotation",
#     #     temp_session_step_path=temp_session_step_path
#     # )
#     # assert os.path.exists(app_window_rect_ann_screenshot_path), "App window rectangle and annotation screenshot file does not exist"
#     # assert isinstance(app_window_rect_ann_coordinate_dict, dict), "App window rectangle and annotation coordinate dictionary is not a dictionary"
#     # coordinate_dicts["app_window_rect_ann"] = app_window_rect_ann_coordinate_dict

#     # # Test concatenating screenshots
#     # temp_session_step_path_test = temp_session_step_path + "/test4"
#     # concat_screenshot_path, _ = capture_screenshot(
#     #     screenshot_type="concat",
#     #     concat_images=[app_window_ann_screenshot_path, app_window_rect_screenshot_path],
#     #     temp_session_step_path=temp_session_step_path_test
#     # )
#     # assert os.path.exists(concat_screenshot_path), "Concatenated screenshot file does not exist"

#     # # Test different annotation types
#     # temp_session_step_path_test = temp_session_step_path + "/test5"
#     # app_window_number_ann_screenshot_path, _ = capture_screenshot(
#     #     screenshot_type="app_window",
#     #     app_title="Excel",
#     #     sub_control_titles=["New"],
#     #     annotation_type="number",
#     #     output_format="annotation",
#     #     temp_session_step_path=temp_session_step_path_test
#     # )
#     # assert os.path.exists(app_window_number_ann_screenshot_path), "App window number annotation screenshot file does not exist"

#     # temp_session_step_path_test = temp_session_step_path + "/test6"
#     # app_window_letter_ann_screenshot_path, _ = capture_screenshot(
#     #     screenshot_type="app_window",
#     #     app_title="Excel",
#     #     sub_control_titles=["New"],
#     #     annotation_type="letter",
#     #     output_format="annotation",
#     #     temp_session_step_path=temp_session_step_path_test
#     # )
#     # assert os.path.exists(app_window_letter_ann_screenshot_path), "App window letter annotation screenshot file does not exist"

#     # # Test different color schemes
#     # temp_session_step_path_test = temp_session_step_path + "/test7"
#     # app_window_color_diff_screenshot_path, _ = capture_screenshot(
#     #     screenshot_type="app_window",
#     #     app_title="Excel",
#     #     sub_control_titles=["New"],
#     #     color_diff=True,
#     #     output_format="annotation",
#     #     temp_session_step_path=temp_session_step_path_test
#     # )
#     # assert os.path.exists(app_window_color_diff_screenshot_path), "App window color differentiation screenshot file does not exist"

#     # temp_session_step_path_test = temp_session_step_path + "/test8"
#     # app_window_color_default_screenshot_path, _ = capture_screenshot(
#     #     screenshot_type="app_window",
#     #     app_title="Excel",
#     #     sub_control_titles=["New"],
#     #     color_diff=False,
#     #     color_default="#FFFFFF",
#     #     output_format="annotation",
#     #     temp_session_step_path=temp_session_step_path_test
#     # )
#     # assert os.path.exists(app_window_color_default_screenshot_path), "App window default color screenshot file does not exist"

#     # Generate a unique filename for the JSON file
#     timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#     json_filename = f"coordinate_dicts_{timestamp}.json"
#     json_filepath = os.path.join(temp_session_step_path, json_filename)

#     # Write the coordinate dictionaries to a JSON file
#     with open(json_filepath, "w") as json_file:
#         json.dump(coordinate_dicts, json_file, indent=4)

#     print(f"Coordinate dictionaries saved to: {json_filepath}")
#     print("All tests passed!")

# # Run the test
# test_capture_screenshot()

# from utils.control import execute_action

# import json

# def process_actions(step_list):
#     for step in step_list:
#         step_name, step_details = list(step.items())[0]
#         action_details = step_details.split("\n")
        
#         action = {}
#         for detail in action_details:
#             detail.replace("\"", "")
#             if ":" in detail:
#                 key, value = detail.split(":", 1)
#                 key = key.strip().strip('"')
#                 value = value.strip().strip('"')
                
#                 if key == "action_type":
#                     action[key] = value
#                 elif key == "parameters":
#                     parameters = json.loads(value)
#                     action[key] = parameters
#                 elif key == "text":
#                     action["action_type"] = "PRESS"
#                     key = "keys"
#                     # convert text to list of characters
#                     action.setdefault("parameters", {})[key] = list(json.loads(value)[0])
#                 elif key == "keys":
#                     action["action_type"] = "PRESS"
#                     action.setdefault("parameters", {})[key] = json.loads(value)
        
#         print(f"Executing step: {step_name}")
#         print(action)
#         execute_action(action)

# # Example usage
# step_list = [
#     # {
#     #     "step_1": "\"action_desc\": \"Select cell A1\"\n\"action_type\": \"CLICK\",\n\"parameters\": {\"cell\": \"A1\"}"
#     # },
#     {
#         "step_2": "\"action_desc\": \"Enter 'Name' in cell A1\"\n\"action_type\": \"PRESS\",\n\"text\": [\"Name\"]"
#     },
#     {
#         "step_3": "\"action_desc\": \"Move to cell B1\"\n\"action_type\": \"PRESS\",\n\"keys\": [\"right\"]"
#     },
#     {
#         "step_4": "\"action_desc\": \"Enter 'Age' in cell B1\"\n\"action_type\": \"PRESS\",\n\"text\": [\"Age\"]"
#     },
#     {
#         "step_5": "\"action_desc\": \"Move to cell C1\"\n\"action_type\": \"PRESS\",\n\"keys\": [\"right\"]"
#     },
#     {
#         "step_6": "\"action_desc\": \"Enter 'City' in cell C1\"\n\"action_type\": \"PRESS\",\n\"text\": [\"City\"]"
#     }
# ]

# process_actions(step_list)

import openpyxl
import pyautogui
import time
import datetime
import psutil
import os
from pywinauto import Application

# def create_test_workbooks():
#     # Create a workbook with some data already saved on disk
#     wb1 = openpyxl.Workbook()
#     ws1 = wb1.active
#     ws1['A1'] = 'Test Data 1'
#     saved_workbook_path = os.path.abspath('saved_workbook.xlsx')
#     wb1.save(saved_workbook_path)

#     # Create a workbook with some data but never saved yet
#     wb2 = openpyxl.Workbook()
#     ws2 = wb2.active
#     ws2['A1'] = 'Test Data 2'
#     unsaved_workbook_path = os.path.abspath('unsaved_workbook.xlsx')  # This file will not be saved

#     return saved_workbook_path

def close_and_save_excel():
    """
    Close all open Excel files, saving them with a timestamp if they are new.
    """
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] == 'EXCEL.EXE':
            try:
                app = Application().connect(process=proc.pid)
                window = app.top_window()
                window.set_focus()
                
                # Close the window using Alt+F4
                pyautogui.hotkey('alt', 'f4')
                time.sleep(1)
                
                # Check if there's an unsaved workbook dialog
                try:
                    while True:
                        pyautogui.press('enter')  # Confirm to save changes
                        time.sleep(1)
                        
                        # Handle save as dialog if it appears
                        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
                        pyautogui.write(timestamp)  # Write the timestamp as the file name
                        pyautogui.press('enter')  # Save the file with the timestamp
                        time.sleep(1)
                except:
                    pass  # No more dialogs to handle
            except Exception as e:
                print(f"Could not connect to process {proc.pid}: {e}")

# def launch_excel_new_workbook():
#     """
#     Launches Microsoft Excel with a new workbook.
#     """
#     # close_and_save_excel()  # Close any open Excel files and save them
#     pyautogui.hotkey('win', 'r')  # Open the Run dialog
#     pyautogui.write('excel')  # Enter 'excel' to launch Excel
#     pyautogui.press('enter')  # Confirm the launch
#     time.sleep(5)  # Wait for Excel to open
#     pyautogui.press('enter')  # Select an empty workbook

# def launch_excel_existing_workbook(file_path):
#     """
#     Launches Microsoft Excel with an existing workbook using the full file path.

#     Args:
#         file_path (str): The full path to the file.
#     """
#     close_and_save_excel()  # Close any open Excel files and save them
#     pyautogui.hotkey('win', 'r')  # Open the Run dialog
#     pyautogui.write(f'excel "{file_path}"')  # Enter the full path to launch Excel with the file
#     pyautogui.press('enter')  # Confirm the launch
#     time.sleep(5)  # Wait for Excel to open

# # Create the test workbooks
# print("1. Creating test workbooks...")
# saved_workbook_path = create_test_workbooks()
# print(f"2. Saved workbook path: {saved_workbook_path}")

# # Launch Excel with the saved workbook using the full path
# print("3. Launching Excel with the saved workbook...")
# launch_excel_existing_workbook(saved_workbook_path)
# print("4. Launched Excel with the saved workbook")

# # Wait a bit before launching the unsaved workbook
# print("5. Waiting 10 seconds before launching the unsaved workbook...")
# time.sleep(10)
# print("6. Launching Excel with the unsaved workbook...")

# # Launch Excel with a new unsaved workbook
# print("7. Launching Excel with a new workbook...")
# launch_excel_new_workbook()
# print("8. Launched Excel with a new workbook")

# # Test closing and saving workbooks
# print("9. Waiting 10 seconds before closing Excel...")
# time.sleep(10)
print("10. Closing Excel...")
close_and_save_excel()
print("11. Closed Excel")
