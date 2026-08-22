from fastapi import FastAPI
from database import db
from fastapi import FastAPI, HTTPException, status
from routes.employee_routes import router as employee_router
from routes.user_routes import router as user_router
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="Employee Management API",
    description="""
A production-style Employee Management REST API built with FastAPI and MongoDB.

Features:
- Employee CRUD operations
- Search, filtering, pagination and sorting
- JWT authentication
- Role-based authorization
- User management
- MongoDB persistence
- Automated testing
- Health monitoring
""",
    version="1.0.0",
    openapi_tags=[
        {
            "name": "Authentication",
            "description": "User registration and JWT authentication."
        },
        {
            "name": "Employees",
            "description": "Employee management and search operations."
        }
    ]
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.exception_handler(Exception)
async def global_exception_handler(
    request: Request,
    exc: Exception
):
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error"
        }
    )

app.include_router(employee_router)
app.include_router(user_router)

@app.get(
    "/health",
    summary="Health check"
)
def health_check():

    try:
        db.command("ping")

        return {
            "status": "healthy",
            "database": "connected"
        }

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={
                "status": "unhealthy",
                "database": "disconnected"
            }
        )


@app.get("/")
def root():
    return {
        "message": "Employee Management API is running",
        "docs": "/docs",
        "health": "/health"
    }