from sqlalchemy.orm import Mapped, mapped_column, column_property, relationship
from sqlalchemy import ForeignKey
from ..db import db
from sqlalchemy import DateTime
from datetime import datetime
from typing import Optional

class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title:Mapped[str]
    description: Mapped[str]
    completed_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    is_complete = column_property(completed_at != None)

    goal_id: Mapped[Optional[int]]=mapped_column(ForeignKey("goal.id"))
    goal: Mapped[Optional["Goal"]] = relationship(back_populates="tasks")


    def __str__(self):
        return self.__class__.__name__

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
