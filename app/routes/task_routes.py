from flask import Blueprint, request, abort, make_response
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


@tasks_bp.get("")
def get_all_tasks():
    query = db.select(Task)
    tasks = db.session.scalars(query)

    tasks_response = []
    for task in tasks:
        tasks_response.append(
            {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            # "completed_at": new_task.completed_at
            "is_complete": False if task.completed_at is None else True
            }
        )

    return tasks_response, 200


@tasks_bp.get("/<task_id>")
def get_one_task(task_id):
    task = validate_task(task_id)

    response = {
        "task": {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            # "completed_at": new_task.completed_at
            "is_complete": False if task.completed_at is None else True
        }
    }
    
    return response, 200

def validate_task(task_id):
    try:
        task_id = int(task_id)
    except ValueError:
        invalid_response = {"message": f"Task id ({task_id}) is invalid."}
        abort(make_response(invalid_response, 400))
        
    query = db.select(Task).where(Task.id == task_id)
    task = db.session.scalar(query)

    if not task:
        not_found_response = {"message": f"Task id ({task_id}) not found."}
        abort(make_response(not_found_response, 404))

    return task