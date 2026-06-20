## 1. Módulo Criptográfico del Cliente (El Core Zero-Knowledge)

### Archivo 1: Motor de Cifrado y Derivación de Claves

- **Ruta:** `./frontend/src/crypto/vaultCrypto.js`
    
- **Propósito:** Derivar la Master Key (`MK`), generar el Authentication Hash (`AH`) y realizar el cifrado/descifrado simétrico de secretos en la RAM del navegador mediante **AES-256-GCM**.
    
- **Dependencias:** WebCrypto API nativa (disponible en todos los navegadores modernos bajo contextos seguros HTTPS/localhost).
    

## 2. Maquetación del Dashboard y la Bóveda Local

### Archivo 2: Componente Vista de la Bóveda (Empleado)

- **Ruta:** `./frontend/src/views/VaultDashboard.vue`
    
- **Propósito:** Interfaz de usuario construida con TailwindCSS para que el empleado gestione y busque contraseñas de forma limpia y veloz. Muestra el descifrado "al vuelo".
    

## 3. Integración del Panel de Administración

### Archivo 3: Vista del Panel de Gestión Corporativa (Admin)

- **Ruta:** `./frontend/src/views/AdminDashboard.vue`
    
- **Propósito:** Proporcionar al administrador de TI la visualización completa del estado de infraestructura, gestión de alta/baja de empleados y auditoría operacional sin violar el principio Zero-Knowledge.
    

---
**Fecha de Consolidación:** Junio, 2026