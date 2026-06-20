# Configuración de Infraestructura y Políticas de Servicio: Fase 6

Este documento detalla el aprovisionamiento de archivos de configuración estáticos inyectados a los contenedores Docker para garantizar el aislamiento de red, la mitigación de ataques web y el cumplimiento del pilar de Logs Limpios.

---

## 1. Estructura de Directorios Actualizada

Para que la orquestación mediante `docker-compose.yml` sea válida, se ha creado el directorio maestro `docker/` en la raíz del proyecto para almacenar los archivos de configuración inmutables:

```text
ZEROVAULT/
├── backend/
├── docker/                <── Directorio de Configuración de Infraestructura
│   ├── nginx.conf         <── Políticas de Seguridad Web y Proxy Inverso
│   └── postgres.conf      <── Hardening y Optimización de Base de Datos
├── frontend/
└── docker-compose.yml
````

## 2. Especificación Técnico-Defensiva de Nginx

- **Ruta del Archivo:** `./docker/nginx.conf`
    
- **Mapeo en Compose:** Mapeado en modo de solo lectura (`:ro`) para evitar alteraciones en caliente si el contenedor frontend es comprometido.
    

### Directivas Clave de Seguridad Aplicadas:

1. **`server_tokens off;`**: Mitiga ataques de reconocimiento al ocultar la versión exacta de Nginx en las cabeceras de respuesta.
    
2. **`Content-Security-Policy (CSP)`**: Establece un entorno de ejecución estricto (`default-src 'self'`). Evita ataques **XSS** al bloquear la ejecución de scripts externos e impide la exfiltración de datos limitando las conexiones de red estrictamente al origen.
    
3. **`X-Frame-Options "DENY"`**: Inhabilita la renderización de la SPA dentro de iframes externos, destruyendo vectores de ataque por **Clickjacking**.
    
4. **`proxy_pass` bajo `/api/v1/`**: Nginx actúa como escudo. La API de FastAPI permanece oculta en la red interna de Docker (`zerovault-backend-net`) y solo es accesible a través del proxy inverso.
    

## 3. Especificación Técnico-Defensiva de PostgreSQL

- **Ruta del Archivo:** `./docker/postgres.conf`
    
- **Mapeo en Compose:** Inyectado mediante el comando de arranque del servicio de base de datos.
    

### Directivas Clave de Seguridad y Rendimiento Aplicadas:

1. **Aislamiento de Escucha (`listen_addresses = '*'`)**: Aunque escucha en todas las interfaces del contenedor, el archivo compose no expone puertos públicos al host (`ports:` omitido), lo que restringe el acceso exclusivamente al contenedor del backend.
    
2. **`log_statement = 'none'`**: **Garantía del pilar inmutable de Logs Limpios.** Impide de forma absoluta que PostgreSQL registre las sentencias SQL crudas o valores de inserción en los archivos de log (`stderr`), protegiendo los _blobs_ de contraseñas cifradas ante accesos indebidos a los logs del sistema operativo.
    
3. **Optimización de Memoria**: Configuración adaptada para entornos virtualizados (Proxmox/Portainer) limitando los búferes compartidos (`shared_buffers = 128MB`) y la memoria de trabajo para evitar desbordamientos de memoria del sistema (OOM Killer).
    

## 4. Plantilla de Variables de Entorno Obligatoria

Para levantar la infraestructura de forma segura, el administrador debe crear un archivo `.env` en la raíz del proyecto con la siguiente estructura analizada:

Bash

```
# Puerto público de escucha en el servidor Proxmox/Docker
WEB_PORT=8080

# Credenciales de la Base de Datos Interna
DB_USER=zerovault_admin
DB_PASSWORD=CambiaEstePasswordPorUnoCriptograficamenteSeguro2026!
DB_NAME=zerovault_prod

# Clave secreta para la firma de tokens JWT del servidor
# Generar en terminal con: openssl rand -hex 32
APP_SECRET_KEY=clave_secreta_de_produccion_del_servidor_aqui
```

---
**Fecha de Consolidación:** Junio, 2026