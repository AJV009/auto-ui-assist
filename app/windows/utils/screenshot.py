import base64
from io import BytesIO
from typing import Dict, List, Optional, Union
from PIL import Image, ImageDraw, ImageFont, ImageGrab
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
    all_screens: bool = True,
    save_path: Optional[str] = None,
    output_format: str = "image",
    concat_images: Optional[List[str]] = None
) -> Union[Image.Image, str, None]:

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

    def get_annotation_dict(sub_control_list: List[UIAWrapper], annotation_type: str) -> Dict[str, UIAWrapper]:
        annotation_dict = {}
        for i, control in enumerate(sub_control_list):
            label_text = str(i + 1) if annotation_type == "number" else number_to_letter(i)
            annotation_dict[label_text] = control
        return annotation_dict

    def capture_control(control: UIAWrapper, save_path: Optional[str] = None):
        screenshot = control.capture_as_image()
        if save_path:
            screenshot.save(save_path)
        return screenshot

    def capture_desktop(all_screens=True, save_path: Optional[str] = None):
        screenshot = ImageGrab.grab(all_screens=all_screens)
        if save_path:
            screenshot.save(save_path)
        return screenshot

    def concat_screenshots(image1_path: str, image2_path: str, output_path: str) -> Image.Image:
        image1 = Image.open(image1_path)
        image2 = Image.open(image2_path)
        min_height = min(image1.height, image2.height)
        image1 = image1.crop((0, 0, image1.width, min_height))
        image2 = image2.crop((0, 0, image2.width, min_height))
        result = Image.new("RGB", (image1.width + image2.width, min_height))
        result.paste(image1, (0, 0))
        result.paste(image2, (image1.width, 0))
        result.save(output_path)
        return result

    def image_to_base64(image: Image.Image) -> str:
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode("utf-8")

    if screenshot_type == "desktop":
        screenshot = capture_desktop(all_screens=all_screens, save_path=save_path)
    elif screenshot_type == "app_window":
        if not app_title:
            raise ValueError("app_title must be provided for app_window screenshot type.")
        app = Application(backend="uia").connect(title_re=app_title)
        window = app.window(title_re=app_title)
        control = window.wrapper_object()

        if sub_control_titles:
            sub_controls = [child for child in control.descendants() if any(title in child.window_text() for title in sub_control_titles)]
        else:
            sub_controls = []

        if output_format == "rectangle":
            screenshot = capture_control(control)
            window_rect = control.rectangle()
            for sub_control in sub_controls:
                control_rect = sub_control.rectangle()
                adjusted_rect = coordinate_adjusted(window_rect, control_rect)
                screenshot = draw_rectangles(screenshot, coordinate=adjusted_rect, color=rectangle_color, width=rectangle_width)
            if save_path:
                screenshot.save(save_path)
        elif output_format == "annotation":
            screenshot = capture_control(control)
            window_rect = control.rectangle()
            annotation_dict = get_annotation_dict(sub_controls, annotation_type)
            for label_text, sub_control in annotation_dict.items():
                control_rect = sub_control.rectangle()
                adjusted_rect = coordinate_adjusted(window_rect, control_rect)
                adjusted_coordinate = (adjusted_rect[0], adjusted_rect[1])
                screenshot = draw_rectangles_controls(screenshot, adjusted_coordinate, label_text, button_color=color_default if not color_diff else "#FFF68F")
            if save_path:
                screenshot.save(save_path)
        else:
            screenshot = capture_control(control, save_path=save_path)
    elif screenshot_type == "concat":
        if not concat_images or len(concat_images) != 2:
            raise ValueError("concat_images must be a list of two image paths for concat screenshot type.")
        screenshot = concat_screenshots(concat_images[0], concat_images[1], save_path)
    else:
        raise ValueError("Invalid screenshot type")

    if output_format == "base64":
        return image_to_base64(screenshot)
    return screenshot
