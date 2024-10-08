from pydantic import BaseModel, constr
from typing import Optional


class AWSAccountBase(BaseModel):
    account_id: constr(pattern=r'^\d{12}$')
    role_arn: str
    alias: Optional[str] = None
    description: Optional[str] = None
    environment: Optional[str] = None

    class Config:
        from_attributes = True
        
class AWSAccountCreate(AWSAccountBase):
    pass

class AWSAccountUpdate(AWSAccountBase):
    pass

class AWSAccountResponse(AWSAccountBase):
    id: int
