# app/schemas/db_snapshots.py

from pydantic import BaseModel
from typing import Optional

class SnapshotBase(BaseModel):
    snapshot_id: str
    target_region: str
    target_account_id: Optional[str] = None
    kms_key_id: Optional[str] = None

class SnapshotCreate(SnapshotBase):
    pass

class SnapshotResponse(SnapshotBase):
    id: int
    status: str

    class Config:
        from_attributes = True
