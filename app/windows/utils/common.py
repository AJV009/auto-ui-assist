import os
import tempfile

def get_temp_path(app_name: str) -> str:
    return os.path.join(tempfile.gettempdir(), app_name)

def get_temp_session_path(app_temp_path: str, user_session_uuid: str) -> str:
    return os.path.join(app_temp_path, f"session-{user_session_uuid}")

def store_temp_file(file, file_path, app_temp_path):
    file_path = app_temp_path + "/" + file_path
    os.makedirs(file_path, exist_ok=True)
    with open(file_path, "wb") as f:
        f.write(file)
