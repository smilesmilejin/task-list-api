from flask import Blueprint, request, Response
from app.models.task import Task
from app.db import db
from app.routes.route_utilities import validate_model, create_model_and_response, filter_and_sort_models, validate_datetime_type, post_task_complete_msg_to_slack
from datetime import datetime
import requests # Use Python package requests to make HTTP calls
import os

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix = "/tasks")

# Wave 1
@tasks_bp.post("")
def create_task():
    request_body = request.get_json()

    # ============================ #
    #       OPTION ENHANCEMENT
    # ============================ #
    if "completed_at" in request_body:
        validate_datetime_type(request_body["completed_at"])
    # ============================ #
    #       OPTION ENHANCEMENT
    # ============================ #

    return create_model_and_response(Task, request_body)


@tasks_bp.get("")
def get_all_tasks():
    return filter_and_sort_models(Task, request.args)

@tasks_bp.get("/<task_id>")
def get_one_task(task_id):
    task = validate_model(Task, task_id)

    # class_name = str(task).lower()
    # response = {class_name: task.to_dict()}

    # # Wave 6 if task has goal, add the goal to the response
    # if task.goal_id:
    #     response[class_name]["goal_id"] = task.goal_id

    response = task.to_nested_dict()
    
    return response


@tasks_bp.put("/<task_id>")
def update_task(task_id):
    task = validate_model(Task, task_id)

    request_body = request.get_json()
    
    # # ============================ #
    # #       OPTION ENHANCEMENT
    # # ============================ #
    # if "completed_at" in request_body:
    #     validate_datetime_type(request_body["completed_at"])
    #     task.completed_at = request_body["completed_at"] 
    # # ============================ #
    # #       OPTION ENHANCEMENT
    # # ============================ #

    # task.title = request_body["title"] 
    # task.description = request_body["description"]

    task.update(request_body)

    db.session.commit()
    return Response(status=204, mimetype="application/json")

@tasks_bp.delete("/<task_id>")
def delete_task(task_id):
    task = validate_model(Task, task_id)
   
    db.session.delete(task)
    db.session.commit()
    
    return Response(status=204, mimetype="application/json")


@tasks_bp.patch("/<task_id>/mark_complete")
def mark_task_complete(task_id):
    task = validate_model(Task, task_id)

    task.completed_at = datetime.now()
    
    db.session.commit()

    # # Wave 4 Slack
    # slack_url = os.environ.get('SLACK_URI')
    # slack_token = os.environ.get('SLACK_TOEKN')

    # headers = {
    #     "Authorization": f"Bearer {slack_token}",
    #     "Content-Type": "application/json"
    # }   

    # data = {

    #     "channel": "C08NTC26TM1",
    #     "text": f"Someone just completed the task {task.title}"
    # }

    # # Make the POST request to Slack API
    # response = requests.post(slack_url, headers=headers, json=data)

    post_task_complete_msg_to_slack(task.title)

    return Response(status=204, mimetype="application/json")

@tasks_bp.patch("/<task_id>/mark_incomplete")
def mark_task_incomplete(task_id):
    task = validate_model(Task, task_id)
    
    task.completed_at = None
    db.session.commit()
    
    return Response(status=204, mimetype="application/json")

