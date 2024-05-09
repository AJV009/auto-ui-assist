import win32com.client
import os
import json
import tempfile

def app_list(uuid, fetch_old=False):
    """
    List all applications in the system.
    """
    app_temp_dir = os.path.join(tempfile.gettempdir(), "my_app")
    os.makedirs(app_temp_dir, exist_ok=True)
    app_list_file = os.path.join(app_temp_dir, f"{uuid}_app_list.json")

    if fetch_old:
        old_app_list = app_list_backup(app_list_file)
        if old_app_list:
            return old_app_list

    specialDirectories = ["AllUsersPrograms", "StartMenu", "AllUsersDesktop"]
    objShell = win32com.client.Dispatch("WScript.Shell")

    completeApplicationDirectory = {}
    for directory in specialDirectories:
        completeApplicationDirectory[directory] = create_directory_structure(objShell.SpecialFolders(directory))

    app_list_backup(app_list_file, completeApplicationDirectory)
    return completeApplicationDirectory

def app_list_backup(app_list_file, completeApplicationDirectory=None):
    '''
    Backup the application list to a json file
    '''
    if completeApplicationDirectory:
        with open(app_list_file, "w") as f:
            f.write(json.dumps(completeApplicationDirectory))
        return None
    else:
        try:
            with open(app_list_file, "r") as f:
                return json.loads(f.read())
        except FileNotFoundError:
            return None

def create_directory_structure(directory):
    '''
    Create a dictionary structure of the directory
    '''
    structure = {}
    for root, dirs, files in os.walk(directory):
        current_level = structure
        folders = root.replace(directory, "").split(os.sep)
        for folder in folders:
            if folder != "":
                if folder not in current_level:
                    current_level[folder] = {}
                current_level = current_level[folder]

        for file in files:
            if file.lower().endswith((".lnk", ".exe", ".url")):
                current_level[file] = None

    return structure