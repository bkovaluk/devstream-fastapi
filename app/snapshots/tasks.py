#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script: tasks.py
Description: Celery tasks for handling snapshot operations (copying and sharing RDS and RDS cluster snapshots) across AWS accounts and regions.

Tasks:
    - copy_snapshot: Copies an AWS RDS or RDS cluster snapshot to a different region or account.
    - share_snapshot: Shares an AWS RDS or RDS cluster snapshot with other AWS accounts.

Usage:
    These tasks are run asynchronously via Celery workers.

"""

__author__ = "Bradley Kovaluk"
__version__ = "1.1"
__date__ = "2024-09-25"

from celery import shared_task
from app.core.utils.logging import logger
from app.snapshots.services import create_snapshot_service, share_snapshot_service

@shared_task(bind=True)
def copy_snapshot(self, snapshot_id, target_account_id, target_region, kms_key_id=None):
    """
    Task to copy an RDS snapshot or RDS cluster snapshot across AWS accounts or regions.

    Args:
        snapshot_id (str): ID of the RDS or RDS cluster snapshot to be copied.
        target_account_id (str): ID of the target AWS account.
        target_region (str): The AWS region to which the snapshot is being copied.
        kms_key_id (str): Optional KMS key for encryption.
    
    Returns:
        dict: Result of the snapshot copy process.
    """
    try:
        # Delegate the snapshot copy operation to the service
        result = create_snapshot_service(snapshot_id, target_account_id, target_region, kms_key_id)
        logger.info(f"Snapshot copy task completed for {snapshot_id}")
        return result

    except Exception as e:
        logger.error(f"Snapshot copy task failed for {snapshot_id}: {e}")
        self.retry(exc=e, countdown=60, max_retries=3)
        return {"status": "failed", "error": str(e)}

@shared_task(bind=True)
def share_snapshot(self, snapshot_id, target_account_ids):
    """
    Task to share an RDS snapshot or RDS cluster snapshot with other AWS accounts by modifying its attributes.

    Args:
        snapshot_id (str): ID of the snapshot to be shared.
        target_account_ids (list): List of AWS account IDs to share the snapshot with.

    Returns:
        dict: Result of the snapshot sharing process.
    """
    try:
        # Delegate the snapshot sharing operation to the service
        result = share_snapshot_service(snapshot_id, target_account_ids)
        logger.info(f"Snapshot sharing task completed for {snapshot_id}")
        return result

    except Exception as e:
        logger.error(f"Snapshot sharing task failed for {snapshot_id}: {e}")
        self.retry(exc=e, countdown=60, max_retries=3)
        return {"status": "failed", "error": str(e)}
