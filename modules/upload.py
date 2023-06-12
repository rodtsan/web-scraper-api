from flask import Flask, abort, jsonify, request
from app import app
import os
from uuid import uuid4

__audio_formats = ["m4a", "mp3", "webm", "mp4", "mpga", "wav", "mpeg"]


@app.route("/api/audio/upload", methods=["POST"])
def audio_upload_func():
    if request.method == "POST":
        req_file = request.files['file']
        content_type = req_file.content_type
        ext = content_type.split("/").pop()
        if ext in __audio_formats:
            new_filename = f"{uuid4()}_{req_file.filename}"
            file_path = f"{os.getcwd()}/uploads/{new_filename}"
            req_file.save(file_path)
            return jsonify(
                {
                    "job_id": new_filename.split("_")[0],
                    "filename": new_filename,
                    "content_type": content_type,
                    "message": "Audio has been successfully uploaded",
                }
            )
        else:
            return jsonify({"error": "Unsupported audio type"}), 400
    abort(405)


__doc_formats = ["pdf", "docx", "xmlx", "txt"]


@app.route("/api/documents/upload", methods=["POST"])
def documents_upload_func():
    if request.method == "POST":
        file = request.files.get("file")
        ext = file.content_type.split("/").pop()
        if ext in __doc_formats:
            new_filename = f"{uuid4()}_{file.filename}"
            file.save(os.path.join(app.config["UPLOAD_DIR"], new_filename))
            return jsonify(
                {"message": f"Document has been successfully uploaded"}
            )
        else:
            return jsonify({"error": "Unsupported document type"}), 418
    abort(405)
