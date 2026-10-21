
import { useMemo, useState } from "react";
import {
  addEmployee,
  updateEmployee,
  deleteEmployee,
} from "../services/api";
import "./EmployeeTable.css";

const emptyEmployee = {
  id: "",
  name: "",
  email: "",
  role: "",
  salary: "",
};

const formatSalary = (salary) =>
  Number(salary).toLocaleString("en-IN", {
    maximumFractionDigits: 2,
  });

function EmployeeTable({ employees = [], onRefresh }) {
  const [showAddForm, setShowAddForm] = useState(false);
  const [editingEmployee, setEditingEmployee] = useState(null);
  const [newEmployee, setNewEmployee] = useState(emptyEmployee);
  const [search, setSearch] = useState("");
  const [busy, setBusy] = useState(false);

  const filteredEmployees = useMemo(() => {
    const term = search.trim().toLowerCase();

    return employees.filter((employee) =>
      [employee.name, employee.email, employee.role, String(employee.id)]
        .some((value) => String(value ?? "").toLowerCase().includes(term))
    );
  }, [employees, search]);

  const resetForm = () => {
    setNewEmployee(emptyEmployee);
    setShowAddForm(false);
  };

  const handleAddEmployee = async (e) => {
    e.preventDefault();
    setBusy(true);

    try {
      await addEmployee({
        id: Number(newEmployee.id),
        name: newEmployee.name.trim(),
        email: newEmployee.email.trim(),
        role: newEmployee.role.trim(),
        salary: Number(newEmployee.salary),
      });

      resetForm();
      await onRefresh();
    } catch (error) {
      console.error(error);
      alert(error.message || "Unable to add employee.");
    } finally {
      setBusy(false);
    }
  };

  const handleUpdateEmployee = async (e) => {
    e.preventDefault();
    setBusy(true);

    try {
      await updateEmployee(editingEmployee.id, {
        id: Number(editingEmployee.id),
        name: editingEmployee.name.trim(),
        email: editingEmployee.email.trim(),
        role: editingEmployee.role.trim(),
        salary: Number(editingEmployee.salary),
      });

      setEditingEmployee(null);
      await onRefresh();
    } catch (error) {
      console.error(error);
      alert(error.message || "Unable to update employee.");
    } finally {
      setBusy(false);
    }
  };

  const handleDeleteEmployee = async (employee) => {
    if (!window.confirm(`Delete ${employee.name}'s employee record?`)) {
      return;
    }

    setBusy(true);

    try {
      await deleteEmployee(employee.id);
      await onRefresh();
    } catch (error) {
      console.error(error);
      alert(error.message || "Unable to delete employee.");
    } finally {
      setBusy(false);
    }
  };

  const updateField = (setter, current, field, value) => {
    setter({ ...current, [field]: value });
  };

  const renderFormFields = (employee, setter, isEditing = false) => (
    <div className="employee-form-grid">
      <label>
        Employee ID
        <input
          type="number"
          min="1"
          placeholder="e.g. 101"
          value={employee.id}
          disabled={isEditing}
          onChange={(e) =>
            updateField(setter, employee, "id", e.target.value)
          }
          required
        />
      </label>

      <label>
        Full name
        <input
          type="text"
          placeholder="Enter full name"
          value={employee.name}
          onChange={(e) =>
            updateField(setter, employee, "name", e.target.value)
          }
          required
        />
      </label>

      <label>
        Email address
        <input
          type="email"
          placeholder="name@company.com"
          value={employee.email}
          onChange={(e) =>
            updateField(setter, employee, "email", e.target.value)
          }
          required
        />
      </label>

      <label>
        Job role
        <input
          type="text"
          placeholder="e.g. Developer"
          value={employee.role}
          onChange={(e) =>
            updateField(setter, employee, "role", e.target.value)
          }
          required
        />
      </label>

      <label>
        Annual salary (₹)
        <input
          type="number"
          min="0"
          step="0.01"
          placeholder="e.g. 500000"
          value={employee.salary}
          onChange={(e) =>
            updateField(setter, employee, "salary", e.target.value)
          }
          required
        />
      </label>
    </div>
  );

  return (
    <div className="employee-directory">
      <div className="directory-toolbar">
        <div className="directory-title">
          <h2>People Directory</h2>
          <p>Manage and review your employee records.</p>
        </div>

        <button
          type="button"
          className="employee-primary-button"
          onClick={() => {
            setShowAddForm(!showAddForm);
            setEditingEmployee(null);
          }}
        >
          {showAddForm ? "Cancel" : "+ Add Employee"}
        </button>
      </div>

      <div className="directory-search">
        <span aria-hidden="true">⌕</span>
        <input
          type="search"
          aria-label="Search employees"
          placeholder="Search by name, email, role or ID..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
        <span className="employee-count">
          {filteredEmployees.length} {filteredEmployees.length === 1 ? "employee" : "employees"}
        </span>
      </div>

      {showAddForm && (
        <form className="employee-editor" onSubmit={handleAddEmployee}>
          <h3>Add a new employee</h3>
          {renderFormFields(newEmployee, setNewEmployee)}
          <div className="employee-form-actions">
            <button type="button" className="employee-secondary-button" onClick={resetForm}>
              Cancel
            </button>
            <button type="submit" className="employee-primary-button" disabled={busy}>
              {busy ? "Saving..." : "Save Employee"}
            </button>
          </div>
        </form>
      )}

      {editingEmployee && (
        <form className="employee-editor" onSubmit={handleUpdateEmployee}>
          <h3>Edit employee details</h3>
          {renderFormFields(editingEmployee, setEditingEmployee, true)}
          <div className="employee-form-actions">
            <button
              type="button"
              className="employee-secondary-button"
              onClick={() => setEditingEmployee(null)}
            >
              Cancel
            </button>
            <button type="submit" className="employee-primary-button" disabled={busy}>
              {busy ? "Updating..." : "Save Changes"}
            </button>
          </div>
        </form>
      )}

      <div className="employee-table-wrapper">
        <table className="employee-data-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>EMPLOYEE</th>
              <th>JOB ROLE</th>
              <th>ANNUAL SALARY</th>
              <th className="actions-heading">ACTIONS</th>
            </tr>
          </thead>

          <tbody>
            {filteredEmployees.map((employee) => (
              <tr key={employee.id}>
                <td className="employee-id">#{employee.id}</td>
                <td>
                  <div className="employee-identity">
                    <div className="employee-avatar">
                      {(employee.name || "?").trim().charAt(0).toUpperCase()}
                    </div>
                    <div className="employee-person">
                      <strong>{employee.name}</strong>
                      <span>{employee.email}</span>
                    </div>
                  </div>
                </td>
                <td>
                  <span className="employee-role-badge">{employee.role}</span>
                </td>
                <td className="employee-salary">
                  ₹{formatSalary(employee.salary)}
                </td>
                <td>
                  <div className="employee-actions">
                    <button
                      type="button"
                      className="employee-edit-button"
                      disabled={busy}
                      onClick={() => {
                        setShowAddForm(false);
                        setEditingEmployee({
                          ...employee,
                          salary: String(employee.salary),
                        });
                      }}
                    >
                      Edit
                    </button>
                    <button
                      type="button"
                      className="employee-delete-button"
                      disabled={busy}
                      onClick={() => handleDeleteEmployee(employee)}
                    >
                      Delete
                    </button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>

        {filteredEmployees.length === 0 && (
          <div className="employee-empty-state">
            <div className="empty-state-icon">♙</div>
            <h3>{search ? "No matching employees" : "No employees yet"}</h3>
            <p>
              {search
                ? "Try another name, email, role or employee ID."
                : "Add your first employee to start building your directory."}
            </p>
            {search && (
              <button
                type="button"
                className="employee-secondary-button"
                onClick={() => setSearch("")}
              >
                Clear search
              </button>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

export default EmployeeTable;
