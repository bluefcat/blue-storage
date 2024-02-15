import datetime

from typing import Annotated

from sqlalchemy.exc import IntegrityError
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)

from fastapi.security import (
    OAuth2PasswordRequestForm,
    OAuth2PasswordBearer
)

from bluestorage.util import get_hash, verify_password
from bluestorage.databases.query import Query
from bluestorage.databases.schema import User, Token

from bluestorage.api import app

auth_router = APIRouter()

@auth_router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(
    query: Annotated[Query, Depends(app.get_query)],
    username: str, 
    password: str,
) -> User:
    try:
        user = User(
            id=get_hash(username),
            username = username,
            password = password,
            )
        await query.user.create(user)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists"
        )
    return user

async def authenticate(username: str, password: str):
    query = await app.get_query()

    user = await query.user.read_username(username)
    if not user or not verify_password(password, user.password):
        return None

    return user

@auth_router.post("/signin")
async def signin(
    query: Annotated[Query, Depends(app.get_query)],
    form_data: Annotated[
        OAuth2PasswordRequestForm,
        Depends(OAuth2PasswordRequestForm),
    ]
):
    username = form_data.username
    password = form_data.password

    user = await authenticate(username, password)

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    token = await query.token.read(user.id)
    if token and datetime.datetime.now() >= token.expiration_date:
        await query.token.delete(token)
        token = None

    if not token:
        token = Token(id=user.id, user_id=user.id)
        await query.token.create(token)


    return {
        "access_token": token.access_token,
        "token_type": "bearer"
    }

async def get_current_user(
    query: Annotated[Query, Depends(app.get_query)],
    access_token: str= Depends(OAuth2PasswordBearer(tokenUrl="/signin"))
):
    token = await query.token.read_token(access_token)
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    user = await query.user.read(token.user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    return user
