import os


def list_dir(dirpath: str) -> list:
    '''List filepaths from a directory'''
    with os.scandir(dirpath) as entries:
        return [(entry.name, entry.path) for entry in entries if entry.is_file()]


def read_file(filepath: str) -> str:
    '''Read contents of a file'''
    with open(filepath, 'r') as f:
        return f.read()
