import os
import uuid

def get_userid(app_temp_path):
    '''
    a uniqueid will be stored in tempfile as "user-id_<uuid>" no extensions, nothing
    check if user has such a file, then extract its uuid from it and return it
    if the user doesn't have such a file, create one and then return the uuid
    '''
    user_id_file = None
    for file in os.listdir(app_temp_path):
        if file.startswith("user-id_"):
            user_id_file = file
            break
    if user_id_file:
        return user_id_file.split("_")[1]
    user_id = str(uuid.uuid4())
    with open(os.path.join(app_temp_path, f"user-id_{user_id}"), "w") as f:
        f.write("")
    return user_id
