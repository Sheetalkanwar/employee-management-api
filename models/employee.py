from pydantic import BaseModel, EmailStr, Field


class Employee(BaseModel):
    id: int = Field(gt=0)
    name: str
    email: EmailStr
    role: str
    salary: float = Field(gt=0)