from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError

from app.core.models.aws_accounts import AWSAccount
from app.core.schemas.aws_accounts import AWSAccountCreate
from app.core.utils.logging import logger


async def create_aws_account(
    db: AsyncSession, account: AWSAccountCreate
) -> AWSAccount:
    """
    Create a new AWS account record in the database.
    
    Args:
        db (AsyncSession): SQLAlchemy async session.
        account_id (str): The AWS account ID.
        role_arn (str): The IAM role ARN to assume.
        alias (str): Alias for the account (e.g., core-dev, tools-prod).
        description (str): Optional description of the AWS account.
        environment (str): Environment label (e.g., dev, prod, qa).
    
    Returns:
        AWSAccount: The newly created AWS account object.
    """
    try:
        new_account = AWSAccount(
            account_id=account.account_id,
            role_arn=account.role_arn,
            alias=account.alias,
            description=account.description,
            environment=account.environment
        )
        db.add(new_account)
        await db.commit()
        await db.refresh(new_account)
        logger.info(f"AWS account {new_account.account_id} added with role {new_account.role_arn}.")
        return new_account
    except SQLAlchemyError as e:
        logger.error(f"Error creating AWS account: {e}", exc_info=True)
        await db.rollback()
        raise

async def get_aws_account(db: AsyncSession, account_id: str = None) -> list[AWSAccount] | AWSAccount | None:
    """
    Retrieve an AWS account by its account ID or return all AWS accounts if no account ID is provided.
    
    Args:
        db (AsyncSession): SQLAlchemy async session.
        account_id (str, optional): The AWS account ID to retrieve. If None, return all accounts.
    
    Returns:
        AWSAccount: A single AWS account object if an ID is provided, or a list of all AWS accounts.
    """
    try:
        if account_id:
            # Fetch a single account
            result = await db.execute(select(AWSAccount).where(AWSAccount.account_id == account_id))
            account = result.scalars().first()
            if account:
                logger.info(f"AWS account found: {account.account_id}")
            else:
                logger.warning(f"AWS account {account_id} not found.")
            return account
        else:
            # Fetch all accounts
            result = await db.execute(select(AWSAccount))
            accounts = result.scalars().all()
            logger.info(f"Fetched {len(accounts)} AWS accounts.")
            return accounts
    except SQLAlchemyError as e:
        logger.error(f"Error fetching AWS accounts: {e}", exc_info=True)
        raise


async def update_aws_account(
    db: AsyncSession, account_id: str, role_arn: str = None, alias: str = None, description: str = None, environment: str = None
) -> AWSAccount:
    """
    Update an existing AWS account record in the database.
    
    Args:
        db (AsyncSession): SQLAlchemy async session.
        account_id (str): The AWS account ID to update.
        role_arn (str, optional): Updated IAM role ARN.
        alias (str, optional): Updated alias for the account.
        description (str, optional): Updated description.
        environment (str, optional): Updated environment label.
    
    Returns:
        AWSAccount: The updated AWS account object.
    """
    try:
        account = await get_aws_account(db, account_id)
        if not account:
            raise ValueError(f"AWS account {account_id} not found.")
        
        if role_arn:
            account.role_arn = role_arn
        if alias:
            account.alias = alias
        if description:
            account.description = description
        if environment:
            account.environment = environment
        
        await db.commit()
        await db.refresh(account)
        logger.info(f"AWS account {account_id} updated.")
        return account
    except SQLAlchemyError as e:
        logger.error(f"Error updating AWS account {account_id}: {e}", exc_info=True)
        await db.rollback()
        raise
    except ValueError as ve:
        logger.error(f"Validation error: {ve}")
        raise

async def delete_aws_account(db: AsyncSession, account_id: str) -> bool:
    """
    Delete an AWS account record from the database.
    
    Args:
        db (AsyncSession): SQLAlchemy async session.
        account_id (str): The AWS account ID to delete.
    
    Returns:
        bool: True if the account was deleted, False otherwise.
    """
    try:
        account = await get_aws_account(db, account_id)
        if not account:
            raise ValueError(f"AWS account {account_id} not found.")
        
        await db.delete(account)
        await db.commit()
        logger.info(f"AWS account {account_id} deleted.")
        return True
    except SQLAlchemyError as e:
        logger.error(f"Error deleting AWS account {account_id}: {e}", exc_info=True)
        await db.rollback()
        raise
    except ValueError as ve:
        logger.error(f"Validation error: {ve}")
        raise
