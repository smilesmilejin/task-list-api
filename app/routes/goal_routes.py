from flask import Blueprint, request, Response
from ..db import db
from app.models.goal import Goal
from app.models.task import Task
from app.routes.route_utilities import validate_model, create_model_and_response, filter_and_sort_models

goals_bp = Blueprint("goals_bp", __name__, url_prefix = "/goals")


@goals_bp.post("")
def create_goal():
    request_body = request.get_json()

    return create_model_and_response(Goal, request_body)


@goals_bp.get("")
def get_all_goals():
    return filter_and_sort_models(Goal, request.args)


@goals_bp.get("/<goal_id>")
def get_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    # class_name = str(goal).lower()
    # response = {class_name: goal.to_dict()}

    response = goal.to_nested_dict()
    return response


@goals_bp.put("/<goal_id>")
def update_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    request_body = request.get_json()

    # goal.title = request_body["title"]
    # db.session.commit()
    goal.update(request_body)
    db.session.commit()

    return Response(status=204, mimetype="application/json")


@goals_bp.delete("/<goal_id>")
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    db.session.delete(goal)
    db.session.commit()
    
    return Response(status=204, mimetype="application/json")


@goals_bp.post("/<goal_id>/tasks")
def add_existing_tasksIDs_list_to_existing_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    request_body = request.get_json()

    # if the goal already has tasks, create a new list for response,  
    # Note: all previous tasks is not deleted
    if goal.tasks:
        goal.tasks = []

    if "task_ids" in request_body:
        # for task_id in request_body["task_ids"]:
        #     task = validate_model(Task, task_id)
        #     goal.tasks.append(task)
        task_ids = request_body["task_ids"]
        valid_tasks = [validate_model(Task, task_id) for task_id in task_ids]
        goal.tasks = valid_tasks 

    db.session.commit()
    
    response_id= {"id": goal.id}
    response_body = response_id | request_body

    return response_body


@goals_bp.get("/<goal_id>/tasks")
def get_goal_with_tasks_list(goal_id):
    goal = validate_model(Goal, goal_id)

    # task_list = []
    # for task in goal.tasks:
    #     task = task.to_dict()
    #     task["goal_id"] = int(goal_id)
    #     task_list.append(task)
    
    # response = goal.to_dict()
    # response["tasks"] = task_list

    response = goal.goal_with_tasks()

    return response

