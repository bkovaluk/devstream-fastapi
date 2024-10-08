# app/s3_buckets/views.py

from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.db import get_db
from app.core.models.aws_accounts import AWSAccount
from app.s3_buckets.schemas import S3BucketCreate
from app.s3_buckets.services import create_s3_bucket
from app.core.config import templates

router = APIRouter()

@router.get("/s3-buckets", response_class=HTMLResponse)
async def create_s3_bucket_form(request: Request, db: AsyncSession = Depends(get_db)):
    # Fetch AWS accounts for the dropdown
    result = await db.execute(select(AWSAccount))
    aws_accounts = result.scalars().all()

    is_htmx = request.headers.get("HX-Request") is not None
    return templates.TemplateResponse("pages/s3_buckets.html", {"request": request, "aws_accounts": aws_accounts, "is_htmx": is_htmx})

@router.post("/s3-buckets", response_class=HTMLResponse)
async def create_s3_bucket_view(
        request: Request,
        account_id: str = Form(...),
        bucket_name: str = Form(...),
        region: str = Form(...),
        encryption_type: str = Form(...),
        kms_alias: str = Form(None),
        db: AsyncSession = Depends(get_db)
    ):
    # Call the service to create the S3 bucket
    s3_bucket_data = S3BucketCreate(
        account_id=account_id,
        bucket_name=bucket_name,
        region=region,
        encryption_type=encryption_type,
        kms_alias=kms_alias
    )
    try:
        response = create_s3_bucket(s3_bucket_data)
        return templates.TemplateResponse("partials/s3_bucket_card.html", {"request": request, "bucket": response})
    except Exception as e:
        return templates.TemplateResponse("pages/s3_buckets.html", {"request": request, "error": str(e)})
