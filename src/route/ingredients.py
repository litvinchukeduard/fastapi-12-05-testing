from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.database.database import get_postgres_db
from src.schemas import IngredientModel, IngredientResponse
from src.service import ingredients as ingredient_service

router = APIRouter(prefix='/ingredients', tags=["ingredients"])


@router.get("/", response_model=List[IngredientResponse])
async def read_tags(skip: int = 0, limit: int = 100, db: Session = Depends(get_postgres_db)):
    return await ingredient_service.get_ingredients(skip, limit, db)


@router.get("/{id}", response_model=IngredientResponse)
async def read_tag(id: int, db: Session = Depends(get_postgres_db)):
    return await ingredient_service.get_ingredient(id, db)


@router.post("/", response_model=IngredientResponse)
async def create_tag(body: IngredientModel, db: Session = Depends(get_postgres_db)):
    return await ingredient_service.create_ingredient(body, db)


@router.put("/{id}", response_model=IngredientResponse)
async def update_tag(body: IngredientModel, id: int, db: Session = Depends(get_postgres_db)):
    return await ingredient_service.update_ingredient(id, body, db)


@router.delete("/{id}", response_model=IngredientResponse)
async def remove_tag(id: int, db: Session = Depends(get_postgres_db)):
    return await ingredient_service.remove_ingredient(id, db)
