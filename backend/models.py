from sqlalchemy import Column, Integer, String, Float, DateTime, CheckConstraint, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class Category(Base):
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relacionamento
    expenses = relationship("Expense", back_populates="category")
    
    __table_args__ = (
        CheckConstraint('length(name) > 0', name='check_category_name_not_empty'),
    )


class Expense(Base):
    __tablename__ = "expenses"
    
    id = Column(Integer, primary_key=True, index=True)
    description = Column(String(255), nullable=False)
    amount = Column(Float, nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    date = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relacionamento
    category = relationship("Category", back_populates="expenses")
    
    __table_args__ = (
        CheckConstraint('amount > 0', name='check_amount_positive'),
        CheckConstraint('length(description) > 0', name='check_description_not_empty'),
    )
