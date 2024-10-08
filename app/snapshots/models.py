# app/models/db_snapshots.py

from sqlalchemy import Column, String, Integer

from app.sql.alembic import ModelBase

class Snapshot(ModelBase):
    __tablename__ = "snapshots"

    id = Column(Integer, primary_key=True, index=True)
    snapshot_id = Column(String, unique=True, index=True)
    target_account_id = Column(String, nullable=True)
    target_region = Column(String, nullable=False)
    status = Column(String, default="pending")
    kms_key_id = Column(String, nullable=True)
