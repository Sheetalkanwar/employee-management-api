import { useEffect, useState } from "react";
import EmployeeTable from "../components/EmployeeTable";
import { getEmployees } from "../services/api";

function Dashboard({ onLogout }) {
  const [employees, setEmployees] = useState([]);

  const fetchEmployees = async () => {
    try {
      const data = await getEmployees();
      setEmployees(data);
    } catch (error) {
      console.error(error);
    }
  };

  useEffect(() => {
    fetchEmployees();
  }, []);

  const logout = () => {
    localStorage.removeItem("access_token");
    onLogout();
  };

  return (
    <div className="dashboard">
      <nav className="navbar">
        <h2>Employee Management</h2>
        <button onClick={logout}>Logout</button>
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

        <EmployeeTable
  employees={employees}
  onRefresh={fetchEmployees}
/>
      </main>
    </div>
  );
}

export default Dashboard;