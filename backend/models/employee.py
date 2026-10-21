
from pydantic import BaseModel, EmailStr, Field


class Employee(BaseModel):
    id: int = Field(gt=0)
    name: str = Field(min_length=1)
    email: EmailStr
    role: str = Field(min_length=1)
    salary: float = Field(ge=0)
