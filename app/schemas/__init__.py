from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Any

class UserCreate(BaseModel):
    email: EmailStr
    full_name: str = Field(min_length=2, max_length=120)
    password: str = Field(min_length=8, max_length=128)
class UserLogin(BaseModel):
    email: EmailStr
    password: str
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
class IngredientCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    quantity: float = Field(gt=0)
    unit: str = Field(default="unidad", min_length=1, max_length=40)
class IngredientOut(IngredientCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)
class RecipeOut(BaseModel):
    id: int
    title: str
    ingredients: list[dict[str, Any]]
    steps: list[str]
    estimated_time: str
    difficulty: str
    average_rating: float | None = None
class RatingCreate(BaseModel):
    score: int = Field(ge=1, le=5)
