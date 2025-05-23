from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..db import db

class Goal(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    tasks: Mapped[list["Task"]] = relationship(back_populates="goal")

    def __str__(self):
        return self.__class__.__name__

    def to_dict(self):
        goal_as_dict = {}
        
        goal_as_dict["id"] = self.id
        goal_as_dict["title"] = self.title

        return goal_as_dict

    def to_nested_dict(self):
        # class_name = str(goal).lower()
        # response = {class_name: goal.to_dict()}
        class_name = str(self.__class__.__name__).lower()
        response = {class_name: self.to_dict()}

        # if self.goal_id:
        #     response[class_name]["goal_id"] = self.goal_id

        return response
    
    @classmethod
    def from_dict(cls, goal_data):
        new_goal = cls(title=goal_data["title"])

        return new_goal
    
    def update(self, request_body):
        # goal.title = request_body["title"]
        # db.session.commit()
        if 'title' in request_body:
            self.title = request_body['title']

    def goal_with_tasks(self):
        task_list = []
        
        for task in self.tasks:
            task = task.to_dict()
            task["goal_id"] = self.id
            task_list.append(task)
        
        response = self.to_dict()
        response["tasks"] = task_list

        return response