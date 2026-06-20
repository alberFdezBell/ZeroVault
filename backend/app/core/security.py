import os
from datetime import datetime, timedelta, timezone
from typing import Optional
from fastapi import HTTPException, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import jwt
from slowapi import Limiter
from slowapi.util import get_remote_address

# Inicialización del limitador de tasa para mitigar Fuerza Bruta
limiter = Limiter(key_func=get_remote_address)

# Configuraciones de entorno con valores defensivos por defecto
SECRET_KEY = os.getenv("APP_SECRET_KEY", "SUPER_SECRET_INSECURE_DEFAULT_KEY_CHANGE_IT")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15  # JWT de corta duración

security_bearer = HTTPBearer()

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Genera un token JWT firmado de corta duración para la sesión actual."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(credentials: HTTPAuthorizationCredentials = Security(security_bearer)) -> dict:
    """Intercepta, decodifica y valida la firma y vigencia del token JWT."""
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="La sesión ha expirado. Por favor, vuelva a autenticarse.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales de sesión inválidas.",
            headers={"WWW-Authenticate": "Bearer"},
        )