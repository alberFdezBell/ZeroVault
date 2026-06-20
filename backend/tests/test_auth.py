import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI
from app.api.v1.auth import router as auth_router
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi.responses import JSONResponse

# Inicializar app de testing aislada
app = FastAPI()
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.include_router(auth_router, prefix="/api/v1")

@app.exception_handler(RateLimitExceeded)
def _rate_limit_exceeded_handler(request, exc):
    return JSONResponse(status_code=429, content={"detail": "Too many requests"})

client = TestClient(app)

def test_pre_login_existing_user():
    """Valida que un usuario registrado reciba su salt correspondiente."""
    response = client.post("/api/v1/auth/pre-login", json={"email": "empleado@empresa.com"})
    assert response.status_code == 200
    assert "master_key_salt" in response.json()
    assert len(response.json()["master_key_salt"]) == 64

def test_pre_login_non_existing_user_mitigation():
    """Prueba que la mitigación de enumeración funcione entregando una salt genérica."""
    response = client.post("/api/v1/auth/pre-login", json={"email": "no_existe@empresa.com"})
    assert response.status_code == 200
    assert "master_key_salt" in response.json()
    assert len(response.json()["master_key_salt"]) == 64

def test_login_successful():
    """Flujo feliz de inicio de sesión tras validación del hash."""
    payload = {
        "email": "empleado@empresa.com",
        "auth_hash": "hash_derivado_simulado_en_cliente_1234567890abcdef"
    }
    response = client.post("/api/v1/auth/login", json=payload)
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["encrypted_dek"] == "en_memoria_vault_key_blob_aes_gcm"

def test_login_failed_wrong_credentials():
    """Asegura el rechazo inmediato ante hashes incorrectos."""
    payload = {
        "email": "empleado@empresa.com",
        "auth_hash": "un_hash_completamente_malicioso_o_erroneo"
    }
    response = client.post("/api/v1/auth/login", json=payload)
    assert response.status_code == 401
    assert response.json()["detail"] == "Correo electrónico o contraseña incorrectos."