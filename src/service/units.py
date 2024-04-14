from typing import List

from sqlalchemy.orm import Session

from fastapi import HTTPException, status

from src.repository import units as units_repository

from src.database.models import Unit
from src.schemas import UnitModel


async def get_units(skip: int, limit: int, db: Session) -> List[Unit]:
    return units_repository.get_units(skip, limit, db)


async def get_unit(id: int, db: Session) -> Unit:
    return units_repository.get_unit(id, db)


async def create_unit(body: UnitModel, db: Session) -> Unit:
    unit = Unit(
        name=body.name
    )
    return units_repository.create_unit(unit, db)


async def remove_unit(id: int, db: Session) -> Unit | None:
    return units_repository.remove_unit(id, db)


async def update_unit(id: int, body: UnitModel, db: Session) -> Unit | None:
    unit = units_repository.get_unit(id, db)
    if unit:
        unit.name=body.name
        units_repository.update_unit(unit, db)
    return unit
