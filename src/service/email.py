from fastapi import FastAPI
from starlette.responses import JSONResponse
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from pydantic import EmailStr, BaseModel
from typing import List

from src.service import auth as auth_service


conf = ConnectionConfig(
    MAIL_USERNAME = "python_mentor@meta.ua",
    MAIL_PASSWORD = '6&+uG"Y6cqhK:?)',
    MAIL_FROM = "python_mentor@meta.ua",
    MAIL_PORT = 465,
    MAIL_SERVER = "smtp.meta.ua",
    MAIL_FROM_NAME="PyRecipe",
    MAIL_STARTTLS = False,
    MAIL_SSL_TLS = True,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True
)

async def send_confirmation_mail(recipients: list[str]) -> JSONResponse:
    token = await auth_service.create_email_code({'sub': recipients[0]})
    html = f"""<p>Hi this test mail, thanks for using Fastapi-mail</p> {token}"""

    message = MessageSchema(
        subject="Fastapi-Mail module",
        recipients=recipients,
        body=html,
        subtype=MessageType.html)

    fm = FastMail(conf)
    await fm.send_message(message)
    return JSONResponse(status_code=200, content={"message": "email has been sent"})