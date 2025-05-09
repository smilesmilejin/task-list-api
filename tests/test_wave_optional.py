import pytest
from app.db import db
from app.models.task import Task
from datetime import datetime

# ============================ #
#       OPTION ENHANCEMENT
# ============================ #

# @pytest.mark.skip(reason="No way to test this feature yet")
def test_get_tasks_invalid_sort_not_asc_not_desc(client, three_tasks):
    # Act
    response = client.get("/tasks?sort=abc")

    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == {
        "details": "Invalid sort order. Only 'asc' or 'desc' are allowed."
    }

# @pytest.mark.skip(reason="No way to test this feature yet")
def test_get_tasks_filtered_by_title(client, three_tasks):
    # Act
    response = client.get("/tasks?title=tickets")

    response_body = response.get_json()

    print(response_body)
    # Assert
    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body == [
        {
            "id": 3,
            "title": "Pay my outstanding tickets 😭",
            "description": "",
            "is_complete": False
        }
    ]

# @pytest.mark.skip(reason="No way to test this feature yet")
def test_get_tasks_sorted_and_filtered_by_title_and_sorted_asc(client, six_tasks):
    # Act
    response = client.get("/tasks?sort=asc&title=day")

    response_body = response.get_json()

    print(response_body)
    # Assert
    assert response.status_code == 200
    assert len(response_body) == 3
    assert response_body == [
        {
            "id": 5,
            "title": "Bob's oustanding day!",
            "description": "",
            "is_complete": False
        },
        {
            "id": 6,
            "title": "My beautiful day",
            "description": "",
            "is_complete": False
        },
        {
            "id": 4,
            "title": "Tuesday happy hour",
            "description": "",
            "is_complete": False
        }
    ]

# @pytest.mark.skip(reason="No way to test this feature yet")
def test_create_task_with_invalid_datetime_in_completed_at(client):
    # Act
    response = client.post("/tasks", json={
        "title": "A Brand New Task",
        "description": "Test Description",
        "completed_at": "Invalid Time"
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == {
            "details": "Invalid datetime format. Expected 'YYYY-MM-DD HH:MM:SS.ssssss'."
    }
    
    # Make sure the task is not added to the database
    query = db.select(Task)
    tasks = db.session.scalars(query).all()
    assert len(tasks) == 0


# @pytest.mark.skip(reason="No way to test this feature yet")
def test_create_task_successfully_with_valid_completed_at(client):
    # Act
    response = client.post("/tasks", json={
        "title": "A Brand New Task",
        "description": "Test Description",
        "completed_at": "2025-05-09 14:30:45.123456"
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 201
    assert "task" in response_body
    assert response_body == {
        "task": {
            "id": 1,
            "title": "A Brand New Task",
            "description": "Test Description",
            "is_complete": True
        }
    }
    
    query = db.select(Task).where(Task.id == 1)
    new_task = db.session.scalar(query)
    
    expected_completed_at = datetime.strptime("2025-05-09 14:30:45.123456", "%Y-%m-%d %H:%M:%S.%f")

    assert new_task
    assert new_task.title == "A Brand New Task"
    assert new_task.description == "Test Description"
    assert new_task.completed_at == expected_completed_at


# @pytest.mark.skip(reason="No way to test this feature yet")
def test_update_task_with_invalid_datetime_in_completed_at(client, one_task):
    # Act
    response = client.put("/tasks/1", json={
        "title": "A Brand New Task",
        "description": "Test Description",
        "completed_at": "Invalid Time"
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == {
            "details": "Invalid datetime format. Expected 'YYYY-MM-DD HH:MM:SS.ssssss'."
    }
    
    # Make sure the task in the database is not changed
    query = db.select(Task).where(Task.id == 1)
    new_task = db.session.scalar(query)

    assert new_task
    assert new_task.title == "Go on my daily walk 🏞"
    assert new_task.description == "Notice something new every day"
    assert new_task.completed_at == None

# @pytest.mark.skip(reason="No way to test this feature yet")
def test_update_task_successfully_with_valid_completed_at(client, one_task):
    # Act
    response = client.put("/tasks/1", json={
        "title": "A Brand New Task",
        "description": "Test Description",
        "completed_at": "2023-12-31 23:59:59.999999"
    })

    # Assert
    assert response.status_code == 204
    assert response.content_length is None

    query = db.select(Task).where(Task.id == 1)
    task = db.session.scalar(query)

    expected_completed_at = datetime.strptime("2023-12-31 23:59:59.999999", "%Y-%m-%d %H:%M:%S.%f")

    assert task.title == "A Brand New Task"
    assert task.description == "Test Description"
    assert task.completed_at == expected_completed_at
    assert task.is_complete == True
