import os
import json
from datetime import datetime

from utils.screenshot import capture_screenshot

def test_capture_screenshot():
    # Set the temporary session step path
    temp_session_step_path = "temp_screenshots"
    os.makedirs(temp_session_step_path, exist_ok=True)

    # Create a dictionary to store all the coordinate dictionaries
    coordinate_dicts = {}

    # Test app window screenshot
    temp_session_step_path_test = temp_session_step_path + "/test1"
    app_window_ann_screenshot_path, app_window_coordinate_dict = capture_screenshot(
        screenshot_type="app_window",
        app_title="Excel",
        # sub_control_titles=["New"],
        # output_format="annotation",
        temp_session_step_path=temp_session_step_path_test
    )
    assert os.path.exists(app_window_ann_screenshot_path), "App window screenshot file does not exist"
    assert isinstance(app_window_coordinate_dict, dict), "App window coordinate dictionary is not a dictionary"
    coordinate_dicts["app_window_ann"] = app_window_coordinate_dict

    # # Test app window screenshot
    # temp_session_step_path_test = temp_session_step_path + "/test2"
    # app_window_rect_screenshot_path, app_window_coordinate_dict = capture_screenshot(
    #     screenshot_type="app_window",
    #     app_title="Excel",
    #     sub_control_titles=["New"],
    #     output_format="rectangle",
    #     temp_session_step_path=temp_session_step_path_test
    # )
    # assert os.path.exists(app_window_rect_screenshot_path), "App window screenshot file does not exist"
    # assert isinstance(app_window_coordinate_dict, dict), "App window coordinate dictionary is not a dictionary"
    # coordinate_dicts["app_window_rect"] = app_window_coordinate_dict

    # # Test app window screenshot with rectangle and annotation
    # temp_session_step_path_test = temp_session_step_path + "/test3"
    # app_window_rect_ann_screenshot_path, app_window_rect_ann_coordinate_dict = capture_screenshot(
    #     screenshot_type="app_window",
    #     app_title="Excel",
    #     sub_control_titles=["New"],
    #     output_format="rectangle_annotation",
    #     temp_session_step_path=temp_session_step_path
    # )
    # assert os.path.exists(app_window_rect_ann_screenshot_path), "App window rectangle and annotation screenshot file does not exist"
    # assert isinstance(app_window_rect_ann_coordinate_dict, dict), "App window rectangle and annotation coordinate dictionary is not a dictionary"
    # coordinate_dicts["app_window_rect_ann"] = app_window_rect_ann_coordinate_dict

    # # Test concatenating screenshots
    # temp_session_step_path_test = temp_session_step_path + "/test4"
    # concat_screenshot_path, _ = capture_screenshot(
    #     screenshot_type="concat",
    #     concat_images=[app_window_ann_screenshot_path, app_window_rect_screenshot_path],
    #     temp_session_step_path=temp_session_step_path_test
    # )
    # assert os.path.exists(concat_screenshot_path), "Concatenated screenshot file does not exist"

    # # Test different annotation types
    # temp_session_step_path_test = temp_session_step_path + "/test5"
    # app_window_number_ann_screenshot_path, _ = capture_screenshot(
    #     screenshot_type="app_window",
    #     app_title="Excel",
    #     sub_control_titles=["New"],
    #     annotation_type="number",
    #     output_format="annotation",
    #     temp_session_step_path=temp_session_step_path_test
    # )
    # assert os.path.exists(app_window_number_ann_screenshot_path), "App window number annotation screenshot file does not exist"

    # temp_session_step_path_test = temp_session_step_path + "/test6"
    # app_window_letter_ann_screenshot_path, _ = capture_screenshot(
    #     screenshot_type="app_window",
    #     app_title="Excel",
    #     sub_control_titles=["New"],
    #     annotation_type="letter",
    #     output_format="annotation",
    #     temp_session_step_path=temp_session_step_path_test
    # )
    # assert os.path.exists(app_window_letter_ann_screenshot_path), "App window letter annotation screenshot file does not exist"

    # # Test different color schemes
    # temp_session_step_path_test = temp_session_step_path + "/test7"
    # app_window_color_diff_screenshot_path, _ = capture_screenshot(
    #     screenshot_type="app_window",
    #     app_title="Excel",
    #     sub_control_titles=["New"],
    #     color_diff=True,
    #     output_format="annotation",
    #     temp_session_step_path=temp_session_step_path_test
    # )
    # assert os.path.exists(app_window_color_diff_screenshot_path), "App window color differentiation screenshot file does not exist"

    # temp_session_step_path_test = temp_session_step_path + "/test8"
    # app_window_color_default_screenshot_path, _ = capture_screenshot(
    #     screenshot_type="app_window",
    #     app_title="Excel",
    #     sub_control_titles=["New"],
    #     color_diff=False,
    #     color_default="#FFFFFF",
    #     output_format="annotation",
    #     temp_session_step_path=temp_session_step_path_test
    # )
    # assert os.path.exists(app_window_color_default_screenshot_path), "App window default color screenshot file does not exist"

    # Generate a unique filename for the JSON file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    json_filename = f"coordinate_dicts_{timestamp}.json"
    json_filepath = os.path.join(temp_session_step_path, json_filename)

    # Write the coordinate dictionaries to a JSON file
    with open(json_filepath, "w") as json_file:
        json.dump(coordinate_dicts, json_file, indent=4)

    print(f"Coordinate dictionaries saved to: {json_filepath}")
    print("All tests passed!")

# Run the test
test_capture_screenshot()
