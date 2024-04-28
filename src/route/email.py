from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from starlette.responses import JSONResponse

from typing import Annotated

from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, HTTPAuthorizationCredentials, HTTPBearer

from src.database.database import get_postgres_db
from src.schemas import UserModel, Token
from src.service import email as email_service
from src.database.models import User

from src.repository import users as user_repository

router = APIRouter(prefix='/email', tags=["email"])

@router.post("/send")
async def simple_send(recipient: str) -> JSONResponse:
    return await email_service.simple_send(recipient)