import { useState } from "react";
import {
  addEmployee,
  updateEmployee,
  deleteEmployee,
} from "../services/api";

function EmployeeTable({
  employees,
  onRefresh,
}) {
  const [showAddForm, setShowAddForm] = useState(false);
  const [editingEmployee, setEditingEmployee] = useState(null);

  const [newEmployee, setNewEmployee] = useState({
    id: "",
    name: "",
    email: "",
    role: "",
    salary: "",
  });

  const handleAddEmployee = async (e) => {
  e.preventDefault();

  try {
    await addEmployee({
      id: Number(newEmployee.id),
      name: newEmployee.name,
      email: newEmployee.email,
      role: newEmployee.role,
      salary: Number(newEmployee.salary),
    });

    alert("Employee added successfully!");

    setNewEmployee({
      id: "",
      name: "",
      email: "",
      role: "",
      salary: "",
    });

    setShowAddForm(false);

    onRefresh();
  } catch (error) {
    console.error(error);
    alert(error.message);
  }
};

const handleUpdateEmployee = async (e) => {
  e.preventDefault();

  try {
    await updateEmployee(
      editingEmployee.id,
      {
        id: Number(editingEmployee.id),
        name: editingEmployee.name,
        email: editingEmployee.email,
        role: editingEmployee.role,
        salary: Number(editingEmployee.salary),
      }
    );

    alert("Employee updated successfully!");

    setEditingEmployee(null);

    onRefresh();
  } catch (error) {
    console.error(error);
    alert(error.message);
  }
};
    const handleDeleteEmployee = async (employeeId) => {
  try {
    await deleteEmployee(employeeId);

    alert("Employee deleted successfully!");

    onRefresh();
  } catch (error) {
    console.error(error);
    alert(error.message);
  }
};

  return (
    <div className="employee-section">
      <h2>Employees</h2>

      <button
        className="add-button"
        onClick={() => setShowAddForm(!showAddForm)}
      >
        {showAddForm ? "Cancel" : "+ Add Employee"}
      </button>

      {showAddForm && (
        <form
          className="employee-form"
          onSubmit={handleAddEmployee}
        >
          <input
            type="number"
            placeholder="Employee ID"
            value={newEmployee.id}
            onChange={(e) =>
              setNewEmployee({
                ...newEmployee,
                id: e.target.value,
              })
            }
            required
          />

          <input
            type="text"
            placeholder="Name"
            value={newEmployee.name}
            onChange={(e) =>
              setNewEmployee({
                ...newEmployee,
                name: e.target.value,
              })
            }
            required
          />

          <input
            type="email"
            placeholder="Email"
            value={newEmployee.email}
            onChange={(e) =>
              setNewEmployee({
                ...newEmployee,
                email: e.target.value,
              })
            }
            required
          />

          <input
            type="text"
            placeholder="Role"
            value={newEmployee.role}
            onChange={(e) =>
              setNewEmployee({
                ...newEmployee,
                role: e.target.value,
              })
            }
            required
          />

          <input
            type="number"
            placeholder="Salary"
            value={newEmployee.salary}
            onChange={(e) =>
              setNewEmployee({
                ...newEmployee,
                salary: e.target.value,
              })
            }
            required
          />

          <button type="submit">
            Save Employee
          </button>
        </form>
      )}
      {editingEmployee && (
  <form
    className="employee-form"
    onSubmit={updateEmployee}
  >
    <h3>Edit Employee</h3>

    <input
      type="text"
      value={editingEmployee.name}
      onChange={(e) =>
        setEditingEmployee({
          ...editingEmployee,
          name: e.target.value,
        })
      }
      required
    />

    <input
      type="email"
      value={editingEmployee.email}
      onChange={(e) =>
        setEditingEmployee({
          ...editingEmployee,
          email: e.target.value,
        })
      }
      required
    />

    <input
      type="text"
      value={editingEmployee.role}
      onChange={(e) =>
        setEditingEmployee({
          ...editingEmployee,
          role: e.target.value,
        })
      }
      required
    />

    <input
      type="number"
      value={editingEmployee.salary}
      onChange={(e) =>
        setEditingEmployee({
          ...editingEmployee,
          salary: e.target.value,
        })
      }
      required
    />

    <button type="submit">
      Update Employee
    </button>

    <button
      type="button"
      onClick={() => setEditingEmployee(null)}
    >
      Cancel
    </button>
  </form>
)}


      {employees.length === 0 ? (
        <p>No employees found.</p>
      ) : (
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Name</th>
              <th>Email</th>
              <th>Role</th>
              <th>Salary</th>
              <th>Actions</th>
            </tr>
          </thead>

          <tbody>
            {employees.map((employee) => (
              <tr key={employee.id}>
                <td>{employee.id}</td>
                <td>{employee.name}</td>
                <td>{employee.email}</td>
                <td>{employee.role}</td>
                <td>₹{employee.salary}</td>

                <td>
  <button
    onClick={() =>
      setEditingEmployee({
        ...employee,
        salary: String(employee.salary),
      })
    }
  >
    Edit
  </button>

  <button
    onClick={() =>
      handleDeleteEmployee(employee.id)
    }
  >
    Delete
  </button>
</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}

export default EmployeeTable;