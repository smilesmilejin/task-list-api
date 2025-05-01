from flask import Blueprint, request
from app.models.task import Task
from app.db import db

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix = "/tasks")

@tasks_bp.post("")
def create_task():

    request_body = request.get_json()

    # print('####### request_body:', request_body)
    # request_body {'title': 'A Brand New Task', 'description': 'Test Description'}

    if (not "title" in request_body) or (not "description" in request_body):
        response = {
            "details": "Invalid data"
        }
        
        return response, 400

    title = request_body["title"]
    description = request_body["description"]
    
    if not "completed_at" in request_body:
        new_task = Task(
            title=title, 
            description=description
        )
        # None
        # print('##### if completed at key NOT in request_body new_task.completed_at : ', new_task.completed_at)

    elif "completed_at" in request_body:
        
        completed_at = request_body["completed_at"]
    
        new_task = Task(
                title=title, 
                description=description,
                completed_at=completed_at
        )

        # "completed_at": null
        # None
        print('##### if completed at key in request_bodycompleted_at is: ', completed_at)
    
    db.session.add(new_task)
    db.session.commit()

    response = {
        "task": {
            "id": new_task.id,
            "title": new_task.title,
            "description": new_task.description,
            # "completed_at": new_task.completed_at
            "is_complete": False if new_task.completed_at is None else True
        }
    }
    return response, 201
