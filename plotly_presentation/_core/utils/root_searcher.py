import os
import importlib.resources

def find_git_root(path=os.getcwd()):
    venv = os.getenv('VIRTUAL_ENV')
    if venv:
        return venv
    current_path = path
    while current_path != os.path.dirname(
        current_path
    ):  # Stop when we reach the filesystem root
        if os.path.isdir(os.path.join(current_path, ".git")):
            return current_path
        current_path = os.path.dirname(current_path)
    return None

def get_file_path(file_name):
    base_path = importlib.resources.files('plotly_presentation')
    file_path = base_path.joinpath(f'_core/_defaults/{file_name}')
    return file_path
