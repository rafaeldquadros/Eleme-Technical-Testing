from db import db
from datetime import datetime


class CallsModel(db.Model):
    __tablename__ = "calls"

    id = db.Column(db.Integer, primary_key=True)
    priority_level = db.Column(db.String(40), nullable=False)
    status = db.Column(db.String(40), nullable=False, default="Pendente")
    setor = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    createdAt = db.Column(db.String(200), default=datetime.utcnow, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    def __init__(self, priority_level, status, setor, description, user_id):
        self.priority_level = priority_level
        self.status = status
        self.setor = setor
        self.description = description
        self.user_id = user_id

    def as_dict(self):
        return {c.key: getattr(self, c.key) for c in self.__mapper__.column_attrs}

    @classmethod
    def find_all(cls):
        return cls.query.all()

    @classmethod
    def find_by_id(cls, call_id):
        return db.session.get(cls, call_id)

    @classmethod
    def delete(cls, call_id):
        call = db.session.get(cls, call_id)
        if not call:
            return False

        db.session.delete(call)
        db.session.commit()

        return True

    @classmethod
    def update(cls, call_id, **kwargs):
        call = db.session.get(cls, call_id)
        if not call:
            return False

        for key, value in kwargs.items():
            if value is not None:
                setattr(call, key, value)

        db.session.commit()

        return call.as_dict()

    def save(self):
        db.session.add(self)
        db.session.commit()
