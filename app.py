import os
import uuid
import time
from flask import Flask, render_template, request, send_from_directory, session
from rembg import remove
from PIL import Image
from werkzeug.utils import secure_filename

# ---------------- CONFIG ----------------
app = Flask(__name__)
app.secret_key = "change-this-secret-key"

UPLOAD_FOLDER = "static/uploads"
RESULT_FOLDER = "static/results"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

# Auto delete files older than (seconds)
FILE_EXPIRE_TIME = 60 * 10   # 10 minutes

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

# ---------------- HELPERS ----------------
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def cleanup_old_files(folder, max_age):
    """Delete files older than max_age seconds"""
    now = time.time()
    for file in os.listdir(folder):
        path = os.path.join(folder, file)
        if os.path.isfile(path):
            if now - os.path.getmtime(path) > max_age:
                try:
                    os.remove(path)
                except Exception:
                    pass


# ---------------- ROUTES ----------------
@app.route("/", methods=["GET", "POST"])
def index():
    # 🔥 Cleanup on every request
    cleanup_old_files(UPLOAD_FOLDER, FILE_EXPIRE_TIME)
    cleanup_old_files(RESULT_FOLDER, FILE_EXPIRE_TIME)

    # Session is temporary (cleared when browser closes)
    session.permanent = False

    if "history" not in session:
        session["history"] = []

    processed = []

    if request.method == "POST":
        files = request.files.getlist("images")

        for file in files:
            if file and allowed_file(file.filename):
                uid = uuid.uuid4().hex[:8]
                original_name = secure_filename(file.filename)
                base_name = os.path.splitext(original_name)[0]

                output_name = f"{base_name}_InjectAI_background_remover.png"

                input_path = os.path.join(UPLOAD_FOLDER, f"{uid}_{original_name}")
                output_path = os.path.join(RESULT_FOLDER, output_name)

                # Save upload
                file.save(input_path)

                # Remove background
                with Image.open(input_path) as img:
                    result = remove(img)
                    result.save(output_path)

                processed.append(output_name)
                session["history"].insert(0, output_name)

    return render_template(
        "index.html",
        processed_files=processed,
        history_files=session.get("history", [])
    )


@app.route("/results/<filename>")
def download(filename):
    return send_from_directory(RESULT_FOLDER, filename, as_attachment=True)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/privacy")
def privacy():
    return render_template("privacy.html")


@app.route("/terms")
def terms():
    return render_template("terms.html")


# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
