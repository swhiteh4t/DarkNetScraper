import os, sys, json

def save_json(file_path):
    save_file(json.dumps(file_path,indent=4))
    
def join_path(file_directory, file_name):
    if file_directory == "":
        sys.exit(1)
    # Create data directory if it doesn't exist
    if not os.path.exists(file_directory):
        os.makedirs(file_directory)
    local_path = os.path.join(file_directory, file_name)

def save_file(file_path, data):
    with open(file_path, "w") as file:
        file.write(data)