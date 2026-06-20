# 🛡️ ZeroVault - Guía de Acceso

## ✅ Sistema Funcional Completado

ZeroVault ahora tiene una **base de datos PostgreSQL funcional** con estructura ORM completa, migraciones automáticas y endpoints CRUD.

---

## 🚀 Cómo Acceder

### **1. Cliente Regular (Empleado)**
- **URL:** `http://localhost:8080`
- **Email:** `empleado@empresa.com`
- **Contraseña:** `demo123456`

#### Funcionalidades:
- ✅ Crear secretos (credenciales, tokens, etc.)
- ✅ Editar secretos existentes
- ✅ Eliminar secretos
- ✅ Marcar favoritos
- ✅ Buscar por etiqueta
- ✅ Filtrar por categoría

---

### **2. Panel de Administración**
- **URL:** `http://localhost:8080/admin`
- **Email:** `admin@zerovault.local`
- **Contraseña:** `admin_hash_demo_change_me_in_production` (cambiar en producción)

#### Funcionalidades Admin:
- 👥 Crear/editar/eliminar usuarios
- 👤 Asignar roles (Admin/Employee)
- 🔐 Gestionar estados de usuarios
- 📊 Ver auditoría de accesos
- ⚙️ Configuración del sistema

---

## 📦 Estructura Creada

### **Backend (FastAPI + SQLAlchemy)**

```
backend/app/
├── main.py                 # Punto de entrada FastAPI
├── database.py            # Configuración de BD (AsyncSession, engine)
├── models.py              # Modelos ORM
│   ├── User
│   ├── Secret
│   └── AuditLog
├── init_db.py             # Script de inicialización
├── api/v1/
│   ├── auth.py            # Login/Pre-login con BD real
│   ├── secrets.py         # CRUD completo de secretos
│   ├── users.py           # Gestión de usuarios
│   └── admin.py           # Panel administrativo
├── schemas/               # Pydantic models (validación)
└── core/
    └── security.py        # JWT, rate limiting, get_current_user
```

### **Modelos de BD**

#### `User`
```python
- id (PK)
- uuid
- email (unique)
- auth_hash (criptográfico)
- master_key_salt
- encrypted_dek (Data Encryption Key)
- role (admin/employee)
- is_active
- requires_password_change
- created_at, updated_at, last_login
```

#### `Secret`
```python
- id (PK)
- uuid
- owner_id (FK → User)
- label (etiqueta)
- encrypted_value (texto cifrado)
- category (ej. AWS, Cloud)
- is_favorite
- metadata
- created_at, updated_at
```

#### `AuditLog`
```python
- id
- user_id (FK → User)
- secret_id (FK → Secret, nullable)
- action (SECRET_CREATED, SECRET_READ, etc.)
- ip_address
- created_at
```

---

## 📡 Endpoints API Funcionales

### **Autenticación**
```
POST /api/v1/auth/pre-login
  → Obtiene salt criptográfica (mitiga enumeración de usuarios)

POST /api/v1/auth/login
  → Valida auth_hash y retorna JWT token
```

### **Secretos (CRUD)**
```
GET    /api/v1/secrets              → Listar todos (con filtros)
POST   /api/v1/secrets              → Crear secreto
GET    /api/v1/secrets/{id}         → Ver secreto
PUT    /api/v1/secrets/{id}         → Editar secreto
DELETE /api/v1/secrets/{id}         → Eliminar secreto
POST   /api/v1/secrets/{id}/favorite → Toggle favorito
```

### **Usuarios**
```
GET  /api/v1/users/me               → Info del usuario actual
PUT  /api/v1/users/me               → Actualizar usuario
POST /api/v1/users/change-password  → Cambiar contraseña
```

### **Admin** (requiere role=admin)
```
GET    /api/v1/admin/users          → Listar todos los usuarios
POST   /api/v1/admin/users          → Crear usuario
GET    /api/v1/admin/users/{id}     → Obtener usuario
PUT    /api/v1/admin/users/{id}     → Editar usuario
DELETE /api/v1/admin/users/{id}     → Eliminar usuario
```

---

