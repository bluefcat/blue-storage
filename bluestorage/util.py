import base64
import secrets
import datetime

import yaml

from typing import Any
from hashlib import sha256
from passlib.context import CryptContext

from bluestorage.setting import setting

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return password_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_context.verify(plain_password, hashed_password)

def generate_token() -> str:
    return secrets.token_urlsafe(32)

def get_expiration_date() -> datetime.datetime:
    days = setting["TOKEN"]["expiration_date"]
    return datetime.datetime.now() + datetime.timedelta(days=days)


def get_hash(obj: object) -> str:
    prehash: bytes = f"{hash(obj)}".encode()
    hexdigest: str = sha256(prehash).hexdigest()
    return hexdigest[:10]

