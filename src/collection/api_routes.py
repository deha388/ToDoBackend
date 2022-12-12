from fastapi import APIRouter
from controller import login, todo

router = APIRouter()

def register_blueprints(app):
    # route for API with blueprint, because of parsing smaller re-usable components
    app.include_router(login.router, prefix="/user")
    app.include_router(todo.router, prefix="/todo")