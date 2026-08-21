from fastapi import APIRouter, HTTPException, status
from models.employee import Employee
from database import employees_collection

router = APIRouter(
    prefix="/employees",
    tags=["Employees"]
)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    summary="Create a new employee"
)
def add_employee(employee: Employee):

    existing_employee = employees_collection.find_one(
        {"id": employee.id}
    )

    if existing_employee:
        raise HTTPException(
            status_code=400,
            detail="Employee ID already exists"
        )

    result = employees_collection.insert_one(
        employee.model_dump()
    )

    return {
        "message": "Employee added successfully!",
        "mongodb_id": str(result.inserted_id)
    }

@router.get(
    "",
    summary="Get all employees",
    description="Returns a paginated and sorted list of employees."
)
def get_employees(
    page: int = 1,
    limit: int = 5,
    sort_by: str = "id",
    order: str = "asc"
):
    if page < 1:
        raise HTTPException(
            status_code=400,
            detail="Page must be at least 1"
        )

    if limit < 1 or limit > 100:
        raise HTTPException(
            status_code=400,
            detail="Limit must be between 1 and 100"
        )

    allowed_sort_fields = ["id", "name", "salary", "role"]

    if sort_by not in allowed_sort_fields:
        raise HTTPException(
            status_code=400,
            detail="Invalid sort field"
        )

    if order not in ["asc", "desc"]:
        raise HTTPException(
            status_code=400,
            detail="Order must be asc or desc"
        )

    sort_direction = 1 if order == "asc" else -1
    skip = (page - 1) * limit

    employees = list(
        employees_collection.find(
            {},
            {"_id": 0}
        )
        .sort(sort_by, sort_direction)
        .skip(skip)
        .limit(limit)
    )

    return employees
@router.get(
    "/search",
    summary="Search employees with multiple filters"
)
def search_employees(
    name: str | None = None,
    role: str | None = None,
    minimum_salary: float | None = None
):
    query = {}

    if name:
        query["name"] = {
            "$regex": name,
            "$options": "i"
        }

    if role:
        query["role"] = {
            "$regex": f"^{role}$",
            "$options": "i"
        }

    if minimum_salary is not None:
        query["salary"] = {
            "$gte": minimum_salary
        }

    employees = list(
        employees_collection.find(
            query,
            {"_id": 0}
        )
    )

    return employees

@router.get(
    "/{employee_id}",
    summary="Get employee by ID"
)
def get_employee(employee_id: int):

    employee = employees_collection.find_one(
        {"id": employee_id},
        {"_id": 0}
    )

    if employee is None:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    return employee

@router.put(
    "/{employee_id}",
    summary="Update an employee"
)
def update_employee(employee_id: int, employee: Employee):

    result = employees_collection.update_one(
        {"id": employee_id},
        {
            "$set": employee.model_dump()
        }
    )

    if result.matched_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    return {
        "message": "Employee updated successfully!"
    }

@router.delete(
    "/{employee_id}",
    summary="Delete an employee"
)
def delete_employee(employee_id: int):

    result = employees_collection.delete_one(
        {"id": employee_id}
    )

    if result.deleted_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    return {
        "message": "Employee deleted successfully!"
    }

@router.get(
    "/role/{role}",
    summary="Get employees by role"
)
def get_employees_by_role(role: str):

    employees = list(
        employees_collection.find(
            {"role": {"$regex": f"^{role}$", "$options": "i"}},
            {"_id": 0}
        )
    )

    return employees

@router.get(
    "/search/{name}",
    summary="Search employees by name"
)
def search_employees_by_name(name: str):

    employees = list(
        employees_collection.find(
            {"name": {"$regex": name, "$options": "i"}},
            {"_id": 0}
        )
    )

    return employees

@router.get(
    "/salary/{minimum_salary}",
    summary="Get employees by minimum salary"
)
def get_employees_by_salary(minimum_salary: float):

    employees = list(
        employees_collection.find(
            {"salary": {"$gte": minimum_salary}},
            {"_id": 0}
        )
    )

    return employees

