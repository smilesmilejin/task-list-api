from flask import Blueprint, request, abort, make_response
from ..db import db
from app.models.goal import Goal
from app.routes.route_utilities import validate_model

goals_bp = Blueprint("goals_bp", __name__, url_prefix = "/goals")


# Wave 5
@goals_bp.post("")
def create_goal():
    request_body = request.get_json()

    try:
        new_goal = Goal.from_dict(request_body)
    except KeyError as e:
        response = {"details": "Invalid data"}
        abort(make_response(response, 400))

    db.session.add(new_goal)
    db.session.commit()

    ####################### Optional 1
    # response = {"goal": new_goal.to_dict()}

    ####################### Optiona 1 Refactoring
    class_name = (new_goal.__class__.__name__).lower()
    response = {class_name: new_goal.to_dict()}
    ####################### END Optiona 1 Refactoring

    return response, 201

# GET request to /goals
@goals_bp.get("")
def get_all_goals():

    query = db.select(Goal)
    goals = db.session.scalars(query)

    response = [goal.to_dict() for goal in goals]

    return response, 200


@goals_bp.get("/<goal_id>")
def get_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    class_name = (goal.__class__.__name__).lower()
    response = {class_name: goal.to_dict()}

    return response, 200