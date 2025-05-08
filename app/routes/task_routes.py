from flask import Blueprint, request, abort, make_response, Response
from app.models.task import Task
from app.models.goal import Goal
from app.db import db
from app.routes.route_utilities import validate_model
from datetime import datetime
import requests # Use Python package requests to make HTTP calls
import os

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix = "/tasks")

# Wave 1
@tasks_bp.post("")
def create_task():

    request_body = request.get_json()

    # print('####### request_body:', request_body)
    # request_body {'title': 'A Brand New Task', 'description': 'Test Description'}
    
    ######################################## Option 1
    # if (not "title" in request_body) or (not "description" in request_body):
    #     response = {
    #         "details": "Invalid data"
    #     }
        
    #     return response, 400
    
    ################################## Option 1 Refactoring
    try:
        new_task = Task.from_dict(request_body)
    except KeyError as e:
        response = {"details": "Invalid data"}
        abort(make_response(response, 400))
        # return response, 400 # THis also works
    ################################## END Option 1 Refactoring


    ######################################## Option 2
    # Refactoring the class method in task.py

    # title = request_body["title"]
    # description = request_body["description"]
    
    # if not "completed_at" in request_body:
    #     new_task = Task(
    #         title=title, 
    #         description=description
    #     )
    #     # None
    #     # print('##### if completed at key NOT in request_body new_task.completed_at : ', new_task.completed_at)

    # elif "completed_at" in request_body:
        
    #     completed_at = request_body["completed_at"]
    
    #     new_task = Task(
    #             title=title, 
    #             description=description,
    #             completed_at=completed_at
    #     )

    #     # "completed_at": null
    #     # None
    #     # print('##### if completed at key in request_bodycompleted_at is: ', completed_at)
    
    ######################################## END Option 2

    
    db.session.add(new_task)
    db.session.commit()

    ######################################## Option 3
    # response = {
    #     "task": {
    #         "id": new_task.id,
    #         "title": new_task.title,
    #         "description": new_task.description,
    #         # "completed_at": new_task.completed_at
    #         # "is_complete": False if new_task.completed_at is None else True
    #         "is_complete": new_task.is_complete
    #     }
    # }

    ######################################## Option 3 Refactoring
    # use to_dict for creating the instance dictionary
    # response = {"task": new_task.to_dict()}
    ######################################## END Option 3 Refactoring


    ####################### Optiona 3 Refactoring Version 2
    class_name = (new_task.__class__.__name__).lower()
    response = {class_name: new_task.to_dict()}
    ####################### END Optiona 1 Refactoring

    return response, 201


@tasks_bp.get("")
def get_all_tasks():
    query = db.select(Task)

    # Wave 2
    # /tasks?sort=asc
    # /tasks?sort=desc
    sort_param = request.args.get("sort")

    if sort_param == "asc":
        query = query.order_by(Task.title.asc())

    elif sort_param == "desc":
        query = query.order_by(Task.title.desc())
    # End Wave 2 
    
    tasks = db.session.scalars(query)

    tasks_response = []
    for task in tasks:
        ######################################## Option 1
        # tasks_response.append(
        #     {
        #     "id": task.id,
        #     "title": task.title,
        #     "description": task.description,
        #     # "completed_at": new_task.completed_at
        #     # "is_complete": False if task.completed_at is None else True
        #     "is_complete": task.is_complete
        #     }
        # )

        ######################################## Option 1 Refactoring
        # use to_dict for creating the instance dictionary
        tasks_response.append(task.to_dict())
        ######################################## END Option 1 Refactoring

    return tasks_response, 200


@tasks_bp.get("/<task_id>")
def get_one_task(task_id):

    ######################################## Option 1
    # task = validate_task(task_id)

    ######################################## Option 1 Refactoring 
    task = validate_model(Task, task_id)
    ######################################## END Option 1 Refactoring 

    ######################################## Option 1
    # response = {
    #     "task": {
    #         "id": task.id,
    #         "title": task.title,
    #         "description": task.description,
    #         # "completed_at": new_task.completed_at
    #         # "is_complete": False if task.completed_at is None else True
    #         "is_complete": task.is_complete
    #     }
    # }

    ######################################## Option 1 Refactoring
    # use to_dict for creating the instance dictionary
    # response = {"task": task.to_dict()}
    ######################################## END Option 1 Refactoring
    
    ######################################## Optiona 2 Refactoring Version 2
    class_name = (task.__class__.__name__).lower()
    response = {class_name: task.to_dict()}
    ######################################## END Optiona 2 Refactoring

    # Wave 6 if there is goal_id add it
    if task.goal_id:
        response[class_name]["goal_id"] = task.goal_id
    
    return response, 200

######################################## Option 1 
# moved this to route_utilies.
# def validate_task(task_id):
#     try:
#         task_id = int(task_id)
#     except ValueError:
#         invalid_response = {"message": f"Task id ({task_id}) is invalid."}
#         abort(make_response(invalid_response, 400))
        
#     query = db.select(Task).where(Task.id == task_id)
#     task = db.session.scalar(query)

#     if not task:
#         not_found_response = {"message": f"Task id ({task_id}) not found."}
#         abort(make_response(not_found_response, 404))

#     return task

@tasks_bp.put("/<task_id>")
def update_task(task_id):
    ######################################## Option 1
    # task = validate_task(task_id)

    ######################################## Option 1 Refactoring 
    task = validate_model(Task, task_id)
    ######################################## END Option 1 Refactoring 

    request_body = request.get_json()

    task.title = request_body["title"] 
    task.description = request_body["description"]

    db.session.commit()
    return Response(status=204, mimetype="application/json")

@tasks_bp.delete("/<task_id>")
def delete_task(task_id):
    ######################################## Option 1
    # task = validate_task(task_id)

    ######################################## Option 1 Refactoring 
    task = validate_model(Task, task_id)
    ######################################## END Option 1 Refactoring 
    db.session.delete(task)
    db.session.commit()
    
    return Response(status=204, mimetype="application/json")


@tasks_bp.patch("/<task_id>/mark_complete")
def mark_task_complete(task_id):
    task = validate_model(Task, task_id)

    task.completed_at = datetime.now()
    
    db.session.commit()

    # Wave 4
    # Get environmental variables from .env
    slack_url = os.environ.get('SLACK_URI')
    slack_token = os.environ.get('SLACK_TOEKN')

    headers = {
        # This will not work!
        # "Authorization": slack_token,
        "Authorization": f"Bearer {slack_token}",
        "Content-Type": "application/json"
    }   

    data = {

        "channel": "C08NTC26TM1",
        "text": f"Someone just completed the task {task.title}"
    }

    # Make the POST request to Slack API
    response = requests.post(slack_url, headers=headers, json=data)

    # Check Slack Reponse Status code and json
    print('################## Slack Response')
    print(response)
    print(response.status_code)
    print(response.json()) 
    # End Wave 4 

    return Response(status=204, mimetype="application/json")

@tasks_bp.patch("/<task_id>/mark_incomplete")
def mark_task_incomplete(task_id):
    task = validate_model(Task, task_id)
    
    task.completed_at = None
    db.session.commit()
    return Response(status=204, mimetype="application/json")

