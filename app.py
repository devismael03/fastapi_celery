from typing import Optional

from fastapi import FastAPI, HTTPException, Request, Depends, Header
from fastapi.responses import JSONResponse

from pydantic import BaseModel

from api_models import *

from db_models import User, Task

from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException


from worker import get_data

import requests

app = FastAPI()

class Settings(BaseModel):
    authjwt_secret_key: str = "mysupersecret"

@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )

@AuthJWT.load_config
def get_config():
    return Settings()



@app.post("/api/v1/signup")
def register(user: UserDto):
    newUser = User(
        username = user.username,
        password = user.password
    )
    newUser.save()
    return {"Message": "Successfully registered"}

@app.post("/api/v1/login")
def login(user: UserDto, Authorize: AuthJWT = Depends()):
    if User.select().where((User.username == user.username) & (User.password == user.password)).count() > 0:
        access_token = Authorize.create_access_token(subject=user.username)
        refresh_token = Authorize.create_refresh_token(subject=user.username)
        return {"access_token" : access_token, "refresh_token" : refresh_token}
    else:
        raise HTTPException(status_code=403, detail="Username or password is not correct")

@app.post("/api/v1/refresh")
def refresh(Authorize: AuthJWT = Depends()):
    Authorize.jwt_refresh_token_required()

    user = Authorize.get_jwt_subject()
    refreshed_token = Authorize.create_access_token(subject=user)

    return {"access_token" : refreshed_token}

@app.get("/api/v1/user")
def user_info(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()

    current_user = Authorize.get_jwt_subject()
    return {"username" : current_user}


@app.post("/api/v1/task")
def task(ip_address: str, Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    inserted_task = Task(
        ip = ip_address
    )

    inserted_task.save()

    get_data.delay(ip_address,inserted_task.id)
    return {"task_id" : inserted_task.id}


@app.get("/api/v1/status")
def status(id: int, Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    result_task = Task.get_by_id(id)

    return{
        "task_id" : result_task.id,
        "country" : result_task.country,
        "city" : result_task.city
    }

    
