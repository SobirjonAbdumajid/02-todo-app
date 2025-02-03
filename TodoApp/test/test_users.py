# test_users.py
from .utils import *
from ..routers.users import get_db, get_current_user
from fastapi import status


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

def test_return_users(test_user):
    response = client.get('/user')
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['username'] == 'sobirjonabdumajidtest'
    assert response.json()['email'] == 'sobirjon.abdumajid@gmail.com'
    assert response.json()['first_name'] == 'Sobirjon'
    assert response.json()['last_name'] == 'Abdumajid'
    assert response.json()['role'] == 'admin'
    assert response.json()['phone_number'] == '1234567890'



def test_change_password_success(test_user):
    response = client.put('/user/password', json={'password': 'sobirjon123',
                                                  'new_password': 'sobirjon312'})
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_change_password_invalid(test_user):
    response = client.put('/user/password', json={'password': 'wrong_password',
                                                  'new_password': 'sobirjon312'})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {'detail': 'Incorrect password'}


def test_change_phone_number_success(test_user):
    response = client.put('/user/phonenumber/9999')

    assert response.status_code == status.HTTP_204_NO_CONTENT
