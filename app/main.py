import win32com.client
import os
import json
import os
import subprocess
from difflib import SequenceMatcher

# test code for creating directory structure and launching applications
def find_approx_app(app_directory, search_text, threshold=0.8):
    results = []

    def traverse_directory(directory, path):
        for key, value in directory.items():
            if value is None:
                similarity = SequenceMatcher(None, search_text, key).ratio()
                if similarity >= threshold:
                    results.append((path + [key], similarity))
            else:
                traverse_directory(value, path + [key])

    traverse_directory(app_directory, [])

    if results:
        best_match = max(results, key=lambda x: x[1])
        return best_match[0]
    else:
        return None

def get_special_folder_path(folder_name):
    import win32com.client
    shell = win32com.client.Dispatch("WScript.Shell")
    return shell.SpecialFolders(folder_name)

def launch_application(app_path):
    try:
        if app_path.lower().endswith(".lnk"):
            shell = win32com.client.Dispatch("WScript.Shell")
            shortcut = shell.CreateShortcut(app_path)
            target_path = shortcut.Targetpath
            subprocess.Popen(target_path)
            print(f"Launched application: {target_path}")
        else:
            subprocess.Popen(app_path)
            print(f"Launched application: {app_path}")
    except FileNotFoundError:
        print(f"Application not found: {app_path}")
    except Exception as e:
        print(f"Error launching application: {str(e)}")

def create_directory_structure(directory):
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

if __name__ == "__main__":
    objShell = win32com.client.Dispatch("WScript.Shell")
    
    # All Users Programs menu
    allUserProgramsMenu = objShell.SpecialFolders("AllUsersPrograms")
    
    # User Start Menu
    userMenu = objShell.SpecialFolders("StartMenu")
    
    # All Users Desktop
    allDesktop = objShell.SpecialFolders("AllUsersDesktop")
    
    # Create the directory structure for each folder
    allUserProgramsStructure = create_directory_structure(allUserProgramsMenu)
    userMenuStructure = create_directory_structure(userMenu)
    allDesktopStructure = create_directory_structure(allDesktop)
    
    # Combine the structures into a single dictionary
    applicationDirectory = {
        "AllUsersPrograms": allUserProgramsStructure,
        "StartMenu": userMenuStructure,
        "AllUsersDesktop": allDesktopStructure
    }
    
    # pretty print applicationDirectory
    print(json.dumps(applicationDirectory, indent=2))
    # dump to a json file
    with open("application_directory.json", "w") as f:
        json.dump(applicationDirectory, f, indent=2)

    search_text = "Microsoft Edge"
    best_match = find_approx_app(applicationDirectory, search_text)

    if best_match:
        root_folder = best_match[0]
        relative_path = os.path.join(*best_match[1:])

        if root_folder == "AllUsersPrograms":
            base_path = get_special_folder_path("AllUsersPrograms")
        elif root_folder == "StartMenu":
            base_path = get_special_folder_path("StartMenu")
        elif root_folder == "AllUsersDesktop":
            base_path = get_special_folder_path("AllUsersDesktop")
        else:
            print(f"Unknown root folder: {root_folder}")
            exit(1)

        app_path = os.path.join(base_path, relative_path)
        launch_application(app_path)
    else:
        print(f"No application found similar to '{search_text}'")
