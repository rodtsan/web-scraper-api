from flask import abort, jsonify, request
import openai
import os
from decouple import config
from app import app

openai.organization = config("OPENAI_API_ORG")
openai.api_key = config("OPENAI_API_KEY")

@app.route("/api/transcribe-audio-to-text")
def transcribe_audio_to_text():
    file_name = request.args.get("file")
    file_path = f"{os.getcwd()}/uploads/{file_name}"
    if os.path.exists(file_path):
        audio_file = open(file_path, "rb")
        transcript = openai.Audio.transcribe("whisper-1", audio_file)
        return jsonify(transcript)
    abort(400)
  
    
# file_path = f"{os.getcwd()}/temp/harvard.wav"
# audio_file = open(file_path, "rb")
# transcript = openai.Audio.transcribe("whisper-1", audio_file)