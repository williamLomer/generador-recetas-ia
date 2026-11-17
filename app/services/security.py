import base64, hashlib, hmac, json, secrets, time
from app.config import settings

def hash_password(password: str) -> str:
    salt = secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 240_000).hex()
    return f"pbkdf2_sha256${salt}${digest}"

def verify_password(password: str, stored: str) -> bool:
    try:
        algorithm, salt, expected = stored.split("$")
        if algorithm != "pbkdf2_sha256": return False
        actual = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 240_000).hex()
        return hmac.compare_digest(actual, expected)
    except (ValueError, TypeError):
        return False

def create_access_token(subject: str) -> str:
    now = int(time.time())
    header = {"alg": "HS256", "typ": "JWT"}
    payload = {"sub": subject, "iat": now, "exp": now + settings.access_token_expire_minutes * 60}
    encode = lambda obj: base64.urlsafe_b64encode(json.dumps(obj, separators=(",", ":")).encode()).rstrip(b"=").decode()
    signing = f"{encode(header)}.{encode(payload)}"
    signature = base64.urlsafe_b64encode(hmac.new(settings.secret_key.encode(), signing.encode(), hashlib.sha256).digest()).rstrip(b"=").decode()
    return f"{signing}.{signature}"

def decode_access_token(token: str) -> dict:
    try:
        head, body, signature = token.split(".")
        signing = f"{head}.{body}"
        expected = base64.urlsafe_b64encode(hmac.new(settings.secret_key.encode(), signing.encode(), hashlib.sha256).digest()).rstrip(b"=").decode()
        if not hmac.compare_digest(signature, expected): raise ValueError("Firma inválida")
        payload = json.loads(base64.urlsafe_b64decode(body + "=" * (-len(body) % 4)))
        if payload.get("exp", 0) < time.time(): raise ValueError("Token expirado")
        return payload
    except Exception as exc:
        raise ValueError("Token inválido o expirado") from exc
