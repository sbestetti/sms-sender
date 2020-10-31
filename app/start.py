import os

from flask import Flask, request, flash, redirect, render_template
from werkzeug.utils import secure_filename

import tools

application = Flask(__name__)
application.config.from_object("settings")


@application.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if request.form["sid"] == "" or request.form["token"] == "":
            flash("Twilio ID and token required")
            return redirect(request.url)

        if "file" not in request.files:
            flash("No file selected")
            return redirect(request.url)

        file = request.files["file"]
        if file.filename == "":
            flash("No file selected")
            return redirect(request.url)

        if file and tools.allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(
                os.path.join(
                    application.config["UPLOAD_FOLDER"],
                    filename
                )
            )

            number_list = tools.get_number_list(filename)
            wrong_numbers = tools.check_numbers(number_list)

            if wrong_numbers:
                return render_template(
                    "wrong_numbers.html",
                    number_list=wrong_numbers
                )

            number_list = tools.send_messages(number_list)
            return render_template("report.html", number_list=number_list)

    return render_template("index.html")
