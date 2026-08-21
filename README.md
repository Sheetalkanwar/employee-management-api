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
👩‍💻 Author

Sheetal Kanwar

GitHub: https://github.com/Sheetalkanwar