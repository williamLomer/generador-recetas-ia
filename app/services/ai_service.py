import json, re
import httpx
from app.config import settings

REQUIRED_FIELDS = {"nombre_plato", "ingredientes", "pasos", "tiempo_estimado", "dificultad"}

def build_recipe_prompt(inventory: list[dict]) -> str:
    inventory_text = json.dumps(inventory, ensure_ascii=False)
    return f'''Eres un chef. Crea UNA receta que use principalmente este inventario: {inventory_text}
Devuelve exclusivamente JSON válido, sin markdown, con esta estructura exacta:
{{"nombre_plato":"...","ingredientes":[{{"nombre":"...","cantidad":"..."}}],"pasos":["..."],"tiempo_estimado":"...","dificultad":"Fácil|Media|Difícil"}}
No inventes que el usuario tiene ingredientes que no aparecen en el inventario; los complementarios deben señalarse como opcionales.'''

def parse_recipe_response(content: str) -> dict:
    text = content.strip()
    text = re.sub(r"^```(?:json)?\s*|\s*```$", "", text, flags=re.I)
    try:
        data = json.loads(text)
    except json.JSONDecodeError as exc:
        raise ValueError("El modelo no devolvió JSON válido") from exc
    if not isinstance(data, dict) or not REQUIRED_FIELDS.issubset(data):
        raise ValueError("La receta no contiene todos los campos obligatorios")
    if not isinstance(data["ingredientes"], list) or not isinstance(data["pasos"], list) or not data["pasos"]:
        raise ValueError("Ingredientes y pasos deben ser listas; los pasos no pueden estar vacíos")
    return data

async def generate_recipe(inventory: list[dict]) -> dict:
    if not settings.openrouter_api_key:
        raise RuntimeError("Falta configurar OPENROUTER_API_KEY en el archivo .env")
    prompt = build_recipe_prompt(inventory)
    headers = {"Authorization": f"Bearer {settings.openrouter_api_key}", "Content-Type": "application/json", "HTTP-Referer": settings.openrouter_site_url, "X-Title": settings.openrouter_app_name}
    payload = {"model": settings.openrouter_model, "messages": [{"role": "user", "content": prompt}], "temperature": 0.7, "response_format": {"type": "json_object"}}
    async with httpx.AsyncClient(timeout=45) as client:
        response = await client.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
        response.raise_for_status()
    content = response.json()["choices"][0]["message"]["content"]
    return parse_recipe_response(content)
