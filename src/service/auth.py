import bcrypt
from jose import jwt
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import Annotated

from src.database.models import User

from src.database.database import get_postgres_db
from src.repository import users as user_repository

JWT_SECRET = "JWT_SECRET"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_postgres_db)):
    token = await decode_token(token)
    user_email = token.get('sub')
    print(user_email)
    return await user_repository.get_user_by_email(user_email, db)

async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    if not current_user.active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

async def create_hash(password: str):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

async def compare_password(password: str, hash_str):
    return bcrypt.checkpw(password.encode(), hash_str.encode())

async def create_token(data: dict, expire_minutes=15):
    iat = datetime.now()
    expire_date = datetime.now() + timedelta(expire_minutes)
    return jwt.encode({'iat': iat, 'exp': expire_date, **data}, JWT_SECRET, algorithm='HS256')

async def decode_token(token: str):
    return jwt.decode(token, JWT_SECRET, algorithms=['HS256'])

async def create_email_code(data: dict):
    return await create_token(data, expire_minutes=60)

async def confirm_email_code(email: str, token: str):
    user_data = await decode_token(token)
    return user_data.get('sub') == email