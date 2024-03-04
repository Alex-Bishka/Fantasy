import os


def check_save_path(save_path):
    """
    Checks to see if a file already exists, so we avoid over-writing it
    """
    exists = os.path.exists(save_path)
    if exists:
        raise(FileExistsError(f"File '{save_path}' already exists! Please choose a different name for the file."))
        