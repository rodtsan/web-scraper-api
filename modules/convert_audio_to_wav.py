from uuid import uuid4
from flask import abort, jsonify, request
import os
from pydub import AudioSegment
from app import app

@app.route("/api/convert-audio-to-wav", methods=["POST"])
def convert_audio_to_wav():
        if request.method == "POST":
            source_file = request.files['file']
            ext = source_file.content_type.split("/").pop()
            print(ext)
            if ext not in ["wav"]:
                # file_path = os.path.join(app.config["TEMP_DIR"], convert_audio.filename)
                # audio_file.save(file_path)
                dest_file_name = source_file.filename.split(".")[0]
                dest_file_name = "{}.wav".format(dest_file_name)
                dest_file_dest = f"{os.getcwd()}/temp/{dest_file_name}"
                
                # convert {ext} to wav    
                convert = AudioSegment.from_file(source_file)
                convert.export(dest_file_dest, format="wav")
                return jsonify(
                    {
                        "job_id": dest_file_name.split("_")[0],
                        "filename": dest_file_name,
                        "message": "Audio has been converted to wav",
                    }
                )
            else:
                return jsonify({"error": "Audio is wav format"}), 400
        abort(405)
