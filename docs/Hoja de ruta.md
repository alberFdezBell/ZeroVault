### 🔹 Fase 1: Concepción, Identidad y Preparación Inicial

- [x] **Definición del Alcance:** Consolidar el resumen del sistema.
- [x] **Identidad Open Source:** Elección del nombre oficial del proyecto y selección de la licencia de código abierto (ej. **AGPL-3.0** es ideal para proyectos self-hosted porque obliga a quienes modifiquen el software en su beneficio web a liberar sus cambios).
- [x] **Estructuración Documental Base:** Creación de las plantillas iniciales para la comunidad: `README.md` de presentación, `CONTRIBUTING.md` (normas para colaboradores) y `CODE_OF_CONDUCT.md`.

### 🔹 Fase 2: Diseño de Arquitectura y Especificación Criptográfica

- [x] **Modelado de Datos:** Diseñar los esquemas de tablas para la Base de Datos (Relaciones de usuarios, roles, logs e inventario de secretos cifrados).
- [x] **Protocolo de Autenticación:** Diseñar el flujo exacto de intercambio de hashes para el inicio de sesión sin enviar la contraseña maestra (Flujo SRP - _Secure Remote Password_ o derivados basados en Argon2id).
- [x] **Plano de Endpoints:** Diseñar el árbol de rutas de la API de FastAPI (`/api/v1/auth`, `/api/v1/users`, `/api/v1/secrets`).

### 🔹 Fase 3: Desarrollo del Core Backend (Python & FastAPI)

- [x] **Inicialización del Entorno:** Configurar la estructura de carpetas en Python, entornos virtuales y gestión de dependencias estricta (`pip-tools` o `poetry`).
- [x] **Seguridad del Servidor:** Implementar protección contra Fuerza Bruta (Rate Limiting) y el sistema de control de sesiones mediante tokens de un solo uso o JWT de corta duración para administradores.
- [x] **API Functional:** Programar la lógica CRUD de usuarios para el panel de administración y el almacenamiento/recuperación de _blobs_ cifrados para los empleados.
- [x] **Tests Automatizados:** Pruebas unitarias y de integración del backend usando `pytest`.

### 🔹 Fase 4: Desarrollo del Frontend y Criptografía del Cliente (Vue.js 3)

- [x] **Maquetación del Dashboard:** Diseñar la interfaz de usuario con TailwindCSS, priorizando la claridad, velocidad y facilidad de uso.
- [x] **Implementación de la Bóveda Local:** Programar las funciones en JavaScript/TypeScript que cifran y descifran los datos en tiempo real antes de enviarlos o recibirlos de la API.
- [x] **Integración del Panel de Admin:** Conectar las pantallas de creación de usuarios, asignación de roles y visor de logs con el backend.

### 🔹 Fase 5: Dockerización, Infraestructura y DevOps

- [x] **Construcción de Imágenes:** Crear los `Dockerfile` optimizados para producción (utilizando _multi-stage builds_ para reducir el tamaño de las imágenes y eliminar dependencias de desarrollo).
- [x] **Orquestación Definitiva:** Ajustar el archivo `docker-compose.yml` final, asegurando que los volúmenes persistentes mantengan los datos a salvo en Proxmox/Portainer durante las actualizaciones.

### 🔹 Fase 7: Preparación de Lanzamiento y Publicación en GitHub

- [ ] **Documentación de Despliegue:** Redactar la guía definitiva paso a paso para el administrador de sistemas (cómo copiar el compose en Portainer, configurar HTTPS, y hacer backups de la base de datos).
- [ ] **Lanzamiento del Repositorio:** Subir el código a GitHub, configurar las _GitHub Actions_ básicas (para verificar que los tests pasen automáticamente si externos envían código) e inaugurar el _Roadmap_ de la versión 1.1 en las _Issues_ de GitHub.