# app/snapshots/services.py

from app.core.utils.aws import get_boto3_client
from app.core.utils.logging import logger

async def create_snapshot_service(snapshot_id, target_account_id, target_region, kms_key_id=None):
    """
    Service to create and copy an RDS or RDS cluster snapshot.
    """
    try:
        # Use the shared utility to get the AWS client, assuming the role if necessary
        rds_client = await get_boto3_client(
            service_name='rds',
            region_name=target_region,
            account_id=target_account_id
        )

        if "cluster" in snapshot_id:
            response = rds_client.copy_db_cluster_snapshot(
                SourceDBClusterSnapshotIdentifier=snapshot_id,
                TargetDBClusterSnapshotIdentifier=f"copy-{snapshot_id}",
                SourceRegion='us-east-1',
                KmsKeyId=kms_key_id if kms_key_id else None,
                CopyTags=True,
            )
            copy_snapshot_id = response['DBClusterSnapshot']['DBClusterSnapshotIdentifier']
            waiter = rds_client.get_waiter('db_cluster_snapshot_available')
        else:
            response = rds_client.copy_db_snapshot(
                SourceDBSnapshotIdentifier=snapshot_id,
                TargetDBSnapshotIdentifier=f"copy-{snapshot_id}",
                SourceRegion='us-east-1',
                KmsKeyId=kms_key_id if kms_key_id else None,
                CopyTags=True,
            )
            copy_snapshot_id = response['DBSnapshot']['DBSnapshotIdentifier']
            waiter = rds_client.get_waiter('db_snapshot_completed')

        # Wait for the snapshot copy process to complete
        waiter.wait(
            DBSnapshotIdentifier=copy_snapshot_id if "cluster" not in snapshot_id else None,
            DBClusterSnapshotIdentifier=copy_snapshot_id if "cluster" in snapshot_id else None
        )

        logger.info(f"Snapshot {copy_snapshot_id} copied successfully.")
        return {"status": "completed", "snapshot_id": copy_snapshot_id}

    except Exception as e:
        logger.error(f"Error copying snapshot {snapshot_id}: {e}")
        raise


async def share_snapshot_service(snapshot_id, target_account_ids):
    """
    Service to share an RDS or RDS cluster snapshot with other AWS accounts.
    """
    try:
        # Use the shared utility to get the AWS client, no role assumed here (IAM is global)
        rds_client = await get_boto3_client(
            service_name='rds',
            region_name='us-east-1'
        )

        for account_id in target_account_ids:
            if "cluster" in snapshot_id:
                rds_client.modify_db_cluster_snapshot_attribute(
                    DBClusterSnapshotIdentifier=snapshot_id,
                    AttributeName='restore',
                    ValuesToAdd=[account_id]
                )
            else:
                rds_client.modify_db_snapshot_attribute(
                    DBSnapshotIdentifier=snapshot_id,
                    AttributeName='restore',
                    ValuesToAdd=[account_id]
                )
            logger.info(f"Snapshot {snapshot_id} shared with account {account_id}")

        return {"status": "success", "snapshot_id": snapshot_id, "shared_with": target_account_ids}

    except Exception as e:
        logger.error(f"Error sharing snapshot {snapshot_id}: {e}")
        raise
