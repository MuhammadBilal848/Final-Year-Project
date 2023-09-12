from peewee import Model, CharField
from db.db import db

class User(Model):
    username = CharField(unique=True)
    email = CharField(unique=True)

    class Meta:
        database = db

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
        }
