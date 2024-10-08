# app/snapshots/views.py

from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.config import templates
from app.core.db import get_db

from app.snapshots.models import Snapshot
from app.snapshots.schemas import SnapshotCreate
from app.snapshots.tasks import copy_snapshot

router = APIRouter()

@router.get("/snapshots", response_class=HTMLResponse)
async def read_snapshots(request: Request, db: AsyncSession = Depends(get_db)):
    # Fetch all snapshots to display
    result = await db.execute(select(Snapshot))
    snapshots = result.scalars().all()
    
    is_htmx = request.headers.get("HX-Request") is not None
    return templates.TemplateResponse("pages/snapshots.html", {"request": request, "snapshots": snapshots, "is_htmx": is_htmx})

@router.post("/snapshots/create", response_class=HTMLResponse)
async def create_snapshot_view(
        request: Request,
        snapshot_id: str = Form(..., description="The ID of the snapshot to copy."),
        target_region: str = Form(..., description="The target AWS region for the snapshot."),
        target_account_id: str = Form(None, description="The AWS account ID to copy the snapshot to."),
        kms_key_id: str = Form(None, description="Optional KMS key for encryption."),
        db: AsyncSession = Depends(get_db)
    ):
    
    if not snapshot_id or not target_region:
        return templates.TemplateResponse("pages/snapshots.html", {"request": request, "error": "Snapshot ID and target region are required."})

    # Prepare snapshot data
    snapshot_data = SnapshotCreate(
        snapshot_id=snapshot_id,
        target_region=target_region,
        target_account_id=target_account_id,
        kms_key_id=kms_key_id,
    )

    try:
        # Instead of directly creating the snapshot, trigger the Celery task
        task = copy_snapshot.delay(snapshot_id, target_account_id, target_region, kms_key_id=kms_key_id)

        return templates.TemplateResponse(
            "partials/snapshot_card.html", 
            {"request": request, "snapshot": snapshot_data, "task_id": task.id}
        )
    except Exception as e:
        return templates.TemplateResponse("pages/snapshots.html", {"request": request, "error": str(e)})
    