## 🔐 Flujo de Autenticación

1. **Pre-login:** Cliente solicita salt del usuario
2. **Derivación local:** Contraseña + Salt → Master Key (PBKDF2-SHA256 en cliente)
3. **Hash:** Master Key → Authentication Hash (HMAC-SHA256)
4. **Login:** Email + Auth Hash → Servidor valida y emite JWT
5. **Sesión:** JWT token para todas las siguientes peticiones

**Nota:** La contraseña NUNCA sale del navegador. Todo se procesa con WebCrypto API.

---

## 🎯 Características de Seguridad

✅ **Cifrado de cliente:** AES-256-GCM (WebCrypto API)
✅ **Autenticación criptográfica:** Sin enviar contraseña al servidor
✅ **Rate limiting:** 5 intentos de login/minuto por IP
✅ **Protección contra enumeración:** Salt falsa para usuarios inexistentes
✅ **JWT corta duración:** 15 minutos
✅ **Auditoría completa:** Todos los accesos registrados
✅ **Sesiones aisladas:** PostgreSQL con transacciones ACID

---

## 🐳 Docker Compose

Ejecutar todo con:
```bash
cd /path/to/ZeroVault
docker-compose up
```

### Servicios:
- **zerovault-db** → PostgreSQL 16 (puerto interno)
- **zerovault-backend** → FastAPI (puerto 8000 interno)
- **zerovault-frontend** → Nginx (puerto 8080 externo)

---

## 🔧 Cambios Realizados

### Backend
1. ✅ Creado `database.py` con AsyncSessionLocal
2. ✅ Creado `models.py` con User, Secret, AuditLog
3. ✅ Creado `main.py` con FastAPI app
4. ✅ Creado `secrets.py` con CRUD completo
5. ✅ Creado `users.py` con gestión de usuarios
6. ✅ Creado `admin.py` con endpoints administrativos
7. ✅ Actualizado `auth.py` para usar BD real
8. ✅ Actualizado `security.py` con `get_current_user()`
9. ✅ Creado `init_db.py` para inicializar usuarios demo
10. ✅ Actualizado Dockerfile con script entrypoint

### Frontend
1. ✅ Creado `api.js` con cliente axios
2. ✅ Creado `router.js` con Vue Router
3. ✅ Creado `LoginView.vue` con autenticación completa
4. ✅ Actualizado `VaultDashboard.vue` con CRUD funcional
5. ✅ Creado `AdminDashboard.vue` con gestión de usuarios
6. ✅ Actualizado `main.js` para usar router
7. ✅ Actualizado `App.vue` con router-view

---

## 🧪 Pruebas Rápidas

### 1. Acceder como Employee
```
URL: http://localhost:8080
Email: empleado@empresa.com
Password: demo123456
```
→ Verás dashboard con opción de crear secretos

### 2. Crear un Secreto
- Click en "+ Nuevo Secreto"
- Label: "AWS Access Key"
- Category: "AWS"
- Value: "AKIA1234567890ABCDEF"
- Click crear

### 3. Acceder como Admin
```
URL: http://localhost:8080/admin
Email: admin@zerovault.local
Password: admin_hash_demo...
```
→ Verás panel de usuarios

### 4. Crear Nuevo Usuario desde Admin
- Click en "+ Nuevo Usuario"
- Email: "nuevouser@empresa.com"
- Rol: Employee
- Estado: Activo
- Click crear

---

## 🚨 Próximos Pasos (Producción)

1. **Cambiar credenciales demo**
   - `admin_hash_demo_change_me_in_production`
   - Generar nuevas salts seguras

2. **Variables de entorno**
   - `APP_SECRET_KEY` → JWT secret aleatorio
   - `DB_PASSWORD` → Contraseña fuerte PostgreSQL

3. **HTTPS**
   - Certificado SSL en Nginx
   - HSTS headers

4. **Backups**
   - Volumen PostgreSQL persistente
   - Copias diarias de BD

---

**¡ZeroVault está listo para usar! 🎉**

Accede a `http://localhost:8080` y comienza a gestionar tus secretos de forma segura.
