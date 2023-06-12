# Import Libraries
from flask import Blueprint
from .index import *
from .convert_audio_to_wav import *
from .transcribe_audio_to_text import *
from .upload_doc import *
from .upload_audio import *
from .download_csv_file import *
from .download_audio_file import *

bp = Blueprint("api", __name__, url_prefix="/api")

bp.add_url_rule("/", "main", index)
bp.add_url_rule("/hc", "main", index)

bp.add_url_rule(
    "/convert_audio_to_wav",
    "convert_audio_to_wav",
    convert_audio_to_wav,
    methods=["POST"],
)

bp.add_url_rule("/download_csv_zip/<csv_file>", "download_csv_zip", download_csv_file)

bp.add_url_rule("/download_audio_file/<audio_file>", "audio_file", download_audio_file)

bp.add_url_rule(
    "/transcribe_audio_to_text",
    "transcribe_audio_to_text",
    transcribe_audio_to_text,
    methods=["POST"],
)

bp.add_url_rule(
    "/upload_doc",
    "upload_doc",
    upload_doc,
    methods=["POST"],
)

bp.add_url_rule(
    "/upload_audio",
    "upload_audio",
    upload_audio,
    methods=["POST"],
)
