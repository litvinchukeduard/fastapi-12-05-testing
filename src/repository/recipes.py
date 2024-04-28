from typing import List

from sqlalchemy.orm import Session
from sqlalchemy import and_

from src.database.models import Recipe
from src.schemas import RecipeModel


async def get_recipes(skip: int, limit: int, user_id: int, db: Session) -> List[Recipe]:
    return db.query(Recipe).filter(Recipe.user_id == user_id).offset(skip).limit(limit).all()


async def get_recipe(id: int, user_id: int, db: Session) -> Recipe:
    return db.query(Recipe).filter(and_(Recipe.id == id, Recipe.user_id == user_id)).first()


async def get_recipe_by_title(title: str, user_id: int, db: Session) -> Recipe:
    return db.query(Recipe).filter(and_(Recipe.title == title, Recipe.user_id == user_id)).first()


async def create_recipe(body: Recipe, db: Session) -> Recipe:
    db.add(body)
    db.commit()
    db.refresh(body)
    return body


async def remove_recipe(id: int, db: Session) -> Recipe | None:
    recipe = db.query(Recipe).filter(Recipe.id == id).first()
    if recipe:
        db.delete(recipe)
        db.commit()
    return recipe


async def update_recipe(body: Recipe, db: Session) -> Recipe | None:
    if body:
        db.commit()
    return body
