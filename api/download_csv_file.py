# Import Libraries
# Define route "/" & "/<name>"
import os
from flask import Response, send_file
import pandas as pd


def download_csv_file(csv_file) -> Response:
    gzip_download_name = f"{csv_file}.zip"
    csv_filepath = f"{os.getcwd()}/files/embeddings/{csv_file}"
    zip_filepath = f"{os.getcwd()}/files/embeddings/{gzip_download_name}"
    # write a pandas dataframe to zipped CSV file
    if not os.path.isfile(zip_filepath):
        df = pd.read_csv(csv_filepath)
        df.to_csv(zip_filepath, index=False, compression="zip")

    return send_file(
        path_or_file=zip_filepath,
        mimetype="application/zip",
        download_name=gzip_download_name,
    )
