from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from .database import get_db
from . import crud, models

def get_sweet_or_404(sweet_id: int, db: Session = Depends(get_db)):
    sweet = crud.get_sweet(db, sweet_id=sweet_id)
    if sweet is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sweet not found"
        )
    return sweet