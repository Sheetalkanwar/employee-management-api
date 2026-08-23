import { useEffect, useState } from "react";
import "./App.css";

function App() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [email, setEmail] = useState("");
  const [isRegistering, setIsRegistering] = useState(false);
  const [employees, setEmployees] = useState([]);
  const [showAddForm, setShowAddForm] = useState(false);

  const [newEmployee, setNewEmployee] = useState({
  id: "",
  name: "",
  email: "",
  role: "",
  salary: "",
});
const [editingEmployee, setEditingEmployee] = useState(null);
  
  const [loggedIn, setLoggedIn] = useState(
    !!localStorage.getItem("access_token")
  );

  const login = async (e) => {
    e.preventDefault();

    try {
      const formData = new URLSearchParams();

      formData.append("username", username);
      formData.append("password", password);

      const response = await fetch(
        "http://127.0.0.1:8000/auth/login",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/x-www-form-urlencoded",
          },
          body: formData,
        }
      );

      const data = await response.json();

      if (!response.ok) {
        alert(data.detail || "Login failed");
        return;
      }

      localStorage.setItem("access_token", data.access_token);
      setLoggedIn(true);
    } catch (error) {
      console.error(error);
      alert("Cannot connect to backend");
    }
  };

  const register = async (e) => {
  e.preventDefault();

  try {
    const response = await fetch(
      "http://127.0.0.1:8000/auth/register",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          username,
          email,
          password,
        }),
      }
    );

    const data = await response.json();

    if (!response.ok) {
      alert(data.detail || "Registration failed");
      return;
    }

    alert("Registration successful! Please login.");

    setIsRegistering(false);
    setEmail("");
    setPassword("");
  } catch (error) {
    console.error(error);
    alert("Cannot connect to backend");
  }
};
    const fetchEmployees = async () => {
    const token = localStorage.getItem("access_token");

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/employees",
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      if (!response.ok) {
        throw new Error("Failed to fetch employees");
      }

      const data = await response.json();

      setEmployees(data);
    } catch (error) {
      console.error(error);
    }
  };

  useEffect(() => {
    if (loggedIn) {
      fetchEmployees();
    }
  }, [loggedIn]);
  const addEmployee = async (e) => {
  e.preventDefault();

  const token = localStorage.getItem("access_token");

  try {
    const response = await fetch(
      "http://127.0.0.1:8000/employees",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          id: Number(newEmployee.id),
          name: newEmployee.name,
          email: newEmployee.email,
          role: newEmployee.role,
          salary: Number(newEmployee.salary),
        }),
      }
    );

    const data = await response.json();

    if (!response.ok) {
      alert(data.detail || "Failed to add employee");
      return;
    }

    alert("Employee added successfully!");

    setNewEmployee({
      id: "",
      name: "",
      email: "",
      role: "",
      salary: "",
    });

    setShowAddForm(false);

    fetchEmployees();
  } catch (error) {
    console.error(error);
    alert("Cannot connect to backend");
  }
};


  const startEdit = (employee) => {
  setEditingEmployee({
    ...employee,
    salary: String(employee.salary),
  });
};
  const updateEmployee = async (e) => {
  e.preventDefault();

  const token = localStorage.getItem("access_token");

  try {
    const response = await fetch(
      `http://127.0.0.1:8000/employees/${editingEmployee.id}`,
      {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          id: Number(editingEmployee.id),
          name: editingEmployee.name,
          email: editingEmployee.email,
          role: editingEmployee.role,
          salary: Number(editingEmployee.salary),
        }),
      }
    );

    const data = await response.json();

    if (!response.ok) {
      alert(data.detail || "Failed to update employee");
      return;
    }

    setEditingEmployee(null);
    fetchEmployees();
  } catch (error) {
    console.error(error);
    alert("Cannot connect to backend");
  }
};
  const logout = () => {
    localStorage.removeItem("access_token");
    setLoggedIn(false);
    setEmployees([]);
  };

  if (!loggedIn) {
    return (
      <div className="login-page">
        <div className="login-card">
          <h1>Employee Management</h1>
          <p>Welcome back! Login to continue.</p>

          <form onSubmit={isRegistering ? register : login}>
            <div className="form-group">
              <label>Username</label>
              <input
                type="text"
                placeholder="Enter username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                required
              />
            </div>

{isRegistering && (
  <div className="form-group">
    <label>Email</label>
    <input
      type="email"
      placeholder="Enter email"
      value={email}
      onChange={(e) => setEmail(e.target.value)}
      required
    />
  </div>
)}
 <div className="form-group">
              <label>Password</label>
              <input
                type="password"
                placeholder="Enter password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </div>

           <button className="login-button" type="submit">
             {isRegistering ? "Register" : "Login"}
          </button> 
          </form>
          <div className="register-text">
  {isRegistering ? (
    <>
      Already have an account?{" "}
      <span onClick={() => setIsRegistering(false)}>
        Login
      </span>
    </>
  ) : (
    <>
      Don't have an account?{" "}
      <span onClick={() => setIsRegistering(true)}>
        Register
      </span>
    </>
  )}
</div>
          
        </div>
      </div>
    );
  }

  return (
    <div className="dashboard">
      <nav className="navbar">
        <h2>Employee Management</h2>

        <button onClick={logout}>
          Logout
        </button>
      </nav>

      <main className="dashboard-content">
        <h1>Employee Dashboard</h1>

        <div className="stats">
          <div className="card">
            <h3>Total Employees</h3>
            <p>{employees.length}</p>
          </div>

          <div className="card">
            <h3>System</h3>
            <p>Online</p>
          </div>

          <div className="card">
            <h3>Authentication</h3>
            <p>JWT Active</p>
          </div>
        </div>

        <div className="employee-section">
          <h2>Employees</h2>
          <button
            className="add-button"
            onClick={() => setShowAddForm(!showAddForm)}
>
            + Add Employee
          </button>

{showAddForm && (
  <form className="employee-form" onSubmit={addEmployee}>
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
    className="edit-button"
    onClick={() => startEdit(employee)}
  >
    Edit
  </button>

  <button
    className="delete-button"
    onClick={() => deleteEmployee(employee.id)}
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
      </main>
    </div>
  );
}

export default App;