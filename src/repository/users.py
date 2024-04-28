from sqlalchemy.orm import Session

from src.database.models import User

async def get_user_by_email(email: str, db: Session) -> User:
    return db.query(User).filter(User.email == email).first()

async def create_user(body: User, db: Session) -> User:
    body.active = False
    db.add(body)
    db.commit()
    db.refresh(body)
    return body
