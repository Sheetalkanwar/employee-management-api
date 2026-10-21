
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from database import engine
from routes.employee_routes import router as employee_router
from routes.user_routes import router as user_router

app = FastAPI(
    title="Employee Management API",
    description="""
Employee Management REST API built with FastAPI and PostgreSQL.

Features:
- Employee CRUD operations
- Search, filtering, pagination and sorting
- JWT authentication
- Role-based authorization
- User management
- PostgreSQL persistence
- Health monitoring
""",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    openapi_tags=[
        {
            "name": "Authentication",
            "description": "User registration and JWT authentication.",
        },
        {
            "name": "Employees",
            "description": "Employee management and search operations.",
        },
    ],
)



from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://employee-management-apiii-2.onrender.com",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    # Log the actual error in the backend terminal for debugging.
    print(f"Unhandled error on {request.method} {request.url.path}: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )


app.include_router(employee_router)
app.include_router(user_router)


@app.get("/health", summary="Health check")
def health_check():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        return {
            "status": "healthy",
            "database": "connected",
        }

    except Exception as exc:
        print(f"Database health check failed: {exc}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={
                "status": "unhealthy",
                "database": "disconnected",
            },
        )


@app.get("/")
def root():
    return {
        "message": "Employee Management API is running",
        "docs": "/docs",
        "health": "/health",
    }
