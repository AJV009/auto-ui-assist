import os
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
