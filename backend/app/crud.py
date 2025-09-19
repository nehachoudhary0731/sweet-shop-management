from app.auth import get_password_hash
from sqlalchemy.orm import Session
from sqlalchemy import or_

from . import models, schemas

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        email=user.email, 
        hashed_password=hashed_password, 
        full_name=user.full_name
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_sweets(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Sweet).offset(skip).limit(limit).all()

def get_sweet(db: Session, sweet_id: int):
    return db.query(models.Sweet).filter(models.Sweet.id == sweet_id).first()

def create_sweet(db: Session, sweet: schemas.SweetCreate):
    db_sweet = models.Sweet(**sweet.dict())
    db.add(db_sweet)
    db.commit()
    db.refresh(db_sweet)
    return db_sweet

def update_sweet(db: Session, sweet_id: int, sweet_update: schemas.SweetUpdate):
    db_sweet = db.query(models.Sweet).filter(models.Sweet.id == sweet_id).first()
    if not db_sweet:
        return None
    
    update_data = sweet_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_sweet, field, value)
    
    db.commit()
    db.refresh(db_sweet)
    return db_sweet

def delete_sweet(db: Session, sweet_id: int):
    db_sweet = db.query(models.Sweet).filter(models.Sweet.id == sweet_id).first()
    if db_sweet:
        db.delete(db_sweet)
        db.commit()
    return db_sweet

def search_sweets(db: Session, query: str = None, category: str = None, min_price: float = None, max_price: float = None):
    q = db.query(models.Sweet)
    
    if query:
        q = q.filter(or_(
            models.Sweet.name.ilike(f"%{query}%"),
            models.Sweet.description.ilike(f"%{query}%")
        ))
    
    if category:
        q = q.filter(models.Sweet.category == category)
    
    if min_price is not None:
        q = q.filter(models.Sweet.price >= min_price)
    
    if max_price is not None:
        q = q.filter(models.Sweet.price <= max_price)
    
    return q.all()

def purchase_sweet(db: Session, sweet_id: int, user_id: int, quantity: int):
    sweet = db.query(models.Sweet).filter(models.Sweet.id == sweet_id).first()
    if not sweet or sweet.quantity < quantity:
        return None
    
    sweet.quantity -= quantity
    total_price = sweet.price * quantity
    
    purchase = models.Purchase(
        user_id=user_id,
        sweet_id=sweet_id,
        quantity=quantity,
        total_price=total_price
    )
    
    db.add(purchase)
    db.commit()
    db.refresh(purchase)
    db.refresh(sweet)
    
    return purchase

def restock_sweet(db: Session, sweet_id: int, quantity: int):
    sweet = db.query(models.Sweet).filter(models.Sweet.id == sweet_id).first()
    if not sweet:
        return None
    
    sweet.quantity += quantity
    db.commit()
    db.refresh(sweet)
    return sweet

def get_user_purchases(db: Session, user_id: int):
    return db.query(models.Purchase).filter(models.Purchase.user_id == user_id).all()