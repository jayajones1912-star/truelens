from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.secret_key = "replace-with-a-secure-key"

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "uploads")
ALLOWED_EXTENSIONS = {"mp4", "mov", "avi", "mkv"}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload_video():
    if "video" not in request.files:
        flash("No file part")
        return redirect(url_for("home"))

    video = request.files["video"]

    if video.filename == "":
        flash("No file selected")
        return redirect(url_for("home"))

    if video and allowed_file(video.filename):
        filename = secure_filename(video.filename)
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        video.save(filepath)

        # FAKE analysis (placeholder for your real model later)
        score = 72
        level = "Medium Risk"

        return render_template("result.html", score=score, level=level)

    flash("Invalid file type. Allowed types: mp4, mov, avi, mkv")
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)