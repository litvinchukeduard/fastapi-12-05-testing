from typing import List

from sqlalchemy.orm import Session

from src.database.models import Unit
from src.schemas import UnitModel


async def get_units(skip: int, limit: int, db: Session) -> List[Unit]:
    return db.query(Unit).offset(skip).limit(limit).all()


async def get_unit(id: int, db: Session) -> Unit:
    return db.query(Unit).filter(Unit.id == id).first()


async def get_units_by_ids(ids: List[int], db: Session) -> List[Unit]:
    return db.query(Unit).filter(Unit.id.in_(ids)).all()


async def create_unit(body: Unit, db: Session) -> Unit:
    db.add(body)
    db.commit()
    db.refresh(body)
    return body


async def remove_unit(id: int, db: Session) -> Unit | None:
    unit = db.query(Unit).filter(Unit.id == id).first()
    if unit:
        db.delete(unit)
        db.commit()
    return unit


async def update_unit(body: Unit, db: Session) -> Unit | None:
    if body:
        body.name=body.name
        db.commit()
    return body
