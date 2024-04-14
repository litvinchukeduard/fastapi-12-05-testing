from typing import List

from fastapi import HTTPException, status

from sqlalchemy.orm import Session

from src.repository import unit_quantity as unit_quantity_repository
from src.repository import recipes as recipes_repository
from src.repository import ingredients as ingredients_repository
from src.repository import units as units_repository

from src.database.models import UnitQuantity
from src.schemas import UnitQuantityModel


async def get_unit_quantity(skip: int, limit: int, db: Session) -> List[UnitQuantity]:
    return unit_quantity_repository.get_unit_quantities(skip, limit, db)


async def get_unit_quantity(id: int, db: Session) -> UnitQuantity:
    return unit_quantity_repository.get_unit_quantity(id, db)


async def create_unit_quantity(body: UnitQuantityModel, db: Session) -> UnitQuantity:
    unit_quantity = UnitQuantity(
        name=body.name,
        quantity=body.quantity,
        optional=body.optional,
        recipe_id=body.recipe_id,
        ingredient_id=body.ingredient_id,
        unit_id=body.unit_id
    )
    return unit_quantity_repository.create_unit_quantity(unit_quantity, db)


async def remove_unit_quantity(id: int, db: Session) -> UnitQuantity | None:
    return unit_quantity_repository.remove_unit_quantity(id, db)


async def update_unit_quantity(id: int, body: UnitQuantityModel, db: Session) -> UnitQuantity | None:
    unit_quantity = unit_quantity_repository.get_unit_quantity(id, db)
    if unit_quantity:
        # tags = db.query(Tag).filter(Tag.id.in_(body.tags)).all()
        unit_quantity.name=body.name
        unit_quantity.quantity=body.quantity
        unit_quantity.optional=body.optional
        unit_quantity.recipe_id=body.recipe_id
        unit_quantity.ingredient_id=body.ingredient_id
        unit_quantity.unit_id=body.unit_id
        unit_quantity_repository.update_unit_quantity(unit_quantity)
    return unit_quantity
