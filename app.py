# Import Libraries 
import os
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

# Define app.
app = Flask(__name__, static_folder="temp")
CORS(app)

db_path = os.path.abspath(os.getcwd())
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///{}\sm_db.db".format(db_path)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["UPLOAD_DIR"] = "uploads"
app.config["TEMP_DIR"] = "temp"
db = SQLAlchemy(app)

# linkedin_bp = Blueprint('linkedin_blueprint', __name__,
#                         template_folder='templates')

# app.register_blueprint(linkedin_bp, url_prefix="/api/linkedin")

from modules import *
from modules.linkedin import *

