from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.database.database import get_postgres_db
from src.schemas import RecipeModel, RecipeResponse
from src.service import recipes as recipes_service

router = APIRouter(prefix='/recipes', tags=["recipes"])


@router.get("/", response_model=List[RecipeResponse])
async def read_tags(skip: int = 0, limit: int = 100, db: Session = Depends(get_postgres_db)):
    return await recipes_service.get_recipes(skip, limit, db)


@router.get("/{id}", response_model=RecipeResponse)
async def read_tag(id: int, db: Session = Depends(get_postgres_db)):
    return await recipes_service.get_recipe(id, db)


@router.post("/", response_model=RecipeResponse)
async def create_tag(body: RecipeModel, db: Session = Depends(get_postgres_db)):
    return await recipes_service.create_recipe(body, db)


@router.put("/{id}", response_model=RecipeResponse)
async def update_tag(body: RecipeModel, id: int, db: Session = Depends(get_postgres_db)):
    return await recipes_service.update_recipe(id, body, db)


@router.delete("/{id}", response_model=RecipeResponse)
async def remove_tag(id: int, db: Session = Depends(get_postgres_db)):
    return await recipes_service.remove_recipe(id, db)
