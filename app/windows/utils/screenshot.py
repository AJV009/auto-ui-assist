import base64
import re
import os
from io import BytesIO
from typing import Dict, List, Optional, Tuple, Union

from PIL import Image, ImageDraw, ImageFont
from pywinauto import Application
from pywinauto.controls.uiawrapper import UIAWrapper
from pywinauto.win32structures import RECT

def capture_screenshot(
    screenshot_type: str,
    app_title: Optional[str] = None,
    sub_control_titles: Optional[List[str]] = None,
    annotation_type: str = "number",
    color_diff: bool = True,
    color_default: str = "#FFF68F",
    rectangle_color: str = "red",
    rectangle_width: int = 3,
    output_format: str = "image",
    concat_images: Optional[List[str]] = None,
    temp_session_step_path: str = None,
) -> Union[Tuple[str, Dict[str, Tuple[int, int]]], str, None]:
    os.makedirs(temp_session_step_path, exist_ok=True)    

    def draw_rectangles(image: Image.Image, coordinate: tuple, color: str = "red", width: int = 3):
        draw = ImageDraw.Draw(image)
        draw.rectangle(coordinate, outline=color, width=width)
        return image

    def draw_rectangles_controls(image: Image.Image, coordinate: tuple, label_text: str, botton_margin: int = 5, border_width: int = 2, font_size: int = 25, font_color: str = "#000000", border_color: str = "#FF0000", button_color: str = "#FFF68F"):
        font = ImageFont.truetype("arial.ttf", font_size)
        text_size = font.getbbox(label_text)
        button_size = (text_size[2] + botton_margin, text_size[3] + botton_margin)
        button_img = Image.new("RGBA", button_size, button_color)
        button_draw = ImageDraw.Draw(button_img)
        button_draw.text((botton_margin / 2, botton_margin / 2), label_text, font=font, fill=font_color)
        ImageDraw.Draw(button_img).rectangle([(0, 0), (button_size[0] - 1, button_size[1] - 1)], outline=border_color, width=border_width)
        image.paste(button_img, (coordinate[0], coordinate[1]))
        return image

    def number_to_letter(n: int):
        if n < 0:
            return "Invalid input"
        result = ""
        while n >= 0:
            remainder = n % 26
            result = chr(65 + remainder) + result
            n = n // 26 - 1
            if n < 0:
                break
        return result

    def coordinate_adjusted(window_rect: RECT, control_rect: RECT):
        return (
            control_rect.left - window_rect.left,
            control_rect.top - window_rect.top,
            control_rect.right - window_rect.left,
            control_rect.bottom - window_rect.top,
        )

    def get_annotation_dict(sub_control_list: List[UIAWrapper], annotation_type: str) -> Dict[str, Tuple[UIAWrapper, Tuple[int, int]]]:
        annotation_dict = {}
        for i, control in enumerate(sub_control_list):
            label_text = str(i + 1) if annotation_type == "number" else number_to_letter(i)
            control_rect = control.rectangle()
            center_x = (control_rect.left + control_rect.right) // 2
            center_y = (control_rect.top + control_rect.bottom) // 2
            annotation_dict[label_text] = (control, (center_x, center_y))
        return annotation_dict

    def capture_control(control: UIAWrapper, save: bool = False):
        screenshot = control.capture_as_image()
        if save:
            screenshot.save(temp_session_step_path + "/" + "capture_control.png")
        return screenshot

    def concat_screenshots(image1_path: str, image2_path: str) -> Image.Image:
        image1 = Image.open(image1_path)
        image2 = Image.open(image2_path)
        min_height = min(image1.height, image2.height)
        image1 = image1.crop((0, 0, image1.width, min_height))
        image2 = image2.crop((0, 0, image2.width, min_height))
        result = Image.new("RGB", (image1.width + image2.width, min_height))
        result.paste(image1, (0, 0))
        result.paste(image2, (image1.width, 0))
        result.save(temp_session_step_path + "/" + "concat_screenshots.png")
        return result

    def image_to_base64(image: Image.Image) -> str:
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode("utf-8")
    
    def process_screenshot(screenshot, controls=None, window_rect=None, annotation_dict=None):
        coordinate_dict = {}
        if output_format == "rectangle" or output_format == "annotation" or output_format == "rectangle_annotation":
            for i, control in enumerate(controls):
                control_rect = control.rectangle()
                control_rect = coordinate_adjusted(window_rect, control_rect)

                if annotation_dict:
                    label_text = list(annotation_dict.keys())[i]
                else:
                    label_text = str(i + 1) if annotation_type == "number" else number_to_letter(i)

                if output_format == "rectangle" or output_format == "rectangle_annotation":
                    screenshot = draw_rectangles(screenshot, coordinate=control_rect, color=rectangle_color, width=rectangle_width)
                if output_format == "annotation" or output_format == "rectangle_annotation":
                    adjusted_coordinate = (control_rect[0], control_rect[1])
                    screenshot = draw_rectangles_controls(screenshot, adjusted_coordinate, label_text, button_color=color_default if not color_diff else "#FFF68F")
                center_x = control_rect[0] + (control_rect[2] - control_rect[0]) // 2
                center_y = control_rect[1] + (control_rect[3] - control_rect[1]) // 2
                coordinate_dict[label_text] = (center_x, center_y)
        return screenshot, coordinate_dict

    def application_screenshot():
        if not app_title:
            raise ValueError("app_title must be provided for app_window screenshot type.")
        app = Application(backend="uia").connect(title_re="(?i)" + app_title)
        window = app.window(title_re="(?i)" + app_title)
        control = window.wrapper_object()

        if sub_control_titles:
            sub_controls = [
                child
                for child in control.descendants()
                if any(re.search("(?i)" + re.escape(title), child.window_text()) for title in sub_control_titles)
            ]
        else:
            sub_controls = []

        screenshot = capture_control(control)
        window_rect = control.rectangle()
        annotation_dict = get_annotation_dict(sub_controls, annotation_type)
        screenshot, coordinate_dict = process_screenshot(screenshot, controls=sub_controls, window_rect=window_rect, annotation_dict=annotation_dict)
        return screenshot, coordinate_dict

    coordinate_dict = {}
    if screenshot_type == "app_window":
        screenshot, coordinate_dict = application_screenshot()
    elif screenshot_type == "concat":
        if not concat_images or len(concat_images) != 2:
            raise ValueError("concat_images must be a list of two image paths for concat screenshot type.")
        screenshot = concat_screenshots(concat_images[0], concat_images[1])
    else:
        raise ValueError("Invalid screenshot type")

    if output_format == "base64":
        return image_to_base64(screenshot), coordinate_dict
    else:
        screenshot_path = temp_session_step_path + "/" + "screenshot.png"
        screenshot.save(screenshot_path)
        return screenshot_path, coordinate_dict
