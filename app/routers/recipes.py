import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select, func
from app.database import get_db
from app.dependencies import get_current_user
from app.models import Ingredient, Recipe, Rating, User
from app.schemas import RatingCreate
from app.services.ai_service import generate_recipe

router = APIRouter(prefix="/recipes", tags=["Recetas"])
def serialize(recipe: Recipe, db: Session):
    average = db.scalar(select(func.avg(Rating.score)).where(Rating.recipe_id == recipe.id))
    return {"id": recipe.id, "title": recipe.title, "ingredients": json.loads(recipe.ingredients_json), "steps": json.loads(recipe.steps_json), "estimated_time": recipe.estimated_time, "difficulty": recipe.difficulty, "average_rating": round(float(average), 1) if average is not None else None}

@router.post("/generate")
async def create_recipe(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    inventory = db.scalars(select(Ingredient).where(Ingredient.owner_id == user.id).order_by(Ingredient.name)).all()
    if not inventory: raise HTTPException(400, "Agrega ingredientes a tu inventario antes de generar una receta")
    items = [{"nombre": i.name, "cantidad": i.quantity, "unidad": i.unit} for i in inventory]
    try: data = await generate_recipe(items)
    except RuntimeError as exc: raise HTTPException(503, str(exc))
    except Exception as exc: raise HTTPException(502, f"No fue posible generar la receta: {str(exc)}")
    recipe = Recipe(title=data["nombre_plato"], ingredients_json=json.dumps(data["ingredientes"], ensure_ascii=False), steps_json=json.dumps(data["pasos"], ensure_ascii=False), estimated_time=data["tiempo_estimado"], difficulty=data["dificultad"], owner_id=user.id)
    db.add(recipe); db.commit(); db.refresh(recipe)
    return serialize(recipe, db)

@router.get("/")
def recipe_history(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    recipes = db.scalars(select(Recipe).where(Recipe.owner_id == user.id).order_by(Recipe.created_at.desc())).all()
    return [serialize(r, db) for r in recipes]

@router.post("/{recipe_id}/rating")
def rate_recipe(recipe_id: int, data: RatingCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    recipe = db.scalar(select(Recipe).where(Recipe.id == recipe_id, Recipe.owner_id == user.id))
    if not recipe: raise HTTPException(404, "Receta no encontrada")
    rating = db.scalar(select(Rating).where(Rating.recipe_id == recipe_id, Rating.user_id == user.id))
    if rating: rating.score = data.score
    else: db.add(Rating(recipe_id=recipe_id, user_id=user.id, score=data.score))
    db.commit(); return {"message": "Calificación guardada", "average_rating": serialize(recipe, db)["average_rating"]}

@router.delete("/{recipe_id}", status_code=204)
def delete_recipe(recipe_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    recipe = db.scalar(select(Recipe).where(Recipe.id == recipe_id, Recipe.owner_id == user.id))
    if not recipe: raise HTTPException(404, "Receta no encontrada")
    db.delete(recipe); db.commit()
