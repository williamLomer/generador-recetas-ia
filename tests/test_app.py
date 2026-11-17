import json
from app.services.ai_service import build_recipe_prompt, parse_recipe_response
from app.services.security import hash_password, verify_password, create_access_token, decode_access_token


def register(client):
    r=client.post('/auth/register',json={'email':'will@example.com','full_name':'Willian','password':'Password123'})
    assert r.status_code==201
    return r.json()['access_token']

def auth(token): return {'Authorization':f'Bearer {token}'}

def test_health_endpoint(client):
    r=client.get('/health'); assert r.status_code==200 and r.json()['status']=='ok'

def test_password_hash_and_verify():
    hashed=hash_password('Password123')
    assert hashed != 'Password123' and verify_password('Password123',hashed)
    assert not verify_password('incorrecta',hashed)

def test_jwt_round_trip():
    token=create_access_token('17'); assert decode_access_token(token)['sub']=='17'

def test_prompt_contains_inventory():
    prompt=build_recipe_prompt([{'nombre':'Tomate','cantidad':2,'unidad':'unidad'}])
    assert 'Tomate' in prompt and 'JSON válido' in prompt

def test_parse_valid_recipe_json():
    data={'nombre_plato':'Arroz casero','ingredientes':[{'nombre':'Arroz','cantidad':'1 taza'}],'pasos':['Lavar','Cocinar'],'tiempo_estimado':'25 minutos','dificultad':'Fácil'}
    assert parse_recipe_response(json.dumps(data))['nombre_plato']=='Arroz casero'

def test_parse_rejects_incomplete_json():
    try: parse_recipe_response('{"nombre_plato":"Solo título"}')
    except ValueError as exc: assert 'campos' in str(exc)
    else: assert False, 'Debió rechazar la receta incompleta'

def test_register_and_login(client):
    register(client)
    r=client.post('/auth/login',json={'email':'will@example.com','password':'Password123'})
    assert r.status_code==200 and r.json()['access_token']

def test_ingredient_crud_and_user_protection(client):
    token=register(client)
    created=client.post('/ingredients/',headers=auth(token),json={'name':'Tomate','quantity':3,'unit':'unidades'})
    assert created.status_code==201
    item_id=created.json()['id']
    assert client.get('/ingredients/',headers=auth(token)).json()[0]['name']=='Tomate'
    updated=client.put(f'/ingredients/{item_id}',headers=auth(token),json={'name':'Tomate cherry','quantity':5,'unit':'unidades'})
    assert updated.status_code==200 and updated.json()['quantity']==5
    assert client.delete(f'/ingredients/{item_id}',headers=auth(token)).status_code==204
    assert client.get('/ingredients/',headers=auth(token)).json()==[]

def test_ingredient_requires_auth(client):
    assert client.get('/ingredients/').status_code==401
