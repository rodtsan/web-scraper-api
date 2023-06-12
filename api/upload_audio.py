from flask import Response, abort, json, request
import os
import time
import shortuuid as uuid
from pydub import AudioSegment

__audio_formats = ["m4a", "mp3", "webm", "mp4", "mpga", "wav", "mpeg"]


def upload_audio() -> Response:
    if request.method == "POST":
        file_id = uuid.ShortUUID().random(10)
        req_file = request.files["file"]
        content_type = req_file.content_type
        ext = content_type.split("/").pop()
        type = content_type.split("/")[0]
        new_filename = f"{file_id}_{req_file.filename}"
        new_filepath = f"{os.getcwd()}/files/uploads/{new_filename}"
        if ext in __audio_formats:
            req_file.save(new_filepath)
            return Response(
                json.dumps(
                    {
                        "job_id": new_filename.split("_")[0],
                        "filename": new_filename,
                        "content_type": content_type,
                        "message": "Audio has been successfully uploaded",
                    },
                    indent=4,
                ),
                200,
                mimetype="application/json",
            )
        else:
            if type == "audio":
                try:
                    dest_filename = "{}.wav".format(os.path.splitext(new_filename)[0])
                    dest_filepath = f"{os.getcwd()}/uploads/{dest_filename}"
                    time.sleep(5)
                    convert = AudioSegment.from_file(req_file)
                    convert.export(dest_filepath, format="wav")
                    return Response(
                        json.dumps(
                            {
                                "job_id": dest_filename.split("_")[0],
                                "filename": dest_filename,
                                "content_type": "audio/wav",
                                "message": "Audio has been successfully uploaded",
                            },
                            indent=4,
                        ),
                        200,
                        mimetype="application/json",
                    )
                except:
                    return Response(
                        json.dumps({"error": "Unsupported audio type"}),
                        400,
                        mimetype="application/json",
                    )

    abort(405)
