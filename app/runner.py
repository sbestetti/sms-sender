import os

import csv, settings

def process_file(filename):
    file_path = os.path.join(
        settings.UPLOAD_FOLDER,
        filename
    )

    print(file_path)
