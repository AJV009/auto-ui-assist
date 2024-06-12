import os
from io import BytesIO
import base64
import tempfile
import threading

def get_temp_path(app_name: str) -> str:
    return os.path.join(tempfile.gettempdir(), app_name)

def get_temp_session_path(app_temp_path: str, user_session_uuid: str) -> str:
    return os.path.join(app_temp_path, f"session-{user_session_uuid}")

def store_temp_file(file, file_path, app_temp_path):
    file_path = app_temp_path + "/" + file_path
    os.makedirs(file_path, exist_ok=True)
    with open(file_path, "wb") as f:
        f.write(file)

def get_input_with_timeout(prompt, timeout):
    user_input = None
    input_received = threading.Event()

    def input_handler():
        nonlocal user_input
        user_input = input(prompt)
        input_received.set()

    input_thread = threading.Thread(target=input_handler)
    input_thread.start()

    while not input_received.is_set():
        if not input_thread.is_alive():
            break
        input_received.wait(timeout)

    if user_input is None:
        print("\nInput timed out. Continuing with the default/existing/empty value.")
    else:
        input_thread.join()  # Allow the user to continue editing

    return user_input

def encode_image(image_path=None, IMAGE_object=None):
    if IMAGE_object:
        output = BytesIO()
        IMAGE_object.save(output, format='PNG')
        im_data = output.getvalue()
        return base64.b64encode(im_data).decode('utf-8')

    if image_path:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
