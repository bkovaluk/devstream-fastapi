# app/s3_buckets/models.py

from sqlalchemy import Column, String, Boolean, Integer

from app.sql.alembic import ModelBase

class S3Bucket(ModelBase):
    __tablename__ = "s3_buckets"

    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(String, index=True)
    bucket_name = Column(String, unique=True, index=True)
    region = Column(String)
    encryption_type = Column(String)
    kms_alias = Column(String, nullable=True)
    policy = Column(String)
