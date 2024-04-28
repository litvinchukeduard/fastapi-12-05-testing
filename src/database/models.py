from typing import List

from sqlalchemy import Column, Integer, String, Boolean, Table, ForeignKey, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.sql.sqltypes import DateTime

Base = declarative_base()

recipe_m2m_ingredient = Table(
    "recipe_m2m_ingredient",
    Base.metadata,
    Column("recipe_id", ForeignKey("recipes.id")),
    Column("ingredient_id", ForeignKey("ingredients.id")),
)

ingredient_m2m_unit = Table(
    "ingredient_m2m_unit",
    Base.metadata,
    Column("ingredient_id", ForeignKey("ingredients.id")),
    Column("unit_id", ForeignKey("units.id")),
)


class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False, unique=True)
    description = Column(String(255), nullable=False)
    instructions = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), default=func.now())
    igredients: Mapped[List['Ingredient']] = relationship(
        secondary=recipe_m2m_ingredient
    )
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates='recipes')


class Ingredient(Base):
    __tablename__ = "ingredients"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    units: Mapped[List['Unit']] = relationship(
        secondary=ingredient_m2m_unit
    )


class Unit(Base):
    __tablename__ = "units"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)


class UnitQuantity(Base):
    __tablename__ = "unit_quantity"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    quantity = Column(Integer, nullable=False)
    optional = Column(Boolean, default=True, nullable=False)
    recipe_id = Column("recipe_id", Integer, ForeignKey("recipes.id"), nullable=False)
    ingredient_id = Column("ingredient_id", Integer, ForeignKey("ingredients.id"), nullable=False)
    unit_id = Column("unit_id", Integer, ForeignKey("units.id"), nullable=False)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False, unique=True)
    active = Column(Boolean, nullable=False)
    recipes: Mapped[List['Recipe']] = relationship()

