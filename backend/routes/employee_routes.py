
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import text

from auth import get_current_user, require_admin
from database import engine
from models.employee import Employee
from models.response import EmployeeResponse, MessageResponse, EmployeeListResponse

router = APIRouter(prefix="/employees", tags=["Employees"])


def fetch_employees(query, params=None):
    with engine.connect() as connection:
        rows = connection.execute(text(query), params or {}).mappings().all()
        return [dict(row) for row in rows]


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=EmployeeResponse,
    summary="Create a new employee",
)
def add_employee(
    employee: Employee,
    current_user: dict = Depends(require_admin),
):
    data = employee.model_dump()

    with engine.begin() as connection:
        existing = connection.execute(
            text("SELECT id FROM employees WHERE id = :id"),
            {"id": data["id"]},
        ).first()

        if existing:
            raise HTTPException(
                status_code=400,
                detail="Employee ID already exists",
            )

        connection.execute(
            text("""
                INSERT INTO employees (id, name, email, role, salary)
                VALUES (:id, :name, :email, :role, :salary)
            """),
            data,
        )

    return {
    "message": "Employee added successfully!",
    "employee_id": str(data["id"]),
}


@router.get(
    "",
    response_model=EmployeeListResponse,
    summary="Get all employees",
)
def get_employees(
    page: int = 1,
    limit: int = 5,
    sort_by: str = "id",
    order: str = "asc",
    current_user: dict = Depends(get_current_user),
):
    if page < 1:
        raise HTTPException(status_code=400, detail="Page must be at least 1")
    if limit < 1 or limit > 100:
        raise HTTPException(status_code=400, detail="Limit must be between 1 and 100")

    allowed_sort_fields = {"id", "name", "salary", "role"}
    if sort_by not in allowed_sort_fields:
        raise HTTPException(status_code=400, detail="Invalid sort field")
    if order not in {"asc", "desc"}:
        raise HTTPException(status_code=400, detail="Order must be asc or desc")

    offset = (page - 1) * limit
    employees = fetch_employees(
      f"SELECT id, name, email, role, salary FROM employees "
      f"ORDER BY {sort_by} {order.upper()} LIMIT :limit OFFSET :offset",
      {"limit": limit, "offset": offset},
)

    return {"employees": employees}


@router.get("/search", summary="Search employees with multiple filters")
def search_employees(
    name: str | None = None,
    role: str | None = None,
    minimum_salary: float | None = None,
    current_user: dict = Depends(get_current_user),
):
    conditions = []
    params = {}

    if name:
        conditions.append("name ILIKE :name")
        params["name"] = f"%{name}%"
    if role:
        conditions.append("role ILIKE :role")
        params["role"] = role
    if minimum_salary is not None:
        conditions.append("salary >= :minimum_salary")
        params["minimum_salary"] = minimum_salary

    where = " WHERE " + " AND ".join(conditions) if conditions else ""
    return fetch_employees(
        "SELECT id, name, email, role, salary FROM employees" + where + " ORDER BY id",
        params,
    )


@router.get("/role/{role}", summary="Get employees by role")
def get_employees_by_role(
    role: str,
    current_user: dict = Depends(get_current_user),
):
    return fetch_employees(
        "SELECT id, name, email, role, salary FROM employees WHERE role ILIKE :role ORDER BY id",
        {"role": role},
    )


@router.get("/search/{name}", summary="Search employees by name")
def search_employees_by_name(
    name: str,
    current_user: dict = Depends(get_current_user),
):
    return fetch_employees(
        "SELECT id, name, email, role, salary FROM employees WHERE name ILIKE :name ORDER BY id",
        {"name": f"%{name}%"},
    )


@router.get("/salary/{minimum_salary}", summary="Get employees by minimum salary")
def get_employees_by_salary(
    minimum_salary: float,
    current_user: dict = Depends(get_current_user),
):
    return fetch_employees(
        "SELECT id, name, email, role, salary FROM employees WHERE salary >= :salary ORDER BY id",
        {"salary": minimum_salary},
    )


@router.get("/{employee_id}", summary="Get employee by ID")
def get_employee(
    employee_id: int,
    current_user: dict = Depends(get_current_user),
):
    employees = fetch_employees(
        "SELECT id, name, email, role, salary FROM employees WHERE id = :id",
        {"id": employee_id},
    )
    if not employees:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employees[0]


@router.put(
    "/{employee_id}",
    response_model=MessageResponse,
    summary="Update an employee",
)
def update_employee(
    employee_id: int,
    employee: Employee,
    current_user: dict = Depends(require_admin),
):
    data = employee.model_dump()
    data["employee_id"] = employee_id

    with engine.begin() as connection:
        result = connection.execute(
            text("""
                UPDATE employees
                SET id = :id, name = :name, email = :email,
                    role = :role, salary = :salary, updated_at = NOW()
                WHERE id = :employee_id
            """),
            data,
        )
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="Employee not found")

    return {"message": "Employee updated successfully!"}


@router.delete(
    "/{employee_id}",
    response_model=MessageResponse,
    summary="Delete an employee",
)
def delete_employee(
    employee_id: int,
    current_user: dict = Depends(require_admin),
):
    with engine.begin() as connection:
        result = connection.execute(
            text("DELETE FROM employees WHERE id = :id"),
            {"id": employee_id},
        )
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="Employee not found")

    return {"message": "Employee deleted successfully!"}
