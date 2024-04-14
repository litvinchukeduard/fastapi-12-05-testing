from typing import List

from sqlalchemy.orm import Session

from src.database.models import Ingredient


async def get_ingredients(skip: int, limit: int, db: Session) -> List[Ingredient]:
    return db.query(Ingredient).offset(skip).limit(limit).all()


async def get_ingredient(id: int, db: Session) -> Ingredient:
    return db.query(Ingredient).filter(Ingredient.id == id).first()


async def get_ingredient_by_name(name: str, db: Session) -> Ingredient:
    return db.query(Ingredient).filter(Ingredient.name == name).first()


async def get_ingredients_by_ids(ids: List[int], db: Session) -> List[Ingredient]:
    return db.query(Ingredient).filter(Ingredient.id.in_(ids)).all()


async def create_ingredient(body: Ingredient, db: Session) -> Ingredient:
    db.add(body)
    db.commit()
    db.refresh(body)
    return body


async def remove_ingredient(id: int, db: Session) -> Ingredient | None:
    ingredient = db.query(Ingredient).filter(Ingredient.id == id).first()
    if ingredient:
        db.delete(ingredient)
        db.commit()
    return ingredient


async def update_ingredient(body: Ingredient, db: Session) -> Ingredient | None:
    if body:
        db.commit()
    return body
