from fastapi import FastAPI

from routes.employee_routes import router as employee_router
from routes.user_routes import router as user_router


app = FastAPI(
    title="Employee Management API",
    description="A FastAPI and MongoDB backend for managing employees.",
    version="1.0.0"
)

app.include_router(employee_router)
app.include_router(user_router)




