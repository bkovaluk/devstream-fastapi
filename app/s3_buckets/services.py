# app/s3_buckets/services.py

from app.core.utils.aws import get_boto3_client
from app.s3_buckets.schemas import S3BucketCreate
from app.core.utils.logging import logger
from app.core.config import templates

def generate_s3_policy(bucket_name: str, account_id: str) -> str:
    """Generate a default S3 bucket access policy from a Jinja2 template."""
    template = templates.get_template("policies/s3_bucket_policy.j2")
    return template.render(bucket_name=bucket_name)

def create_s3_bucket(s3_bucket_data: S3BucketCreate) -> dict:
    """Create an S3 bucket with specified encryption and policy."""
    try:
        s3_client = get_boto3_client('s3', region=s3_bucket_data.region)
        bucket_name = s3_bucket_data.bucket_name
        
        # Create the bucket
        s3_client.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={'LocationConstraint': s3_bucket_data.region}
        )
        logger.info(f"S3 Bucket {bucket_name} created successfully.")

        # Apply encryption
        if s3_bucket_data.encryption_type == 'kms':
            s3_client.put_bucket_encryption(
                Bucket=bucket_name,
                ServerSideEncryptionConfiguration={
                    'Rules': [{
                        'ApplyServerSideEncryptionByDefault': {
                            'SSEAlgorithm': 'aws:kms',
                            'KMSMasterKeyID': s3_bucket_data.kms_alias
                        }
                    }]
                }
            )
        elif s3_bucket_data.encryption_type == 's3':
            s3_client.put_bucket_encryption(
                Bucket=bucket_name,
                ServerSideEncryptionConfiguration={
                    'Rules': [{
                        'ApplyServerSideEncryptionByDefault': {
                            'SSEAlgorithm': 'AES256'
                        }
                    }]
                }
            )
        
        # Generate and apply policy
        policy = generate_s3_policy(bucket_name, s3_bucket_data.account_id)
        s3_client.put_bucket_policy(Bucket=bucket_name, Policy=policy)
        logger.info(f"Policy applied to {bucket_name}.")
        
        return {"status": "success", "bucket_name": bucket_name}
    except Exception as e:
        logger.error(f"Error creating S3 bucket: {e}")
        raise
