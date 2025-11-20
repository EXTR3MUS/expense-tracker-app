from sqlalchemy import Column, Integer, String, Float, Text, CheckConstraint, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class Category(Base):
    __tablename__ = "Category"
    
    category_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, nullable=False, unique=True)
    
    # Relacionamento
    transactions = relationship("Transaction", back_populates="category")


class Transaction(Base):
    __tablename__ = "Transactions"
    
    transaction_id = Column(Integer, primary_key=True, autoincrement=True)
    amount = Column(Float, nullable=False)
    description = Column(Text)
    date = Column(Text, default=lambda: datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    category_id = Column(Integer, ForeignKey("Category.category_id"), nullable=False)
    
    # Relacionamento
    category = relationship("Category", back_populates="transactions")
    
    __table_args__ = (
        CheckConstraint('amount > 0', name='check_amount_positive'),
    )


class Budget(Base):
    __tablename__ = "Budget"
    
    budget_id = Column(Integer, primary_key=True)
    total_spent_ever = Column(Float, default=0)
