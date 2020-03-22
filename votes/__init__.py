import os

from flask import Flask, abort, g, request


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='super-secret-key',
    )

    app.config.from_pyfile('config.py', silent=True)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import database

    from .routes import bp

    app.register_blueprint(bp)

    from . import auth

    app.register_blueprint(auth.auth_bp)

    return app
