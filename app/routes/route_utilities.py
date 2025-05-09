
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

    # class_name = (new_model.__class__.__name__).lower()
    class_name = str(new_model).lower()
    response = {class_name: new_model.to_dict()}

    return response, 201

def get_models_sorted_by_title(cls, sort_order):
    query = db.select(cls)

    if sort_order:
        for sort, order in sort_order.items():
            if order == "asc":
                # print('############### asc')
                query = query.order_by(cls.title.asc())
            elif order == "desc":
                # print('############### desc')
                query = query.order_by(cls.title.desc())
    
    models = db.session.scalars(query)
    models_reponse = [model.to_dict() for model in models]

    return models_reponse