
from flask import abort, make_response
from ..db import db

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

def create_model(cls, model_data):
    try:
        new_model = cls.from_dict(model_data)
    except KeyError:
        response = {"details": "Invalid data"}
        abort(make_response(response, 400))


    db.session.add(new_model)
    db.session.commit()

    class_name = (new_model.__class__.__name__).lower()
    response = {class_name: new_model.to_dict()}

    return response, 201