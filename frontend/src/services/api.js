const API_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

export const loginUser = async (username, password) => {
  const formData = new URLSearchParams();

  formData.append("username", username);
  formData.append("password", password);

  const response = await fetch(`${API_URL}/auth/login`, {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body: formData,
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.detail || "Login failed");
  }

  return data;
};

export const registerUser = async (
  username,
  email,
  password
) => {
  const response = await fetch(`${API_URL}/auth/register`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      username,
      email,
      password,
    }),
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.detail || "Registration failed");
  }

  return data;
};

export const getEmployees = async () => {
  const token = localStorage.getItem("access_token");

  const response = await fetch(`${API_URL}/employees`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.detail || "Failed to fetch employees");
  }

  return data;
};
export const addEmployee = async (employee) => {
  const token = localStorage.getItem("access_token");

  const response = await fetch(`${API_URL}/employees`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify(employee),
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.detail || "Failed to add employee");
  }

  return data;
};

export const updateEmployee = async (employeeId, employee) => {
  const token = localStorage.getItem("access_token");

  const response = await fetch(
    `${API_URL}/employees/${employeeId}`,
    {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify(employee),
    }
  );

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.detail || "Failed to update employee");
  }

  return data;
};

export const deleteEmployee = async (employeeId) => {
  const token = localStorage.getItem("access_token");

  const response = await fetch(
    `${API_URL}/employees/${employeeId}`,
    {
      method: "DELETE",
      headers: {
        Authorization: `Bearer ${token}`,
      },
    }
  );

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.detail || "Failed to delete employee");
  }

  return data;
};