import os


def find_git_root(path=os.getcwd()):
    current_path = path
    while current_path != os.path.dirname(
        current_path
    ):  # Stop when we reach the filesystem root
        if os.path.isdir(os.path.join(current_path, ".git")):
            return current_path
        current_path = os.path.dirname(current_path)
    return None
