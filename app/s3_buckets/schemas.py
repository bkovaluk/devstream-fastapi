# app/s3_buckets/schemas.py

from pydantic import BaseModel, constr
from typing import Optional

class S3BucketBase(BaseModel):
    account_id: constr(pattern=r'^\d{12}$')
    bucket_name: str
    region: str
    encryption_type: str
    kms_alias: Optional[str] = None

class S3BucketCreate(S3BucketBase):
    pass

class S3BucketResponse(S3BucketBase):
    id: int
    policy: str

    class Config:
        orm_mode = True
