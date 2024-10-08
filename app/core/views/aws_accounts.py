from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.core.schemas.aws_accounts import AWSAccountCreate, AWSAccountUpdate, AWSAccountResponse
from app.core.services.aws_accounts import (
    create_aws_account,
    update_aws_account,
    delete_aws_account,
    get_aws_account,
)
from app.core.db import get_db

router = APIRouter()

@router.post("/", response_model=AWSAccountResponse)
async def create_account(account: AWSAccountCreate, db: AsyncSession = Depends(get_db)):
    return await create_aws_account(db, account)

@router.get("/", response_model=List[AWSAccountResponse])
async def read_accounts(db: AsyncSession = Depends(get_db)):
    return await get_aws_account(db)

@router.get("/{account_id}", response_model=AWSAccountResponse)
async def read_account(account_id: int, db: AsyncSession = Depends(get_db)):
    account = await get_aws_account(db, account_id)
    if not account:
        raise HTTPException(status_code=404, detail="AWS Account not found")
    return account

@router.put("/{account_id}", response_model=AWSAccountResponse)
async def update_account(account_id: int, account: AWSAccountUpdate, db: AsyncSession = Depends(get_db)):
    return await update_aws_account(db, account_id, account)

@router.delete("/{account_id}")
async def delete_account(account_id: int, db: AsyncSession = Depends(get_db)):
    deleted = await delete_aws_account(db, account_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="AWS Account not found")
    return {"status": "success", "message": "AWS Account deleted successfully"}
