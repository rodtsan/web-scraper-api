from app import app
from flask import send_from_directory


@app.route('/pdf/<path:filename>', methods=['GET', 'POST'])
def download(filename):    
    return send_from_directory(directory='uploads', filename=filename)