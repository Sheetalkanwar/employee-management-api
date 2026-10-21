
import { useState } from "react";
import { Link } from "react-router-dom";
import { loginUser } from "../services/api";

function Login({ onLogin }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);

  const handleLogin = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const data = await loginUser(username.trim(), password);

      if (!data.access_token) {
        throw new Error("Login succeeded, but no access token was returned.");
      }

      localStorage.setItem("access_token", data.access_token);
      onLogin();
    } catch (error) {
      console.error("Login error:", error);
      alert(error.message || "Login failed. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-page">
      <div className="login-card">
        <h1>Employee Management</h1>
        <p>Welcome back! Login to continue.</p>

        <form onSubmit={handleLogin}>
          <div className="form-group">
            <label htmlFor="username">Username</label>
            <input
              id="username"
              type="text"
              placeholder="Enter username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              autoComplete="username"
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="password">Password</label>
            <input
              id="password"
              type="password"
              placeholder="Enter password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              autoComplete="current-password"
              required
            />
          </div>

          <button
            className="login-button"
            type="submit"
            disabled={loading}
          >
            {loading ? "Signing in..." : "Login"}
          </button>
        </form>

        <div className="register-text">
          Don't have an account?{" "}
          <Link to="/register">Register</Link>
        </div>
      </div>
    </div>
  );
}

export default Login;
