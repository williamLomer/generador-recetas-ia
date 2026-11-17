from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.services.security import decode_access_token

bearer = HTTPBearer(auto_error=False)
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer), db: Session = Depends(get_db)) -> User:
    if not credentials: raise HTTPException(status_code=401, detail="Debes iniciar sesión")
    try: user_id = int(decode_access_token(credentials.credentials)["sub"])
    except Exception: raise HTTPException(status_code=401, detail="Token inválido o expirado")
    user = db.get(User, user_id)
    if not user: raise HTTPException(status_code=401, detail="Usuario no encontrado")
    return user
