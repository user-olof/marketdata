# import app.app as app
from app.import_csv import import_csv
from pathlib import Path
import os

def test_get_three_source_file_names():
    source_file_names = [
        "8TRA-2019-06-28-2024-04-30.csv",
        "ABB-1999-06-22-2024-04-30.csv",
        "ALFA-2002-05-17-2024-04-30.csv"
        ]
    base_dir = Path(__file__).parent.parent.absolute()
    print(base_dir)
    path = str(base_dir) + "/data/"
    print(path)
    csv_files = import_csv.get_source_files(path)
    res = all(f in csv_files for f in source_file_names)

    assert res == True


if __name__ == '__main__':
    test_get_three_source_file_names()




