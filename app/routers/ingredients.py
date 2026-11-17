from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.database import get_db
from app.dependencies import get_current_user
from app.models import Ingredient, User
from app.schemas import IngredientCreate, IngredientOut

router = APIRouter(prefix="/ingredients", tags=["Ingredientes"])
@router.get("/", response_model=list[IngredientOut])
def list_ingredients(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return db.scalars(select(Ingredient).where(Ingredient.owner_id == user.id).order_by(Ingredient.name)).all()
@router.post("/", response_model=IngredientOut, status_code=201)
def create_ingredient(data: IngredientCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    item = Ingredient(name=data.name.strip(), quantity=data.quantity, unit=data.unit.strip(), owner_id=user.id)
    db.add(item); db.commit(); db.refresh(item); return item
@router.get("/{ingredient_id}", response_model=IngredientOut)
def get_ingredient(ingredient_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    item = db.scalar(select(Ingredient).where(Ingredient.id == ingredient_id, Ingredient.owner_id == user.id))
    if not item: raise HTTPException(404, "Ingrediente no encontrado")
    return item
@router.put("/{ingredient_id}", response_model=IngredientOut)
def update_ingredient(ingredient_id: int, data: IngredientCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    item = db.scalar(select(Ingredient).where(Ingredient.id == ingredient_id, Ingredient.owner_id == user.id))
    if not item: raise HTTPException(404, "Ingrediente no encontrado")
    item.name=data.name.strip(); item.quantity=data.quantity; item.unit=data.unit.strip(); db.commit(); db.refresh(item); return item
@router.delete("/{ingredient_id}", status_code=204)
def delete_ingredient(ingredient_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    item = db.scalar(select(Ingredient).where(Ingredient.id == ingredient_id, Ingredient.owner_id == user.id))
    if not item: raise HTTPException(404, "Ingrediente no encontrado")
    db.delete(item); db.commit()
