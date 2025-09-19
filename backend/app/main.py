from datetime import timedelta
from fastapi import FastAPI, Depends, HTTPException, status, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional

from . import models, schemas, crud, auth, dependencies
from .database import engine, get_db
from .config import settings

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React app origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Auth endpoints
@app.post("/api/auth/register", response_model=schemas.User)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    return crud.create_user(db=db, user=user)

@app.post("/api/auth/login", response_model=schemas.Token)
def login_user(form_data: schemas.UserCreate, db: Session = Depends(get_db)):
    user = auth.authenticate_user(db, form_data.email, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# Sweet endpoints
@app.post("/api/sweets", response_model=schemas.Sweet, status_code=status.HTTP_201_CREATED)
def create_sweet(
    sweet: schemas.SweetCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_admin_user)
):
    return crud.create_sweet(db=db, sweet=sweet)

@app.get("/api/sweets", response_model=List[schemas.Sweet])
def read_sweets(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    sweets = crud.get_sweets(db, skip=skip, limit=limit)
    return sweets

@app.get("/api/sweets/search", response_model=List[schemas.Sweet])
def search_sweets(
    query: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    min_price: Optional[float] = Query(None),
    max_price: Optional[float] = Query(None),
    db: Session = Depends(get_db)
):
    sweets = crud.search_sweets(
        db, 
        query=query, 
        category=category, 
        min_price=min_price, 
        max_price=max_price
    )
    return sweets

@app.get("/api/sweets/{sweet_id}", response_model=schemas.Sweet)
def read_sweet(sweet: models.Sweet = Depends(dependencies.get_sweet_or_404)):
    return sweet

@app.put("/api/sweets/{sweet_id}", response_model=schemas.Sweet)
def update_sweet(
    sweet_update: schemas.SweetUpdate,
    sweet: models.Sweet = Depends(dependencies.get_sweet_or_404),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_admin_user)
):
    return crud.update_sweet(db=db, sweet_id=sweet.id, sweet_update=sweet_update)

@app.delete("/api/sweets/{sweet_id}")
def delete_sweet(
    sweet: models.Sweet = Depends(dependencies.get_sweet_or_404),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_admin_user)
):
    crud.delete_sweet(db=db, sweet_id=sweet.id)
    return {"message": "Sweet deleted successfully"}

# Purchase endpoints
@app.post("/api/sweets/{sweet_id}/purchase", response_model=schemas.Purchase)
def purchase_sweet(
    purchase: schemas.PurchaseCreate,
    sweet: models.Sweet = Depends(dependencies.get_sweet_or_404),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    result = crud.purchase_sweet(db, sweet.id, current_user.id, purchase.quantity)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Not enough stock available"
        )
    return result

@app.post("/api/sweets/{sweet_id}/restock", response_model=schemas.Sweet)
def restock_sweet(
    restock: schemas.RestockRequest,
    sweet: models.Sweet = Depends(dependencies.get_sweet_or_404),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_admin_user)
):
    result = crud.restock_sweet(db, sweet.id, restock.quantity)
    return result

@app.get("/api/purchases", response_model=List[schemas.Purchase])
def get_my_purchases(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    return crud.get_user_purchases(db, current_user.id)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)