# app/routes.py

from fastapi import APIRouter

from app.core.views.health import router as health_router
from app.core.views.home import router as home_router
from app.core.views.aws_accounts import router as aws_accounts_router
from app.snapshots.views import router as snapshots_router
from app.s3_buckets.views import router as s3_buckets_router

main_router = APIRouter()

# include views
main_router.include_router(health_router, tags=["health"], include_in_schema=False)
main_router.include_router(home_router, tags=["home"], include_in_schema=False)
main_router.include_router(snapshots_router, tags=["snapshots"], include_in_schema=False)
main_router.include_router(s3_buckets_router, tags=["s3_buckets"], include_in_schema=False)


main_router.include_router(aws_accounts_router, prefix="/api/v1/aws-accounts", tags=["AWS Accounts"])
