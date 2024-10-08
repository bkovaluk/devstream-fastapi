# app/core/models/aws_accounts.py

from sqlalchemy import Column, Integer, String, Text, DateTime, func
from app.sql.alembic import ModelBase

class AWSAccount(ModelBase):
    __tablename__ = "aws_accounts"

    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(String(12), nullable=False, unique=True)
    role_arn = Column(String(255), nullable=False)
    alias = Column(String(50))
    description = Column(Text, nullable=True)
    environment = Column(String(50), nullable=True)
    created_at = Column(DateTime, default=func.now())
