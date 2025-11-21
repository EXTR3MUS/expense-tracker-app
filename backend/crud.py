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
    category = db.query(models.Category).filter(models.Category.category_id == category_id).first()
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


# CRUD de Transações
def create_transaction(db: Session, transaction: schemas.TransactionCreate):
    # Verificar se a categoria existe
    category = db.query(models.Category).filter(models.Category.category_id == transaction.category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    try:
        transaction_data = transaction.dict()
        if transaction_data['date'] is None:
            transaction_data['date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        db_transaction = models.Transaction(**transaction_data)
        db.add(db_transaction)
        db.commit()
        db.refresh(db_transaction)
        return db_transaction
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error creating transaction: {str(e)}"
        )

def get_transactions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Transaction).offset(skip).limit(limit).all()

def get_transaction(db: Session, transaction_id: int):
    transaction = db.query(models.Transaction).filter(models.Transaction.transaction_id == transaction_id).first()
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction

def update_transaction(db: Session, transaction_id: int, transaction: schemas.TransactionUpdate):
    db_transaction = get_transaction(db, transaction_id)
    
    # Verificar se a categoria existe, caso seja fornecida
    if transaction.category_id:
        category = db.query(models.Category).filter(models.Category.category_id == transaction.category_id).first()
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
    
    try:
        update_data = transaction.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_transaction, key, value)
        db.commit()
        db.refresh(db_transaction)
        return db_transaction
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error updating transaction: {str(e)}"
        )

def delete_transaction(db: Session, transaction_id: int):
    db_transaction = get_transaction(db, transaction_id)
    try:
        db.delete(db_transaction)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error deleting transaction: {str(e)}"
        )


# Funções para estatísticas (usando a VIEW e stored procedures)
def get_monthly_summary(db: Session):
    """Usa a VIEW View_Monthly_Summary"""
    result = db.execute(text("SELECT * FROM View_Monthly_Summary LIMIT 12"))
    return [
        {
            "month": row[0],
            "total_expenses": float(row[1] or 0)
        }
        for row in result
    ]

def get_budget_info(db: Session):
    """Retorna informações do budget (atualizado via trigger)"""
    budget = db.query(models.Budget).filter(models.Budget.budget_id == 1).first()
    if not budget:
        # Criar budget inicial se não existir
        budget = models.Budget(budget_id=1, total_spent_ever=0)
        db.add(budget)
        db.commit()
        db.refresh(budget)
    return budget

def get_transactions_by_category(db: Session):
    """Usa stored procedure get_expenses_by_category()"""
    result = db.execute(text("SELECT * FROM get_expenses_by_category()"))
    
    return [
        {
            "category": row[0],
            "transaction_count": int(row[1] or 0),
            "total_amount": float(row[2] or 0),
            "average_amount": float(row[3] or 0)
        }
        for row in result
    ]


def get_audit_logs(db: Session, skip: int = 0, limit: int = 100):
    """Retorna logs de auditoria das transações"""
    result = db.execute(text("""
        SELECT * FROM Transaction_Log 
        ORDER BY log_timestamp DESC 
        LIMIT :limit OFFSET :skip
    """), {"limit": limit, "skip": skip})
    
    columns = ['log_id', 'operation', 'transaction_id', 
               'old_amount', 'new_amount', 
               'old_description', 'new_description',
               'old_date', 'new_date',
               'old_category_id', 'new_category_id',
               'log_timestamp']
    
    return [
        {col: row[i] for i, col in enumerate(columns)}
        for row in result
    ]
