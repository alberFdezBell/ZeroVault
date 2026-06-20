## 1. Construcción de Imágenes Optimizadas (Multi-Stage)

### Archivo 1: Dockerfile del Backend (Python/FastAPI)

- **Ruta:** `./backend/Dockerfile`
    
- **Propósito:** Compilar las dependencias de Python usando la imagen oficial de desarrollo y trasladar el entorno final a una imagen base de **Alpine Linux** ultra-ligera, configurada para ejecutarse bajo un usuario no-raíz (_Non-root user_) para evitar escaladas de privilegios si el contenedor es comprometido.
    

### Archivo 2: Dockerfile del Frontend (Vue.js 3 / Nginx)

- **Ruta:** `./frontend/Dockerfile`
    
- **Propósito:** Compilar la SPA de Vue.js con Node.js y transferir los archivos estáticos listos para producción a un servidor Nginx optimizado.
    

## 2. Orquestación Definitiva para Portainer

### Archivo 3: Archivo de Orquestación Empresarial

- **Ruta:** `./docker-compose.yml`
    
- **Propósito:** Desplegar la infraestructura completa de ZeroVault con aislamiento estricto de redes internas y políticas de persistencia seguras para entornos Proxmox/Portainer.
    
---
**Fecha de Consolidación:** Junio, 2026