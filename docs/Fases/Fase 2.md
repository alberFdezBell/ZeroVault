Este documento detalla el diseño de la base de datos relacional, el protocolo criptográfico de Conocimiento Cero (Zero-Knowledge) y el plano de la API para el proyecto **ZeroVault**.

---

## 1. Modelo de Datos (Esquema PostgreSQL)

El diseño de la base de datos asegura la integridad referencial y optimiza el rendimiento mediante la indexación de campos de búsqueda frecuentes, aislando completamente los secretos cifrados de la lógica de administración.

````markdown
-- Habilitar la extensión UUID para generación segura de IDs
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- =============================================================================
-- BLOQUE DE IDENTIDAD Y ACCESOS
-- =============================================================================

CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    role VARCHAR(20) NOT NULL CHECK (role IN ('admin', 'employee')),
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    master_key_salt VARCHAR(64) NOT NULL,
    auth_hash VARCHAR(255) NOT NULL,
    encrypted_dek TEXT NOT NULL,
    requires_password_change BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_email ON users(email);

CREATE TABLE groups (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE user_groups (
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    group_id UUID REFERENCES groups(id) ON DELETE CASCADE,
    PRIMARY KEY (user_id, group_id)
);

-- =============================================================================
-- BLOQUE DE LA BÓVEDA (ZERO-KNOWLEDGE)
-- =============================================================================

CREATE TABLE secrets (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    group_id UUID REFERENCES groups(id) ON DELETE SET NULL,
    encrypted_payload TEXT NOT NULL,
    nonce VARCHAR(32) NOT NULL,
    tag VARCHAR(32) NOT NULL,
    label VARCHAR(100) NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_secrets_user ON secrets(user_id);

-- =============================================================================
-- BLOQUE DE AUDITORÍA
-- =============================================================================

CREATE TABLE audit_logs (
    id BIGSERIAL PRIMARY KEY,
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    action VARCHAR(50) NOT NULL,
    ip_address VARCHAR(45) NOT NULL,
    user_agent TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
````

---

## 2. Protocolo de Autenticación y Cifrado Zero-Knowledge

### Variables Criptográficas

- CM: Contraseña Maestra
    
- MKSalt: Salt única por usuario
    
- MK: Master Key derivada en cliente
    
- AH: Authentication Hash
    
- DEK: Data Encryption Key
    

---

### Fórmulas del Cliente

$$  
MK = Argon2id(CM, MKSalt)  
$$

$$  
AH = HMAC-SHA256(MK, "auth_token_v1")  
$$

$$  
Encrypted_DEK = AES-GCM-Encrypt(DEK, MK)  
$$

---

### Fórmula del Servidor

$$  
auth_hash = Argon2id(AH, server_salt_interna)  
$$

---

## 3. Plano de Endpoints de la API (v1)

|Módulo|Método|Ruta HTTP|Descripción|Permisos|
|---|---|---|---|---|
|Auth|GET|/api/v1/auth/pre-login|Obtiene salt del usuario|Público|
|Auth|POST|/api/v1/auth/login|Autenticación y JWT|Público|
|Users|GET|/api/v1/users|Lista usuarios|Admin|
|Users|POST|/api/v1/users|Crear usuario|Admin|
|Users|PATCH|/api/v1/users/{id}/status|Activar/desactivar usuario|Admin|
|Users|DELETE|/api/v1/users/{id}|Eliminar usuario|Admin|
|Groups|GET|/api/v1/groups|Listar grupos|Admin|
|Groups|POST|/api/v1/groups|Crear grupo|Admin|
|Secrets|GET|/api/v1/secrets|Listar secretos|Autenticado|
|Secrets|GET|/api/v1/secrets/{id}|Obtener secreto cifrado|Propietario|
|Secrets|POST|/api/v1/secrets|Crear secreto|Autenticado|
|Secrets|PUT|/api/v1/secrets/{id}|Actualizar secreto|Propietario|
|Secrets|DELETE|/api/v1/secrets/{id}|Borrar secreto|Propietario|
|Audit|GET|/api/v1/audit/logs|Logs del sistema|Admin|

---
**Fecha de Consolidación:** Junio, 2026