from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT
import jwt_mng
from model import users as users
from datetime import timedelta
from pydantic import Field
from dataclasses import dataclass
from fastapi.security import HTTPBearer

ACCESS_TOKEN_EXPIRE_TIME = timedelta(days=1)

router = APIRouter()

@dataclass
class User:
    username: str = Field("test", description="username")
    password: str = Field("123456",description="password")

@dataclass
class User_Register:
    username: str = Field("deha", description="username")
    password: str = Field("deha",description="password")
    email: str = Field("deha@deha",description="email")

#login process
@router.post('/login', tags=["Login"])
async def login(user: User, Authorize: AuthJWT = Depends()):
    #compare with database
    #body = await request.json()
    username = user.username
    password = user.password
    user = users.UserRepository().get_by_username_and_password(username=username, password=password)
    #check if is it exist or not #### user=list
    print(user)
    if len(user) < 1:
        msg = "Bad username or password"
        return JSONResponse(status_code=401, content={"message": msg})

    enc_message = jwt_mng.get_encrypt_payload(user[0])
    print(enc_message)
    access_token = Authorize.create_access_token(subject=enc_message,expires_time=ACCESS_TOKEN_EXPIRE_TIME)

    return JSONResponse(status_code=200, content={"access_token":access_token})

@router.post('/register', tags=["Login"])
async def create_user(user: User_Register):
    username = user.username
    password = user.password
    email = user.email
    is_active = True
    users.UserRepository().create_user(username=username, email=email, password=password, is_active=is_active)

    return JSONResponse(status_code=200, content={"Status":"Added"})

@router.get('/me', tags=["Login"], dependencies=[Depends(HTTPBearer())])
async def me(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    try:
        current_user = Authorize.get_jwt_subject()
        print(current_user)
        dec_payload = jwt_mng.get_decrypt_payload(current_user.encode()).decode()
        return JSONResponse(status_code=200, content={"user": dec_payload})
    except:
        return JSONResponse(status_code=401, content={"message": "msg"})
