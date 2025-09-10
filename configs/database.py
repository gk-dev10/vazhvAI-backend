import os
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv() 

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    CORS(app)

    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise RuntimeError("DATABASE_URL is not set in .env")

    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    return app
