import time
import os
from uuid import uuid4
from flask import Response, abort, json, request
from pydub import AudioSegment

def convert_audio_to_wav() -> Response:
    if request.method == "POST":
        source_file = request.files["file"]
        ext = source_file.content_type.split("/").pop()
        if ext not in ["wav"]:
            source_filename = source_file.filename.split(".")[0]
            dest_filename = "{}.wav".format(source_filename)
            dest_filepath = f"{os.getcwd()}/files/temp/{dest_filename}"
            
            if not os.path.exists(dest_filepath):
                convert = AudioSegment.from_file(source_file)
                convert.export(dest_filepath, format="wav")
                time.sleep(4)
            
            print(dest_filename)   
            return Response(
                json.dumps(
                    {
                        "job_id": uuid4(),
                        "filename": dest_filename,
                        "content_type": "audio/wav",
                        "message": "Audio has been converted to wav",
                    },
                    indent=4,
                ),
                200,
                mimetype="application/json",
            )
        else:
            return Response(
                json.dumps({"error": "Audio is wav format"}),
                400,
                mimetype="application/json",
            )
    abort(405)
