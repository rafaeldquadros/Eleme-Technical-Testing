from flask_restful import Resource, reqparse
from .services import UsersService


class Base:
    __service__ = UsersService

    parser = reqparse.RequestParser()
    parser.add_argument("name", type=str, required=True, help="Informe um nome")
    parser.add_argument("email", type=str, required=True, help="Informe um email")
    parser.add_argument("password", type=str, required=True, help="Informe uma senha")
    parser.add_argument("isAdmin", type=str, required=False, help="Deve ser boolean")


class UserCreation(Resource):
    __service__ = UsersService

    parser = reqparse.RequestParser()

    parser.add_argument(
        "name", type=str, required=True, help="Name is a required field"
    )
    parser.add_argument(
        "email", type=str, required=True, help="Email is a required field"
    )
    parser.add_argument(
        "password", type=str, required=True, help="Password is a required field"
    )
    parser.add_argument("isAdmin", type=str, required=False)

    def post(self):
        data = UserCreation.parser.parse_args()
        return self.__service__.create(self, **data)


class UserLogin(Resource):
    __service__ = UsersService

    parser = reqparse.RequestParser()
    parser.add_argument(
        "email", type=str, required=True, help="Email is a required field"
    )
    parser.add_argument(
        "password", type=str, required=True, help="Password is a required field"
    )

    def post(self):
        data = UserLogin.parser.parse_args()
        return self.__service__.login(self, **data)
