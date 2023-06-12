from flask import Response, abort, json, request
import openai
import os
import settings

openai.organization = settings.OPENAI_API_ORG
openai.api_key = settings.OPENAI_API_KEY


def transcribe_audio_to_text() -> Response:
    if request.method == "POST":
        filename = request.get_json()["file"]
        filepath = f"{os.getcwd()}/files/uploads/{filename}"
        if os.path.exists(filepath):
            audio_file = open(filepath, "rb")
            transcript = openai.Audio.transcribe("whisper-1", audio_file)
            return Response(
                json.dumps(transcript),
                200,
                mimetype="application/json",
            )
    abort(400)


# filepath = f"{os.getcwd()}/temp/harvard.wav"
# audio_file = open(file_path, "rb")
# transcript = openai.Audio.transcribe("whisper-1", audio_file)
