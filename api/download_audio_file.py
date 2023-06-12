# Import Libraries
# Define route "/" & "/<name>"
import os
from flask import Response, send_file
import pandas as pd


def download_audio_file(audio_file) -> Response:
    audio_filepath = f"{os.getcwd()}/files/temp/{audio_file}"
    ext = audio_file.split(".").pop()
    # write a pandas dataframe to zipped CSV file
    return send_file(
        path_or_file=audio_filepath,
        mimetype=f"audio/{ext}",
        download_name=audio_file,
    )
