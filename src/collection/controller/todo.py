from fastapi import APIRouter, Depends, Request, Response
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT
import jwt_mng
from model import users as users
from model import todo as todos
from datetime import timedelta
from utils.seriliazer import Seriliazer
import random
from fastapi.security import HTTPBearer
from pydantic import Field
from dataclasses import dataclass

router = APIRouter()
seriliazer = Seriliazer()

@dataclass
class ToDo:
    todo: str = Field("make homework", description="TODO")
    description: str = Field("math homework",description="DESC")

@dataclass
class ToDo_ID:
    todo_id: int = Field(1, description="ID")

@dataclass
class ToDo_Upper:
    todo_id: int = Field(1, description="ID")
    todo: str = Field("make homework", description="TODO")
    description: str = Field("math homework",description="DESC")

@router.post('/create', tags=["ToDo"], dependencies=[Depends(HTTPBearer())])
async def create_post(todo: ToDo, Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    dec_payload = jwt_mng.get_decrypt_payload(current_user.encode()).decode()
    # get user
    user = users.UserRepository().get_by_username(username=dec_payload)
    if len(user) < 1:
        msg = "User not exists"
        return JSONResponse(status_code=400, content={"message": msg})

    todo = todo.todo
    description = todo.description
    todos.ToDoRepository().create_todo(todo=todo, description=description)

    return JSONResponse(status_code=200, content={"status":"added"})

@router.get('/list', tags=["ToDo"], dependencies=[Depends(HTTPBearer())])
async def get_all(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    dec_payload = jwt_mng.get_decrypt_payload(current_user.encode()).decode()
    # get user
    user = users.UserRepository().get_by_username(username=dec_payload)
    if len(user) < 1:
        msg = "User not exists"
        return JSONResponse(status_code=400, content={"message": msg})
    
    query = todos.ToDoRepository().get_all()
    body = seriliazer.convert_list_json(query=query)
    seriliazer.dict_to_seriliaze = []
    return Response(status_code=200, content=str(body))

@router.get('/fetch_one', tags=["ToDo"], dependencies=[Depends(HTTPBearer())])
async def get_one(todo_id: ToDo_ID, Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    dec_payload = jwt_mng.get_decrypt_payload(current_user.encode()).decode()
    # get user
    user = users.UserRepository().get_by_username(username=dec_payload)
    if len(user) < 1:
        msg = "User not exists"
        return JSONResponse(status_code=400, content={"message": msg})

    todo_id = todo_id.todo_id

    query = todos.ToDoRepository().fetch_one_by_id(todo_id=todo_id)
    return JSONResponse(status_code=200, content={"data":{"ToDo": query.TODO, "Desc":query.DESCRIPTION}})

@router.get('/fetch_random', tags=["ToDo"], dependencies=[Depends(HTTPBearer())])
async def get_random(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    dec_payload = jwt_mng.get_decrypt_payload(current_user.encode()).decode()
    # get user
    user = users.UserRepository().get_by_username(username=dec_payload)
    if len(user) < 1:
        msg = "User not exists"
        return JSONResponse(status_code=400, content={"message": msg})
    
    query = todos.ToDoRepository().get_all()
    body = seriliazer.convert_list_json(query=query)
    seriliazer.dict_to_seriliaze = []
    num1 = random.randint(0, len(body)-1)
    return Response(status_code=200, content=str(body[num1]))

@router.put('/update', tags=["ToDo"], dependencies=[Depends(HTTPBearer())])
async def update_todo(todo: ToDo_Upper, Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    dec_payload = jwt_mng.get_decrypt_payload(current_user.encode()).decode()
    # get user
    user = users.UserRepository().get_by_username(username=dec_payload)
    if len(user) < 1:
        msg = "User not exists"
        return JSONResponse(status_code=400, content={"message": msg})

    todo_id = todo.todo_id
    todo =  todo.todo
    desc = todo.description

    todos.ToDoRepository().update_by_id(todo_id=todo_id, query={"todo":todo,"description":desc})
    return JSONResponse(status_code=200, content={"status":"updated"})

@router.delete('/delete', tags=["ToDo"], dependencies=[Depends(HTTPBearer())])
async def delete_todo(todo_id: ToDo_ID, Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    dec_payload = jwt_mng.get_decrypt_payload(current_user.encode()).decode()
    # get user
    user = users.UserRepository().get_by_username(username=dec_payload)
    if len(user) < 1:
        msg = "User not exists"
        return JSONResponse(status_code=400, content={"message": msg})
    
    todo_id = todo_id.todo_id

    todos.ToDoRepository().delete_by_id(todo_id=todo_id)
    return JSONResponse(status_code=200, content={"status":"deleted"})

