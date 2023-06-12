from flask import Response, abort, json,request
import os
from uuid import uuid4

__doc_formats = ["pdf", "docx", "xmlx", "txt"]

def upload_doc()-> Response:
    if request.method == "POST":
        req_file = request.files["file"]
        content_type = req_file.content_type
        ext = content_type.split("/").pop()
        if ext in __doc_formats:
            new_filename = f"{uuid4()}_{req_file.filename}"
            new_filepath = f"{os.getcwd()}/files/uploads/{new_filename}"
            req_file.save(new_filepath)
            return Response(
                json.dumps(
                    {
                        "job_id": new_filename.split("_")[0],
                        "filename": new_filename,
                        "content_type": content_type,
                        "message": "Document has been successfully uploaded",
                    },
                    indent=4,
                ),
                200,
                mimetype="application/json",
            )
        else:
            return Response(
                json.dumps({"error": "Unsupported document type"}),
                400,
                mimetype="application/json",
            )
    abort(405)
