from database import employees_collection




def test_get_all_employees(client):
    response = client.get("/employees")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_employee(client):
    employee = {
        "id": 1002,
        "name": "Test Employee",
        "email": "test1002@gmail.com",
        "role": "Developer",
        "salary": 500000
    }

    # Remove the test employee if it already exists
    employees_collection.delete_one({"id": 1002})

    response = client.post("/employees", json=employee)

    assert response.status_code == 201
    assert response.json()["message"] == "Employee added successfully!"

    # Clean up after the test
    employees_collection.delete_one({"id": 1002})


def test_duplicate_employee_id(client):
    employee = {
        "id": 2000,
        "name": "First Employee",
        "email": "first2000@gmail.com",
        "role": "Developer",
        "salary": 500000
    }

    # Clean up old test data
    employees_collection.delete_one({"id": 2000})

    # First employee should be created
    first_response = client.post(
        "/employees",
        json=employee
    )

    assert first_response.status_code == 201

    duplicate_employee = {
        "id": 2000,
        "name": "Duplicate Employee",
        "email": "duplicate2000@gmail.com",
        "role": "Tester",
        "salary": 300000
    }

    # Second employee has the same ID
    second_response = client.post(
        "/employees",
        json=duplicate_employee
    )

    assert second_response.status_code == 400
    assert second_response.json()["detail"] == "Employee ID already exists"

    # Clean up after test
    employees_collection.delete_one({"id": 2000})


def test_invalid_employee_email(client):
    employee = {
        "id": 3000,
        "name": "Invalid Email",
        "email": "not-an-email",
        "role": "Developer",
        "salary": 500000
    }

    response = client.post(
        "/employees",
        json=employee
    )

    assert response.status_code == 422

def test_employee_not_found(client):
    response = client.get("/employees/999999")

    assert response.status_code == 404

def test_update_employee(client):
    employee = {
        "id": 4000,
        "name": "Update Test",
        "email": "update@test.com",
        "role": "Developer",
        "salary": 400000
    }

    # Make sure the test employee doesn't already exist
    employees_collection.delete_one({"id": 4000})

    # Create employee first
    create_response = client.post(
        "/employees",
        json=employee
    )

    assert create_response.status_code == 201

    # Update employee
    updated_employee = {
        "id": 4000,
        "name": "Updated Employee",
        "email": "updated@test.com",
        "role": "Senior Developer",
        "salary": 600000
    }

    response = client.put(
        "/employees/4000",
        json=updated_employee
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Employee updated successfully!"

    # Clean up
    employees_collection.delete_one({"id": 4000})


def test_delete_employee(client):
    employee = {
        "id": 5000,
        "name": "Delete Test",
        "email": "delete@test.com",
        "role": "Tester",
        "salary": 300000
    }

    # Make sure it doesn't already exist
    employees_collection.delete_one({"id": 5000})

    # Create employee
    create_response = client.post(
        "/employees",
        json=employee
    )

    assert create_response.status_code == 201

    # Delete employee
    response = client.delete("/employees/5000")

    assert response.status_code == 200
    assert response.json()["message"] == "Employee deleted successfully!"

    # Verify it was actually deleted
    get_response = client.get("/employees/5000")

    assert get_response.status_code == 404