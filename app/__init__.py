from flask import Flask

from app import settings
from app import views


def create_app():
    app = Flask(__name__)
    app.config.from_object(settings)

    app.register_blueprint(views.blog.bp)
    app.register_blueprint(views.contact.bp)
    app.register_blueprint(views.instructions.bp)
    app.register_blueprint(views.index.bp)

    return app