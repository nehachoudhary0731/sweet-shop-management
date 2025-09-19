from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_admin: bool
    created_at: datetime
    
    class Config:
        orm_mode = True

class SweetBase(BaseModel):
    name: str
    description: Optional[str] = None
    category: str
    price: float
    quantity: int

class SweetCreate(SweetBase):
    pass

class SweetUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    price: Optional[float] = None
    quantity: Optional[int] = None

class Sweet(SweetBase):
    id: int
    image_url: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        orm_mode = True

class PurchaseBase(BaseModel):
    sweet_id: int
    quantity: int

class PurchaseCreate(PurchaseBase):
    pass

class Purchase(PurchaseBase):
    id: int
    user_id: int
    total_price: float
    created_at: datetime
    sweet: Sweet
    
    class Config:
        orm_mode = True

class RestockRequest(BaseModel):
    quantity: int