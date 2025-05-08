from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..db import db

class Goal(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    # Wave 5
    title: Mapped[str]

    # Wave 6
    # One to many relationship
    # One goal has many tasks
    # One task has one goal
    tasks: Mapped[list["Task"]] = relationship(back_populates="goal")

    def to_dict(self):
        goal_as_dict = {}
        goal_as_dict["id"] = self.id
        goal_as_dict["title"] = self.title

        return goal_as_dict


    @classmethod
    def from_dict(cls, goal_data):
        new_goal = cls(title=goal_data["title"])

        return new_goal