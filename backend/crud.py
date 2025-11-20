from sqlalchemy.orm import Session
from sqlalchemy import func, text
from fastapi import HTTPException, status
import models
import schemas
from datetime import datetime

# CRUD de Categorias
def create_category(db: Session, category: schemas.CategoryCreate):
    try:
        db_category = models.Category(**category.dict())
        db.add(db_category)
        db.commit()
        db.refresh(db_category)
        return db_category
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error creating category: {str(e)}"
        )

def get_categories(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Category).offset(skip).limit(limit).all()

def get_category(db: Session, category_id: int):
    category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

def update_category(db: Session, category_id: int, category: schemas.CategoryUpdate):
    db_category = get_category(db, category_id)
    try:
        update_data = category.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_category, key, value)
        db.commit()
        db.refresh(db_category)
        return db_category
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error updating category: {str(e)}"
        )

def delete_category(db: Session, category_id: int):
    db_category = get_category(db, category_id)
    try:
        db.delete(db_category)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error deleting category: {str(e)}"
        )


# CRUD de Despesas
def create_expense(db: Session, expense: schemas.ExpenseCreate):
    # Verificar se a categoria existe
    category = db.query(models.Category).filter(models.Category.id == expense.category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    try:
        expense_data = expense.dict()
        if expense_data['date'] is None:
            expense_data['date'] = datetime.utcnow()
        
        db_expense = models.Expense(**expense_data)
        db.add(db_expense)
        db.commit()
        db.refresh(db_expense)
        return db_expense
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error creating expense: {str(e)}"
        )

def get_expenses(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Expense).offset(skip).limit(limit).all()

def get_expense(db: Session, expense_id: int):
    expense = db.query(models.Expense).filter(models.Expense.id == expense_id).first()
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    return expense

def update_expense(db: Session, expense_id: int, expense: schemas.ExpenseUpdate):
    db_expense = get_expense(db, expense_id)
    
    # Verificar se a categoria existe, caso seja fornecida
    if expense.category_id:
        category = db.query(models.Category).filter(models.Category.id == expense.category_id).first()
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
    
    try:
        update_data = expense.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_expense, key, value)
        db.commit()
        db.refresh(db_expense)
        return db_expense
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error updating expense: {str(e)}"
        )

def delete_expense(db: Session, expense_id: int):
    db_expense = get_expense(db, expense_id)
    try:
        db.delete(db_expense)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error deleting expense: {str(e)}"
        )


# Funções para estatísticas (simulando procedures/views)
def get_expense_summary(db: Session):
    """Simula uma stored procedure que retorna resumo de despesas"""
    total = db.query(func.sum(models.Expense.amount)).scalar() or 0
    count = db.query(func.count(models.Expense.id)).scalar() or 0
    avg = db.query(func.avg(models.Expense.amount)).scalar() or 0
    
    return {
        "total_expenses": float(total),
        "expense_count": count,
        "average_expense": float(avg)
    }

def get_expenses_by_category(db: Session):
    """Simula uma view que agrupa despesas por categoria"""
    results = db.query(
        models.Category.name,
        func.count(models.Expense.id).label('count'),
        func.sum(models.Expense.amount).label('total'),
        func.avg(models.Expense.amount).label('average')
    ).join(models.Expense).group_by(models.Category.id).all()
    
    return [
        {
            "category": r.name,
            "expense_count": r.count,
            "total_amount": float(r.total or 0),
            "average_amount": float(r.average or 0)
        }
        for r in results
    ]
