from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from typing import Annotated

from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, HTTPAuthorizationCredentials, HTTPBearer

from src.database.database import get_postgres_db
from src.schemas import UserModel, Token
from src.service import auth as auth_service
from src.database.models import User

from src.repository import users as user_repository
from src.service import email as email_service

router = APIRouter(prefix='/auth', tags=["auth"])

EMAIL_ALREADY_EXISTS = "User with this email already exists"
PASSWORD_IS_NOT_CORRECT = "User password is not correct"

@router.post('/signup')
async def create_user(body: UserModel, db: Session = Depends(get_postgres_db)):
    if await user_repository.get_user_by_email(body.email, db):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=EMAIL_ALREADY_EXISTS)
    body.password = await auth_service.create_hash(body.password)
    user = await user_repository.create_user(User(**body.model_dump()), db)
    await email_service.send_confirmation_mail([body.email])
    return {"id": user.id}

@router.post('/login')
async def login_user(body: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_postgres_db)):
    user = await user_repository.get_user_by_email(body.username, db)
    if not await auth_service.compare_password(body.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=PASSWORD_IS_NOT_CORRECT)
    access_token = await auth_service.create_token({'sub': user.email})
    return Token(access_token=access_token, token_type="bearer")

@router.post('/confirm-email')
async def confirm_email(body: dict, db: Session = Depends(get_postgres_db)):
    # {'email': '', 'token': ''}
    if not await user_repository.get_user_by_email(body.get('email'), db):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=EMAIL_ALREADY_EXISTS)
    return await auth_service.confirm_email_code(body.get('email'), body.get('token'))
