from flask import Flask

application = Flask(__name__)


@application.route("/")
def inex():
    return "<h1>OK</h1>", 200
