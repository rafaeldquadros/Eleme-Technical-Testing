from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token

from .model import UsersModel
from .exceptions import (
    UsersAlreadyExistisExcpetion,
    UserEmailOrPasswordInvalidExcpetion,
)


class UsersService:
    def create(self, **kwargs):
        user = UsersModel.find_user_email(kwargs["email"])
        if user:
            raise UsersAlreadyExistisExcpetion(
                "There is already a user registered with this email: {}".format(
                    kwargs["email"]
                )
            )

        new_user = UsersModel(**kwargs)
        new_user.save()
        return new_user.as_dict()

    def login(self, **kwargs):
        user = UsersModel.find_user_email(kwargs["email"])
        if user and pbkdf2_sha256.verify(kwargs["password"], user.password):
            access_token = create_access_token(identity=user.id)

            if user.isAdmin:
                access_token_with_claim = create_access_token(
                    identity=user.id, additional_claims={"is_admin": True}
                )
            else:
                access_token_with_claim = access_token

            return {"access_token": access_token_with_claim}

        raise UserEmailOrPasswordInvalidExcpetion("Invalid email or password")
