from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.config import settings
from app.database import Base, engine
from app import models  # registra los modelos antes de crear tablas
from app.routers import auth, ingredients, recipes

BASE_DIR = Path(__file__).resolve().parent
Base.metadata.create_all(bind=engine)
app = FastAPI(title=settings.app_name, description="API para administrar inventario y generar recetas personalizadas con IA.", version="1.0.0")
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")
app.include_router(auth.router)
app.include_router(ingredients.router)
app.include_router(recipes.router)

@app.get("/health", tags=["Estado"])
def health(): return {"status": "ok", "service": settings.app_name}
@app.get("/", include_in_schema=False)
def home(request: Request): return templates.TemplateResponse("index.html", {"request": request, "app_name": settings.app_name})
