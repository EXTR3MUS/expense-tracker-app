from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime
from decimal import Decimal

class CategoryBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)

class CategoryResponse(CategoryBase):
    category_id: int
    
    class Config:
        from_attributes = True


class TransactionBase(BaseModel):
    amount: float = Field(..., gt=0)
    description: Optional[str] = None
    category_id: int
    date: Optional[datetime] = None
    
    @validator('amount')
    def validate_amount(cls, v):
        if v <= 0:
            raise ValueError('Amount must be greater than 0')
        return v

class TransactionCreate(TransactionBase):
    pass

class TransactionUpdate(BaseModel):
    amount: Optional[float] = Field(None, gt=0)
    description: Optional[str] = None
    category_id: Optional[int] = None
    date: Optional[datetime] = None
    
    @validator('amount')
    def validate_amount(cls, v):
        if v is not None and v <= 0:
            raise ValueError('Amount must be greater than 0')
        return v

class TransactionResponse(BaseModel):
    transaction_id: int
    amount: float
    description: Optional[str]
    date: datetime
    category_id: int
    category: CategoryResponse
    
    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class BudgetResponse(BaseModel):
    budget_id: int
    total_spent_ever: float
    
    class Config:
        from_attributes = True
