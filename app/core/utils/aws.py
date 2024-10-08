import boto3
from botocore.exceptions import BotoCoreError, NoCredentialsError
from app.core.utils.logging import logger

def assume_role(account_id: str, role_arn: str, role_session_name: str = "cross-account-session"):
    """
    Assume a role in another AWS account and return temporary credentials.
    
    Args:
        account_id (str): AWS account ID to assume the role in.
        role_arn (str): The ARN of the role to assume.
        role_session_name (str): Name of the session for the assumed role.
    
    Returns:
        dict: Temporary credentials for assumed role.
    """
    try:
        logger.info(f"Attempting to assume role for account {account_id} using role {role_arn}")
        sts_client = boto3.client('sts')

        # Assume the role in the target account
        assumed_role = sts_client.assume_role(
            RoleArn=role_arn,
            RoleSessionName=role_session_name
        )

        # Return the temporary credentials
        return assumed_role['Credentials']
    
    except (BotoCoreError, NoCredentialsError) as e:
        logger.error(f"Error assuming role in account {account_id}: {e}")
        raise

def get_boto3_client(service_name: str, creds: dict = None, region_name: str = "us-east-1"):
    """
    Get a boto3 client using optional assumed role credentials. If no credentials are provided,
    it defaults to the environment or instance profile credentials.
    
    Args:
        service_name (str): AWS service (e.g., 's3', 'rds').
        creds (dict, optional): Temporary credentials obtained by assume_role. Defaults to None.
        region_name (str): AWS region to use for the client. Defaults to 'us-east-1'.
    
    Returns:
        boto3.client: Boto3 client for the specified service.
    """
    if creds:
        return boto3.client(
            service_name,
            aws_access_key_id=creds['AccessKeyId'],
            aws_secret_access_key=creds['SecretAccessKey'],
            aws_session_token=creds['SessionToken'],
            region_name=region_name
        )
    else:
        # Use default credentials from environment, instance profile, or IAM role
        return boto3.client(service_name, region_name=region_name)