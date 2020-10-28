import os

from flask import Flask, request, flash, redirect, render_template
from werkzeug.utils import secure_filename

application = Flask(__name__)
application.config.from_object("settings")


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower()
        in application.config["ALLOWED_EXTENSIONS"]
        )


@application.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "file" not in request.files:
            flash("No file part")
            return redirect(request.url)

        file = request.files["file"]
        if file.filename == "":
            flash("No selected file")
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(
                os.path.join(
                    application.config["UPLOAD_FOLDER"],
                    filename
                )
            )
            return "File uploaded", 200
    return render_template("index.html")
