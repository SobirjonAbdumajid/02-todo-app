# utils.py
from sqlalchemy import create_engine, text
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker
from TodoApp.database import Base
from TodoApp.main import app
from TodoApp.models import Todos, Users
from ..routers.auth import bcrypt_context
import pytest


SQLALCHEMY_DATABASE_URI = 'sqlite:///./testdb.db'
engine = create_engine(
    SQLALCHEMY_DATABASE_URI,
    connect_args={'check_same_thread': False},
    poolclass = StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

def override_get_current_user():
    return {'username': 'string', 'id': 1, 'user_role': 'admin'}


client = TestClient(app)


@pytest.fixture
def test_todo():
    todo = Todos(
        title='Learn code',
        description="don't give up",
        priority=5,
        complete=False,
        owner_id=1
    )

    db = TestingSessionLocal()
    db.add(todo)
    db.commit()
    yield todo
    with TestingSessionLocal() as connection:
        connection.execute(text('DELETE FROM todos;'))
        connection.commit()
        # db.delete(todo)
    # db.rollback()


@pytest.fixture
def test_user():
    user = Users(
        username='sobirjonabdumajidtest',
        email='sobirjon.abdumajid@gmail.com',
        first_name='Sobirjon',
        last_name='Abdumajid',
        hashed_password=bcrypt_context.hash("sobirjon123"),
        role='admin',
        phone_number="1234567890"
    )

    db = TestingSessionLocal()
    db.add(user)
    db.commit()
    yield user
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM users;"))
        connection.commit()