from typing import List

from fastapi import HTTPException, status

from sqlalchemy.orm import Session

from src.repository import recipes as recipes_repository
from src.repository import ingredients as ingredients_repository

from src.database.models import Recipe, User
from src.schemas import RecipeModel


ERROR_RECIPE_ALREADY_EXISTS = "Recipe with this title already exists"


async def get_recipes(skip: int, limit: int, db: Session, user: User) -> List[Recipe]:
    return await recipes_repository.get_recipes(skip, limit, user.id, db)


async def get_recipe(id: int, db: Session) -> Recipe:
    return await recipes_repository.get_recipe(id, db)


async def create_recipe(body: RecipeModel, db: Session, user: User) -> Recipe:
    check_if_title_is_unique(body.title, db)
    ingredients = await ingredients_repository.get_ingredients_by_ids(body.ingredients, db)
    recipe = Recipe(
        title=body.title,
        description=body.description,
        instructions=body.instructions,
        igredients=ingredients,
        user=user
    )
    return await recipes_repository.create_recipe(recipe, db)


async def remove_recipe(id: int, db: Session) -> Recipe | None:
    recipe = db.query(Recipe).filter(Recipe.id == id).first()
    if recipe:
        db.delete(recipe)
        db.commit()
    return recipe


async def update_recipe(id: int, body: RecipeModel, db: Session) -> Recipe | None:
    recipe = await recipes_repository.get_recipe(id, db)
    if recipe:
        ingredients = await ingredients_repository.get_ingredients_by_ids(body.ingredients, db)
        recipe.title = body.title
        recipe.description = body.description
        recipe.instructions = body.instructions
        recipe.ingredients = ingredients
        await recipes_repository.update_recipe(recipe, db)
    return recipe

async def check_if_title_is_unique(title: str, db: Session) -> None:
    recipe = await recipes_repository.get_recipe_by_title(title, db)
    if recipe:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ERROR_RECIPE_ALREADY_EXISTS)
