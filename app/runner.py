import os

import csv, settings

def process_file(filename):
    file_path = os.path.join(
        settings.UPLOAD_FOLDER,
        filename
    )
    with open(file_path, "r") as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            print(row[0])
