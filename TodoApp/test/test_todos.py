from ..routers.todos import get_db, get_current_user
from fastapi import status
from .utils import *

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

def test_read_all_authenticated(test_todo):
    response = client.get('/todos')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [
        {
            'id': 1,
            "title": "Learn code",
            "description": "don't give up",
            "priority": 5,
            "complete": False,
            "owner_id": 1
        }
    ]


def test_read_one_authenticated(test_todo):
    response = client.get('/todos/todo/1')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        'id': 1,
        "title": "Learn code",
        "description": "don't give up",
        "priority": 5,
        "complete": False,
        "owner_id": 1
    }


def test_read_todo_authenticated_not_found():
    response = client.get('/todos/todo/999')
    assert response.json()['status_code'] == 404
    assert response.json() == {'detail': 'Todo not found', 'headers': None, 'status_code': 404}


def test_create_todo(test_todo):
    request_data={
        'title': 'New Todo!',
        'description':'New todo description',
        'priority': 5,
        'complete': False,
    }

    response = client.post('/todos/todo/', json=request_data)
    assert response.status_code == 201

    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 2).first()
    assert model.title == request_data.get('title')
    assert model.description == request_data.get('description')
    assert model.priority == request_data.get('priority')
    assert model.complete == request_data.get('complete')