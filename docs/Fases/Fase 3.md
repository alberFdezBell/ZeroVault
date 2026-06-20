## 1. Inicialización del Entorno y Dependencias

### Archivo 1: Configuración de Dependencias de Poetry

* **Ruta:** `./backend/pyproject.toml`
* **Propósito:** Declarar las dependencias exactas del proyecto, herramientas de testing y configuraciones del entorno de ejecución de Python.
* **Dependencias:** Python 3.11+, FastAPI, Uvicorn, SQLAlchemy (Async), Asyncpg (Driver Postgres), Pydantic v2 y PyJWT para sesiones.

---

## 2. Configuración Core y Seguridad del Servidor

### Archivo 2: Esquemas de Validación y Modelos Pydantic

* **Ruta:** `./backend/app/schemas/auth.py`
* **Propósito:** Validar estrictamente los payloads de entrada y salida para mitigar inyecciones de datos o desbordamientos de búfer en los endpoints de autenticación.

### Archivo 3: Sistema de Control de Acceso, JWT y Limitador de Tasa (Rate Limiting)

* **Ruta:** `./backend/app/core/security.py`
* **Propósito:** Implementar la protección contra ataques de fuerza bruta (Rate Limiting) mediante `Slowapi` y la emisión/validación de tokens JWT de corta duración para la gestión segura de sesiones de administración y empleados.

---

## 3. API Funcional y Endpoints del Backend

### Archivo 4: Enrutador de Autenticación y Criptografía

* **Ruta:** `./backend/app/api/v1/auth.py`
* **Propósito:** Exponer los endpoints críticos para el intercambio del protocolo Zero-Knowledge. Incluye la simulación defensiva en `pre-login` para mitigar ataques de enumeración de usuarios.

---

## 4. Tests Automatizados

### Archivo 5: Suite de Pruebas Unitarias de Seguridad

* **Ruta:** `./backend/tests/test_auth.py`
* **Propósito:** Validar mediante `pytest` que las restricciones de seguridad (credenciales erróneas, generación de tokens y flujo de pre-login) funcionen de forma infalible antes de compilar la infraestructura.

---
**Fecha de Consolidación:** Junio, 2026