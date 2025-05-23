from sqlalchemy.orm import Mapped, mapped_column, column_property, relationship
from sqlalchemy import ForeignKey
from ..db import db
from sqlalchemy import DateTime
from datetime import datetime
from typing import Optional
from app.routes.route_utilities import validate_datetime_type

class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title:Mapped[str]
    description: Mapped[str]
    completed_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    # does not work somehow
    # completed_at: Mapped[Optional[datetime]]
    is_complete = column_property(completed_at != None)
    goal_id: Mapped[Optional[int]]=mapped_column(ForeignKey("goal.id"))
    goal: Mapped[Optional["Goal"]] = relationship(back_populates="tasks")

    def __str__(self):
        return self.__class__.__name__

    def to_dict(self):
        task_as_dict = {}

        task_as_dict["id"] = self.id
        task_as_dict["title"] = self.title
        task_as_dict["description"] = self.description
        task_as_dict["is_complete"] = self.is_complete

        return task_as_dict
    
    def to_nested_dict(self):
        # str(self.__class__.__name__).lower()
        # class_name = str(task).lower()
        # response = {class_name: task.to_dict()}

        # # Wave 6 if task has goal, add the goal to the response
        # if task.goal_id:
        #     response[class_name]["goal_id"] = task.goal_id

        class_name = str(self.__class__.__name__).lower()
        response = {class_name: self.to_dict()}
        # Wave 6 if task has goal, add the goal to the response
        if self.goal_id:
            response[class_name]["goal_id"] = self.goal_id

        return response
    
    @classmethod
    def from_dict(cls, task_data):

        completed_at = task_data.get("completed_at", None)

        new_task = cls(title=task_data["title"],
                       description=task_data["description"],
                       completed_at=completed_at)
        
        return new_task

    def update(self, request_body):
    
        # ============================ #
        #       OPTION ENHANCEMENT
        # ============================ #
        if "completed_at" in request_body:
            validate_datetime_type(request_body["completed_at"])
            self.completed_at = request_body["completed_at"] 
        # ============================ #
        #       OPTION ENHANCEMENT
        # ============================ #

        self.title = request_body["title"] 
        self.description = request_body["description"]