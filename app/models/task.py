from sqlalchemy.orm import Mapped, mapped_column, column_property
from ..db import db
from sqlalchemy import DateTime
from datetime import datetime

class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    # Wave 1
    title:Mapped[str]
    description: Mapped[str]
    completed_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    # "is_complete": False if new_task.completed_at is None else True
    # is_complete is not a column in the database but is a calculated field.
    # It will return True if completed_at is not null, otherwise False.
    #  It’s not meant to be updated directly — the value is always derived from other fields.
    is_complete = column_property(completed_at != None)

    # No column completed_at
    def to_dict(self):
        task_as_dict = {}

        task_as_dict["id"] = self.id
        task_as_dict["title"] = self.title
        task_as_dict["description"] = self.description
        task_as_dict["is_complete"] = self.is_complete

        return task_as_dict
    
    @classmethod
    def from_dict(cls, task_data):

        completed_at = task_data.get("completed_at", None)

        new_task = cls(title=task_data["title"],
                       description=task_data["description"],
                       completed_at=completed_at)
        
        return new_task
