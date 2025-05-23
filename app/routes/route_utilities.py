
from flask import abort, make_response
from ..db import db
from datetime import datetime
import requests
import os

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except ValueError:
        invalid_response = {"message": f"{cls.__name__} id ({model_id}) is invalid."}
        abort(make_response(invalid_response, 400))
        
    query = db.select(cls).where(cls.id == model_id)
    model = db.session.scalar(query)

    if not model:
        not_found_response = {"message": f"{cls.__name__} id ({model_id}) not found."}
        abort(make_response(not_found_response, 404))

    return model

def create_model_and_response(cls, model_data):
    try:
        new_model = cls.from_dict(model_data)
    except KeyError:
        response = {"details": "Invalid data"}
        abort(make_response(response, 400))

    db.session.add(new_model)
    db.session.commit()

    class_name = str(new_model).lower()
    response = {class_name: new_model.to_dict()}

    return response, 201


def filter_and_sort_models(cls, filters=None):
    query = db.select(cls)

    if filters:
        for attribute, value in filters.items():
            if attribute == "sort":
                if value == "asc":
                    query = query.order_by(cls.title.asc())
                elif value == "desc":
                    query = query.order_by(cls.title.desc())
                
                # ============================ #
                #       OPTION ENHANCEMENT
                # ============================ #
                elif value == "id":
                    query = query.order_by(cls.id.asc())
                # if the value if not asc or desc or id
                else:
                    invalid_sort_order = {"details": "Invalid sort order. Only 'asc' or 'desc' or 'id' are allowed."}
                    abort(make_response(invalid_sort_order, 400))

            # if the class has the attribute
            if hasattr(cls, attribute):
                # getattr(cls, attribute) return the column we are looking for
                query = query.where(getattr(cls, attribute).ilike(f"%{value}%"))

    models = db.session.scalars(query)
    models_reponse = [model.to_dict() for model in models]

    return models_reponse

# ============================ #
#       OPTION ENHANCEMENT
# ============================ #
def validate_datetime_type(date_string):
    try: 
        datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S.%f")
    except ValueError:
        invalid_date_time_response = {
            "details": "Invalid datetime format. Expected 'YYYY-MM-DD HH:MM:SS.ssssss'."
        }
        abort(make_response(invalid_date_time_response, 400))

    return True

def post_task_complete_msg_to_slack(task_title):
    # Wave 4 Slack
    slack_url = os.environ.get('SLACK_URI')
    slack_token = os.environ.get('SLACK_TOEKN')

    headers = {
        "Authorization": f"Bearer {slack_token}",
        "Content-Type": "application/json"
    }   

    data = {

        "channel": "C08NTC26TM1",
        "text": f"Someone just completed the task {task_title}"
    }

    # Make the POST request to Slack API
    response = requests.post(slack_url, headers=headers, json=data)