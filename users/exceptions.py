from werkzeug.exceptions import HTTPException


class UsersAlreadyExistisExcpetion(HTTPException):
    code = 400


class UserEmailOrPasswordInvalidExcpetion(HTTPException):
    code = 404
