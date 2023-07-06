from db import db
from passlib.hash import pbkdf2_sha256


class UsersModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(300), nullable=False)
    isAdmin = db.Column(db.Boolean, default=False)

    def __init__(self, name, email, password, isAdmin):
        self.name = name
        self.email = email
        self.password = pbkdf2_sha256.hash(password)
        self.isAdmin = bool(isAdmin)

    def as_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "isAdmin": self.isAdmin,
        }

    @classmethod
    def find_user_email(cls, _email):
        return cls.query.filter_by(email=_email).first()

    def find_user_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    def save(self):
        db.session.add(self)
        db.session.commit()
