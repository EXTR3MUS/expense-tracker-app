from sqlalchemy import Column, Integer, String, Numeric, Text, CheckConstraint, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class Category(Base):
    __tablename__ = "category"
    
    category_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, nullable=False, unique=True)
    
    # Relacionamento
    transactions = relationship("Transaction", back_populates="category")


class Transaction(Base):
    __tablename__ = "transactions"
    
    transaction_id = Column(Integer, primary_key=True, autoincrement=True)
    amount = Column(Numeric(10, 2), nullable=False)
    description = Column(Text)
    date = Column(DateTime, default=datetime.now)
    category_id = Column(Integer, ForeignKey("category.category_id"), nullable=False)
    
    # Relacionamento
    category = relationship("Category", back_populates="transactions")
    
    __table_args__ = (
        CheckConstraint('amount > 0', name='check_amount_positive'),
    )


class Budget(Base):
    __tablename__ = "budget"
    
    budget_id = Column(Integer, primary_key=True)
    total_spent_ever = Column(Numeric(10, 2), default=0)
