import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import models, crud
from app.schemas import SweetCreate

def test_create_sweet(client: TestClient, admin_token_headers: dict, db: Session):
    response = client.post(
        "/api/sweets",
        headers=admin_token_headers,
        json={
            "name": "Test Sweet",
            "description": "A test sweet",
            "category": "chocolate",
            "price": 2.99,
            "quantity": 50
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Sweet"
    assert data["price"] == 2.99
    assert "id" in data

def test_get_sweets(client: TestClient, db: Session):
    # Create a test sweet first
    sweet_data = SweetCreate(
        name="Test Sweet",
        description="A test sweet",
        category="chocolate",
        price=2.99,
        quantity=50
    )
    crud.create_sweet(db, sweet_data)
    
    response = client.get("/api/sweets")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert data[0]["name"] == "Test Sweet"

def test_search_sweets(client: TestClient, db: Session):
    # Create test sweets
    sweet1 = SweetCreate(
        name="Chocolate Bar",
        description="Delicious chocolate",
        category="chocolate",
        price=1.99,
        quantity=100
    )
    sweet2 = SweetCreate(
        name="Gummy Bears",
        description="Fruity gummies",
        category="candy",
        price=0.99,
        quantity=200
    )
    crud.create_sweet(db, sweet1)
    crud.create_sweet(db, sweet2)
    
    # Search by category
    response = client.get("/api/sweets/search?category=chocolate")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["category"] == "chocolate"
    
    # Search by name
    response = client.get("/api/sweets/search?query=gummy")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert "gummy" in data[0]["name"].lower()

def test_purchase_sweet(client: TestClient, user_token_headers: dict, db: Session):
    # Create a test sweet first
    sweet_data = SweetCreate(
        name="Test Sweet",
        description="A test sweet",
        category="chocolate",
        price=2.99,
        quantity=50
    )
    sweet = crud.create_sweet(db, sweet_data)
    
    # Purchase the sweet
    response = client.post(
        f"/api/sweets/{sweet.id}/purchase",
        headers=user_token_headers,
        json={"quantity": 2}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["quantity"] == 2
    assert data["total_price"] == 5.98
    
    # Verify stock decreased
    sweet_response = client.get(f"/api/sweets/{sweet.id}")
    assert sweet_response.json()["quantity"] == 48

def test_restock_sweet(client: TestClient, admin_token_headers: dict, db: Session):
    # Create a test sweet first
    sweet_data = SweetCreate(
        name="Test Sweet",
        description="A test sweet",
        category="chocolate",
        price=2.99,
        quantity=50
    )
    sweet = crud.create_sweet(db, sweet_data)
    
    # Restock the sweet
    response = client.post(
        f"/api/sweets/{sweet.id}/restock",
        headers=admin_token_headers,
        json={"quantity": 20}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["quantity"] == 70