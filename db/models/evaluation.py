from peewee import Model, IntegerField, CharField, ForeignKeyField, DateField
from db.models.user import User
from db.db import db


class Evaluation(Model):
    evaluation = IntegerField()
    evaluation_message = CharField(max_length=255)
    user_id = ForeignKeyField(User, backref="evaluations")
    evaluation_date = DateField()

    class Meta:
        database = db
        db_table = "evaluation"

    def to_dict(self):
        return {
            "id": self.id,
            "evaluation": self.evaluation,
            "evaluation_message": self.evaluation_message,
            "user": self.user_id.to_dict(),
            "evaluation_date": self.evaluation_date.strftime(
                "%Y-%m-%d"
            ),  # Format the date as a string
        }
