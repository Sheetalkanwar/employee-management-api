from fastapi import FastAPI

from routes.employee_routes import router as employee_router


app = FastAPI(
    title="Employee Management API",
    description="A FastAPI and MongoDB backend for managing employees.",
    version="1.0.0"
)

app.include_router(employee_router)




