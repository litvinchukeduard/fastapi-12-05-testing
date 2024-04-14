from typing import List

from sqlalchemy.orm import Session

from src.database.models import UnitQuantity
from src.schemas import UnitQuantityModel


async def get_unit_quantities(skip: int, limit: int, db: Session) -> List[UnitQuantity]:
    return db.query(UnitQuantity).offset(skip).limit(limit).all()


async def get_unit_quantity(id: int, db: Session) -> UnitQuantity:
    return db.query(UnitQuantity).filter(UnitQuantity.id == id).first()


async def create_unit_quantity(body: UnitQuantity, db: Session) -> UnitQuantity:
    db.add(body)
    db.commit()
    db.refresh(body)
    return body


async def remove_unit_quantity(id: int, db: Session) -> UnitQuantity | None:
    unit_quantity = db.query(UnitQuantity).filter(UnitQuantity.id == id).first()
    if unit_quantity:
        db.delete(unit_quantity)
        db.commit()
    return unit_quantity


async def update_unit_quantity(id: int, body: UnitQuantity, db: Session) -> UnitQuantity | None:
    if body:
        # tags = db.query(Tag).filter(Tag.id.in_(body.tags)).all()
        body.name=body.name
        body.quantity=body.quantity
        body.optional=body.optional
        body.recipe_id=body.recipe_id
        body.ingredient_id=body.ingredient_id
        body.unit_id=body.unit_id
        db.commit()
    return body
