Este documento consolida la definición del alcance, las decisiones de identidad open source y el estado de la estructura documental base del sistema de gestión segura de contraseñas.

---

## 1. Definición del Alcance Consolidado

### Propósito del Sistema
Crear una solución de gestión de contraseñas empresarial de código abierto, autoalojable (self-hosted) y bajo un estricto modelo de **Conocimiento Cero (Zero-Knowledge)**. El sistema resuelve la paradoja corporativa: permitir a la empresa administrar la infraestructura sin otorgarles acceso a los secretos de los empleados.

### Roles del Sistema
*   **Administrador de Infraestructura / TI:** 
    *   Gestiona el ciclo de vida de los usuarios (Crear, revocar, agrupar por departamentos).
    *   Monitorea la salud del sistema y accede a logs de auditoría operacional.
    *   *Restricción:* No tiene acceso visual ni técnico a las claves maestras ni a las bóvedas.
*   **Empleado / Usuario Final:**
    *   Es dueño absoluto de su Contraseña Maestra.
    *   Gestiona, almacena y busca sus secretos (credenciales, notas seguras) de forma privada.
    *   Realiza las operaciones criptográficas localmente en su navegador.

### Arquitectura de Despliegue Objetivo
El sistema se desplegará mediante **Docker Compose** en entornos virtualizados o físicos (optimizados para **Proxmox** y gestionados mediante **Portainer**).
*   **Servicio 1 (Frontend):** Servidor Nginx que actúa como proxy inverso y sirve la SPA.
*   **Servicio 2 (Backend):** API REST asíncrona construida en FastAPI (Python).
*   **Servicio 3 (Base de Datos):** Servidor PostgreSQL para persistencia de datos (blobs cifrados y metadatos de usuario).

---

## 2. Identidad Open Source y Marco Legal

*   **Nombre Oficial del Proyecto:** ZeroVault
*   **Licencia de Código Abierto:** **GNU Affero General Public License v3.0 (AGPL-3.0)**
    *   *Justificación:* Garantiza que cualquier entidad que modifique este software para ofrecerlo como un servicio a través de la red (SaaS/Cloud) esté obligada por ley a liberar sus modificaciones bajo la misma licencia, protegiendo la naturaleza abierta del núcleo del proyecto.

---

## 3. Estado de la Estructura Documental Base

Para habilitar la colaboración externa segura y profesional desde el día uno, se deberán redactar e implementar las siguientes plantillas en la raíz del repositorio:

| Archivo | Propósito |
| :--- | :--- |
| `README.md` | Presentación del proyecto, arquitectura criptográfica e instrucciones de despliegue rápido. |
| `CONTRIBUTING.md` | Reglas de estilo (PEP 8, Vue modulares), flujo de Git (ramas feature) y canal seguro para reportes de vulnerabilidades. |
| `CODE_OF_CONDUCT.md` | Adaptación del estándar *Contributor Covenant* para garantizar un entorno seguro y profesional. |
| `LICENSE` | Copia textual de la licencia GNU AGPL-3.0. |

---

## Compromisos Inmutables de Seguridad (Criterios de Aceptación)

Cualquier desarrollo futuro en el Backend o Frontend debe respetar obligatoriamente estos tres pilares establecidos en la Fase 1:
1.  **Cifrado en el Cliente:** Las contraseñas del usuario se cifran mediante **AES-256-GCM** en el navegador antes de salir hacia la red.
2.  **Derivación Segura:** La Contraseña Maestra del usuario nunca se envía al servidor; se utiliza **Argon2id** localmente para derivar la clave de cifrado y el hash de autenticación.
3.  **Logs Limpios:** Queda estrictamente prohibido registrar hashes de autenticación, textos planos o vectores de inicialización (IV) en los logs de auditoría del servidor.

---
**Fecha de Consolidación:** Junio, 2026