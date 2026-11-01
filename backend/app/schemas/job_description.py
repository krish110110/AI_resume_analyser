from typing import Optional
from pydantic import BaseModel


class JobDescriptionCreate(BaseModel):
    title: str
    company: Optional[str] = None
    description: str


class JobDescriptionOut(BaseModel):
    id: str
    title: str
    company: Optional[str]
    description: str
    created_at: str

    model_config = {"from_attributes": True}
