from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from .models import db
from config import config


migrate = Migrate()


def create_app(config_name="default"):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    CORS(app)
    migrate.init_app(app, db)

    return app
