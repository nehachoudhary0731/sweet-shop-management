import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import get_db, Base
from app.config import settings
from app import models, crud
from app.auth import get_password_hash

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c

@pytest.fixture(scope="module")
def db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(scope="module")
def admin_user(db):
    user = models.User(
        email="admin@example.com",
        hashed_password=get_password_hash("adminpassword"),
        full_name="Admin User",
        is_admin=True
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@pytest.fixture(scope="module")
def regular_user(db):
    user = models.User(
        email="user@example.com",
        hashed_password=get_password_hash("userpassword"),
        full_name="Regular User",
        is_admin=False
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@pytest.fixture(scope="module")
def admin_token_headers(client, admin_user):
    response = client.post(
        "/api/auth/login",
        data={
            "username": "admin@example.com",
            "password": "adminpassword"
        }
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture(scope="module")
def user_token_headers(client, regular_user):
    response = client.post(
        "/api/auth/login",
        data={
            "username": "user@example.com",
            "password": "userpassword"
        }
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}