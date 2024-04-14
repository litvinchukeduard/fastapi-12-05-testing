from datetime import datetime
from typing import List
from pydantic import BaseModel, Field, field_validator


class IngredientBase(BaseModel):
    name: str = Field(max_length=50)


class IngredientModel(IngredientBase):
    units: List[int]


class IngredientResponse(IngredientBase):
    id: int

    class Config:
        orm_mode = True


class UnitModel(BaseModel):
    name: str  = Field(max_length=30)


class UnitResponse(UnitModel):
    id: int

    class Config:
        orm_mode = True


class UnitQuantityModel(BaseModel):
    name: str  = Field(max_length=30)
    quantity: int
    optional: bool
    recipe_id: int
    ingredient_id: int
    unit_id: int

    @field_validator('quantity')
    def quantity_validator(cls, value):
        if value > 0:
            return value
        raise ValueError('Quantity must be positive')


class UnitQuantityResponse(UnitQuantityModel):
    id: int

    class Config:
        orm_mode = True


class RecipeBase(BaseModel):
    title: str  = Field(max_length=200)
    description: str = Field(max_length=255)
    instructions: str = Field(max_length=255)


class RecipeModel(RecipeBase):
    ingredients: List[int]


class RecipeResponse(RecipeBase):
    id: int

    class Config:
        orm_mode = True