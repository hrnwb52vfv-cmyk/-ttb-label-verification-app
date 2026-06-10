import os
from datetime import datetime
from flask import Flask, render_template, request, flash, redirect, url_for
from werkzeug.utils import secure_filename

from config import UPLOAD_FOLDER, ALLOWED_EXTENSIONS, MAX_CONTENT_LENGTH
from services.ocr_service import extract_text
from services.validation_service import validate_label

app = Flask(__name__)
app.secret_key = "development-secret-key"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/verify", methods=["POST"])
def verify():
    label_file = request.files.get("label")

    if not label_file or label_file.filename == "":
        flash("Please upload a label image.", "error")
        return redirect(url_for("index"))

    if not allowed_file(label_file.filename):
        flash("Unsupported file type. Please upload PNG, JPG, JPEG, WEBP, BMP, or TIFF.", "error")
        return redirect(url_for("index"))

    filename = secure_filename(label_file.filename)
    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    saved_filename = f"{timestamp}_{filename}"
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], saved_filename)
    label_file.save(file_path)

    application_data = {
        "brand_name": request.form.get("brand_name", "").strip(),
        "class_type": request.form.get("class_type", "").strip(),
        "alcohol_content": request.form.get("alcohol_content", "").strip(),
        "net_contents": request.form.get("net_contents", "").strip(),
    }

    try:
        extracted_text = extract_text(file_path)
        results = validate_label(extracted_text, application_data)
    except Exception as error:
        flash(f"Unable to process the label: {error}", "error")
        return redirect(url_for("index"))

    return render_template(
        "results.html",
        results=results,
        extracted_text=extracted_text,
        application_data=application_data,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
