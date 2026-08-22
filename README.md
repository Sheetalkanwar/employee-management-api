# Employee Management API

A RESTful Employee Management API built using FastAPI and MongoDB. 
The project provides employee CRUD operations, searching, filtering, 
pagination, sorting, validation, duplicate protection, and Swagger API documentation.

## 🚀 Features

- Create employees
- Get all employees
- Get employee by ID
- Update employee information
- Delete employees
- Search employees by name
- Filter employees by role
- Filter employees by minimum salary
- Combined employee search
- Pagination
- Sorting
- Pydantic data validation
- Duplicate employee ID protection
- MongoDB unique index
- Swagger/OpenAPI documentation
- Environment variable configuration
- Modular project structure

## 🛠️ Tech Stack

- Python
- FastAPI
- MongoDB
- PyMongo
- Pydantic
- Uvicorn
- python-dotenv
- Git
- GitHub

## 📁 Project Structure

```text
employee-management-api/
│
├── main.py
├── database.py
├── .env
├── .gitignore
├── README.md
│
├── models/
│   └── employee.py
│
└── routes/
    └── employee_routes.py
    
    🔌 API Endpoints
Method	Endpoint	Description
POST	/employees	Create employee
GET	/employees	Get all employees
GET	/employees/{employee_id}	Get employee by ID
PUT	/employees/{employee_id}	Update employee
DELETE	/employees/{employee_id}	Delete employee
GET	/employees/search	Search using multiple filters
GET	/employees/search/{name}	Search by name
GET	/employees/role/{role}	Filter by role
GET	/employees/salary/{minimum_salary}	Filter by salary
📄 Employee Data

Example request:

{
  "id": 101,
  "name": "Rahul Sharma",
  "email": "rahul@gmail.com",
  "role": "Backend Developer",
  "salary": 550000
}
⚙️ Installation

Clone the repository:

git clone https://github.com/Sheetalkanwar/employee-management-api.git
cd employee-management-api

Install dependencies:

pip install fastapi uvicorn pymongo pydantic email-validator python-dotenv dnspython
🔐 Environment Variables

Create a .env file:

MONGODB_URI=your_mongodb_connection_string

Never upload the .env file to GitHub.

The .gitignore file prevents the environment file from being committed.

▶️ Run the Application

Start the FastAPI server:

python -m uvicorn main:app --reload

The API will run at:

http://127.0.0.1:8000
📚 API Documentation

FastAPI automatically provides interactive Swagger documentation.

Open:

http://127.0.0.1:8000/docs
🗄️ Database

The application uses MongoDB with:

Database: employee_management
Collection: employees

Employee IDs are protected using a MongoDB unique index to prevent duplicate IDs.

🧪 Testing

The API was tested using FastAPI Swagger UI and includes testing for:

Successful employee creation
Duplicate employee IDs
Invalid request data
Employee search
Employee updates
Employee deletion
Non-existent employee IDs
MongoDB connection
🔮 Future Improvements
JWT authentication
Role-based access control
Automated unit and integration testing
Docker containerization
Cloud deployment
Logging and monitoring
React/Next.js frontend
AI-powered employee assistant










Add Docker
## Docker


The application is containerized using Docker.


### Build image


```bash
docker build -t employee-management-api .
Run container
docker run -p 8000:8000 --env-file .env employee-management-api

The API is then available at:

http://127.0.0.1:8000


### 3. Add **Testing**


Since you got **10 tests passing**, definitely show that:


```markdown
## Testing


Automated tests are implemented using Pytest.


Run tests:


```bash
pytest -v

Current test result:

10 passed

Tests cover employee retrieval, creation, duplicate IDs, validation, update, delete, and not-found scenarios.



### 4. Add **Authentication**


```markdown
## Authentication


The API uses JWT-based authentication.


Authentication flow:


1. Register a user
2. Login using username and password
3. Receive JWT access token
4. Use the token for protected endpoints
5. Admin-only operations are protected using role-based authorization
5. Add Health Check
## Health Check


The API provides a health monitoring endpoint:


```text
GET /health

Example successful response:

{
  "status": "healthy",
  "database": "connected"
}


### 6. Add **Project Architecture**


A simple diagram is useful:


```text
Client
  │
  ▼
FastAPI
  │
  ├── Authentication / JWT
  │
  ├── Employee Routes
  │
  ├── User Routes
  │
  └── Health Check
        │
        ▼
     MongoDB Atlas


Docker
  │
  └── FastAPI Application
7. Add Tech Stack
## Tech Stack


| Technology | Purpose |
|---|---|
| Python | Backend development |
| FastAPI | REST API framework |
| MongoDB | Database |
| PyMongo | MongoDB integration |
| JWT | Authentication |
| Bcrypt | Password hashing |
| Pytest | Automated testing |
| Docker | Containerization |
| Uvicorn | ASGI server |
👩‍💻 Author

Sheetal Kanwar

GitHub: https://github.com/Sheetalkanwar