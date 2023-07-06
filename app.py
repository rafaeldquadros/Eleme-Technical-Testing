from flask import Flask
from flask_restful import Api
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from users.resources import UserCreation, UserLogin
from calls.resources import Calls, CallsById
from db import db
import os
import dotenv

dotenv.load_dotenv()


def create_app():
    app = Flask(__name__)
    api = Api(app)

    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DB_URI"]
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = os.environ["SECRET_KEY"]
    app.config["PROPAGATE_EXCEPTIONS"] = True

    db.init_app(app)

    api.add_resource(UserCreation, "/users")
    api.add_resource(UserLogin, "/login")
    api.add_resource(Calls, "/calls")
    api.add_resource(CallsById, "/calls/<int:id>")

    Migrate(app, db)
    JWTManager(app)

    def create_tables():
        db.create_all()

    return app
