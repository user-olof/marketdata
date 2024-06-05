from pathlib import Path

def get_source_files(path: str):
    obj_path = Path(path)
    l = list()
    for it in obj_path.iterdir():
        l.append(it.name)
    return l
