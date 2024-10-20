import importlib.resources


def get_file_path(file_name):
    base_path = importlib.resources.files("plotly_presentation")
    file_path = base_path.joinpath(f"_core/_defaults/{file_name}")
    return file_path
