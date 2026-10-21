import "./Dashboard.css";
import { useEffect, useState } from "react";
import EmployeeTable from "../components/EmployeeTable";
import { getEmployees } from "../services/api";

function Dashboard({ onLogout }) {
  const [employees, setEmployees] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const fetchEmployees = async () => {
    try {
      setError("");
      const data = await getEmployees();
      setEmployees(Array.isArray(data) ? data : data.employees || []);
    } catch (err) {
      console.error(err);
      setError(err.message || "Unable to load employees.");
    } finally {
      setLoading(false);
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
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-icon">E</div>
          <div>
            <strong>ElevateHR</strong>
            <span>Employee platform</span>
          </div>
        </div>

        <p className="sidebar-label">WORKSPACE</p>
        <div className="sidebar-link active">
          <span>▦</span> Dashboard
        </div>
        <div className="sidebar-link">
          <span>♙</span> Employees
        </div>

        <div className="sidebar-bottom">
          <div className="profile-avatar">HR</div>
          <div className="profile-info">
            <strong>Workspace</strong>
            <span>Management portal</span>
          </div>
          <button className="logout-button" onClick={logout} title="Logout">
            ↗
          </button>
        </div>
      </aside>

      <main className="dashboard-main">
        <header className="topbar">
          <div className="breadcrumb">Workspace / <strong>Dashboard</strong></div>
          <div className="status-pill">
            <span className="status-dot" /> System operational
          </div>
        </header>

        <section className="dashboard-content">
          <div className="welcome-row">
            <div>
              <p className="eyebrow">OVERVIEW</p>
              <h1>Employee dashboard</h1>
              <p className="subtitle">
                Welcome back! Here's what's happening with your team.
              </p>
            </div>
            <div className="date-chip">
              <span>◷</span> People &amp; operations
            </div>
          </div>

          {error && (
            <div className="dashboard-error">
              <strong>Couldn't load employees.</strong>
              <p>{error}</p>
              <button onClick={fetchEmployees}>Try again</button>
            </div>
          )}

          <div className="stats">
            <div className="stat-card">
              <div className="stat-top">
                <span>Total employees</span>
                <div className="stat-icon purple">♙</div>
              </div>
              <div className="stat-value">
                {loading ? "—" : employees.length}
              </div>
              <div className="stat-foot">People in your directory</div>
            </div>

            <div className="stat-card">
              <div className="stat-top">
                <span>System status</span>
                <div className="stat-icon green">✓</div>
              </div>
              <div className="stat-value status-value">Operational</div>
              <div className="stat-foot">
                <span className="status-dot" /> Application dashboard
              </div>
            </div>

            <div className="stat-card">
              <div className="stat-top">
                <span>Security</span>
                <div className="stat-icon blue">◇</div>
              </div>
              <div className="stat-value status-value">JWT enabled</div>
              <div className="stat-foot">Token-based authentication</div>
            </div>
          </div>

          <section className="employee-section">
            <div className="section-heading">
              <div>
                <h2>People directory</h2>
                <p>Manage and review your employee records.</p>
              </div>
              <button className="refresh-button" onClick={fetchEmployees}>
                ↻ Refresh
              </button>
            </div>

            {loading ? (
              <div className="loading-state">Loading employee records...</div>
            ) : (
              <EmployeeTable
                employees={employees}
                onRefresh={fetchEmployees}
              />
            )}
          </section>

          <footer className="dashboard-footer">
            <span>ElevateHR · Employee management</span>
            <span>Built for better teamwork.</span>
          </footer>
        </section>
      </main>
    </div>
  );
}

export default Dashboard;
