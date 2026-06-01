from flask import Flask, send_from_directory
from flask_restful import Api
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from datetime import timedelta
import os

from backend.auth import Register, Login
from backend.documents import UploadDoc, GetUserDocs
from backend.admin import GetAllDocs, VerifyDoc, DownloadDoc

app = Flask(
    __name__,
    static_folder="../frontend",
    template_folder="../frontend"
)

CORS(app)

# JWT Configuration
app.config["JWT_SECRET_KEY"] = "docverify_secret_key"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=5)

jwt = JWTManager(app)

# Upload Folder Configuration
UPLOAD_FOLDER = os.path.join(
    os.path.dirname(__file__),
    "uploads"
)

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Flask RESTful API
api = Api(app)

# Frontend Route
@app.route("/")
def home():
    return send_from_directory(
        "../frontend",
        "login.html"
    )

# API Routes
api.add_resource(Register, "/register")

api.add_resource(Login, "/login")

api.add_resource(UploadDoc, "/upload")

api.add_resource(GetUserDocs, "/documents")

api.add_resource(GetAllDocs, "/all-documents")

api.add_resource(VerifyDoc, "/verify")

api.add_resource(
    DownloadDoc,
    "/download/<int:docid>"
)

if __name__ == "__main__":
    app.run(
        host="localhost",
        port=5000,
        debug=True
    )