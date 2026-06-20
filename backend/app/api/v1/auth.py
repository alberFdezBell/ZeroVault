from fastapi import APIRouter, Request, HTTPException, status
from app.schemas.auth import PreLoginRequest, PreLoginResponse, LoginRequest, TokenResponse
from app.core.security import limiter, create_access_token
import secrets

router = APIRouter(prefix="/auth", tags=["Authentication"])

# Base de datos simulada en memoria para esta prueba conceptual
MOCK_USER_DB = {
    "empleado@empresa.com": {
        "salt": "f3a2c891e4b567d890abcdef1234567890abcdef1234567890abcdef12345678",
        "auth_hash": "hash_derivado_simulado_en_cliente_1234567890abcdef",
        "encrypted_dek": "en_memoria_vault_key_blob_aes_gcm",
        "role": "employee",
        "requires_password_change": False
    }
}

@router.post("/pre-login", response_model=PreLoginResponse)
@limiter.limit("5/minute")  # Límite estricto para evitar mapeo automatizado de cuentas
async def pre_login(request: Request, payload: PreLoginRequest):
    """Retorna la salt criptográfica pública requerida por el cliente."""
    user = MOCK_USER_DB.get(payload.email)
    
    if user:
        return PreLoginResponse(master_key_salt=user["salt"])
    
    # MITIGACIÓN DE ENUMERACIÓN DE USUARIOS: 
    # Si el email no existe, devolvemos una salt falsa aleatoria idéntica en estructura
    # para confundir ataques automatizados de recolección de cuentas activas.
    fake_salt = secrets.token_hex(32)
    return PreLoginResponse(master_key_salt=fake_salt)

@router.post("/login", response_model=TokenResponse)
@limiter.limit("5/minute")
async def login(request: Request, payload: LoginRequest):
    """Valida el Authentication Hash generado localmente por el cliente."""
    user = MOCK_USER_DB.get(payload.email)
    
    # Defensa contra timing attacks: Ejecutar la misma lógica de comparación siempre
    if not user or user["auth_hash"] != payload.auth_hash:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo electrónico o contraseña incorrectos."
        )
        
    # Generar sesión JWT
    token_data = {"sub": payload.email, "role": user["role"]}
    access_token = create_access_token(data=token_data)
    
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        encrypted_dek=user["encrypted_dek"],
        requires_password_change=user["requires_password_change"]
    )