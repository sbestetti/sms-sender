import os

from flask import Flask, request, flash, redirect, render_template
from werkzeug.utils import secure_filename

import tools

application = Flask(__name__)
application.config.from_object("settings")


@application.route("/blog")
def blog():
    return render_template("blog.html")


@application.route("/instructions")
def instructions():
    return render_template("instructions.html")


@application.route("/contact")
def contact():
    return render_template("contact.html")


@application.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if request.form["sid"] == "" or request.form["token"] == "":
            flash("Twilio ID and token required")
            return redirect(request.url)

        sid = request.form["sid"]
        token = request.form["token"]

        if not tools.valid_credentials(sid, token):
            flash("Invalid Twilio credentials. Please double check your Twilio account SID and token and try again")
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
            wrong_numbers = tools.check_numbers(number_list, sid, token)

            if wrong_numbers:
                return render_template(
                    "wrong_numbers.html",
                    number_list=wrong_numbers
                )

            number_list = tools.send_messages(number_list, sid, token)
            return render_template("report.html", number_list=number_list)
        else:
            flash("File type not allowed. Please select a CSV file")
            return redirect(request.url)

    return render_template("index.html")
