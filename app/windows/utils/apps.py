import win32com.client
import os
import json
import tempfile
import subprocess
from difflib import SequenceMatcher

specialDirectories = ["AllUsersPrograms", "StartMenu", "AllUsersDesktop"]

def app_list(uuid, fetch_old=False):
    """
    List all applications in the system.
    """
    app_temp_dir = os.path.join(tempfile.gettempdir(), "autoUIAssist")
    os.makedirs(app_temp_dir, exist_ok=True)
    app_list_file = os.path.join(app_temp_dir, f"{uuid}_app_list.json")

    if fetch_old:
        old_app_list = app_list_backup(app_list_file)
        if old_app_list:
            return old_app_list

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

def launch_app(uuid, app_name):
    '''
    Launch the application
    '''
    app_directory = app_list(uuid, fetch_old=True)
    
    # Find the best match
    results = []
    threshold = 0.8
    def traverse_directory(directory, path):
        for key, value in directory.items():
            if value is None:
                similarity = SequenceMatcher(None, app_name, key).ratio()
                if similarity >= threshold:
                    results.append((path + [key], similarity))
            else:
                traverse_directory(value, path + [key])
    traverse_directory(app_directory, [])
    if results:
        best_match = max(results, key=lambda x: x[1])
        app_dir_match = best_match[0]
        root_folder = app_dir_match[0]
        relative_path = os.path.join(*app_dir_match[1:])
        if root_folder in specialDirectories:
            shell = win32com.client.Dispatch("WScript.Shell")
            base_path = shell.SpecialFolders(root_folder)
            app_path = os.path.join(base_path, relative_path)
            try:
                if app_path.lower().endswith(".lnk"):
                    shell = win32com.client.Dispatch("WScript.Shell")
                    shortcut = shell.CreateShortcut(app_path)
                    target_path = shortcut.Targetpath
                    subprocess.Popen(target_path)
                    return {"success": f"Launched application: {target_path}"}
                else:
                    subprocess.Popen(app_path)
                    return {"success": f"Launched application: {app_path}"}
            except FileNotFoundError:
                return {"error": f"Application not found: {app_path}"}
            except Exception as e:
                return {"error": f"Error launching application: {str(e)}"}
        else:
            return {"error": "No similar application to launch found"}
    else:
        return {"error": "No similar application to launch found"}

def office_app_list(os_apps):
    '''
    Select the office application
    '''
    office_apps = ["excel", "powerpoint", "word"]
    for app in os_apps:
        for office_app in office_apps:
            if office_app in app.lower():
                return app, office_app
    return None
