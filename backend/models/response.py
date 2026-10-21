
from pydantic import BaseModel
from models.employee import Employee


class EmployeeResponse(BaseModel):
    message: str
    employee_id: str


class MessageResponse(BaseModel):
    message: str


class EmployeeListResponse(BaseModel):
    employees: list[Employee]
