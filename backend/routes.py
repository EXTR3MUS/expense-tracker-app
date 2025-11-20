from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
import models
import schemas
import crud

router = APIRouter()

# Rotas de Categorias
@router.post("/categories", response_model=schemas.CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(category: schemas.CategoryCreate, db: Session = Depends(get_db)):
    return crud.create_category(db=db, category=category)

@router.get("/categories", response_model=List[schemas.CategoryResponse])
def read_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_categories(db=db, skip=skip, limit=limit)

@router.get("/categories/{category_id}", response_model=schemas.CategoryResponse)
def read_category(category_id: int, db: Session = Depends(get_db)):
    category = crud.get_category(db=db, category_id=category_id)
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.put("/categories/{category_id}", response_model=schemas.CategoryResponse)
def update_category(category_id: int, category: schemas.CategoryUpdate, db: Session = Depends(get_db)):
    return crud.update_category(db=db, category_id=category_id, category=category)

@router.delete("/categories/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: int, db: Session = Depends(get_db)):
    crud.delete_category(db=db, category_id=category_id)
    return None


# Rotas de Transações
@router.post("/transactions", response_model=schemas.TransactionResponse, status_code=status.HTTP_201_CREATED)
def create_transaction(transaction: schemas.TransactionCreate, db: Session = Depends(get_db)):
    return crud.create_transaction(db=db, transaction=transaction)

@router.get("/transactions", response_model=List[schemas.TransactionResponse])
def read_transactions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_transactions(db=db, skip=skip, limit=limit)

@router.get("/transactions/{transaction_id}", response_model=schemas.TransactionResponse)
def read_transaction(transaction_id: int, db: Session = Depends(get_db)):
    transaction = crud.get_transaction(db=db, transaction_id=transaction_id)
    if transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction

@router.put("/transactions/{transaction_id}", response_model=schemas.TransactionResponse)
def update_transaction(transaction_id: int, transaction: schemas.TransactionUpdate, db: Session = Depends(get_db)):
    return crud.update_transaction(db=db, transaction_id=transaction_id, transaction=transaction)

@router.delete("/transactions/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_transaction(transaction_id: int, db: Session = Depends(get_db)):
    crud.delete_transaction(db=db, transaction_id=transaction_id)
    return None


# Rotas para estatísticas
@router.get("/statistics/monthly")
def get_monthly_statistics(db: Session = Depends(get_db)):
    return crud.get_monthly_summary(db=db)

@router.get("/statistics/budget")
def get_budget(db: Session = Depends(get_db)):
    return crud.get_budget_info(db=db)

@router.get("/statistics/by-category")
def get_category_statistics(db: Session = Depends(get_db)):
    return crud.get_transactions_by_category(db=db)


# Rota para audit logs
@router.get("/audit-logs")
def get_audit_logs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_audit_logs(db=db, skip=skip, limit=limit)
