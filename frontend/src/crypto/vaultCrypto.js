/**
 * ZeroVault Client Cryptographic Engine (WebCrypto API)
 */

// Configuración estándar para derivación de claves si se opta por compatibilidad nativa (PBKDF2-SHA256)
// Nota: Si se requiere Argon2id puro en el cliente web, se integraría una librería WebAssembly (WASM).
const PBKDF2_ITERATIONS = 100000;

/**
 * 1. Deriva la Master Key (MK) a partir de la Contraseña Maestra y la Salt del usuario
 */
export async function deriveMasterKey(masterPassword, masterKeySalt) {
    const encoder = new TextEncoder();
    const passwordBuffer = encoder.encode(masterPassword);
    const saltBuffer = encoder.encode(masterKeySalt);

    // Importar la contraseña como material base de clave
    const baseKey = await window.crypto.subtle.importKey(
        "raw", passwordBuffer, "PBKDF2", false, ["deriveKey"]
    );

    // Derivar la Master Key (MK)
    return await window.crypto.subtle.deriveKey(
        {
            name: "PBKDF2",
            salt: saltBuffer,
            iterations: PBKDF2_ITERATIONS,
            hash: "SHA-256"
        },
        baseKey,
        { name: "AES-GCM", length: 256 },
        false, // No extraíble por seguridad (permanece aislada en memoria RAM)
        ["encrypt", "decrypt"]
    );
}

/**
 * 2. Genera el Authentication Hash (AH) para enviar al servidor
 */
export async function generateAuthenticationHash(masterKey, email) {
    const encoder = new TextEncoder();
    const tokenInfo = encoder.encode("auth_token_v1:" + email);

    // Exportar transitoriamente un derivado para HMAC o usar la MK de forma indirecta
    // Para simplificar la firma nativa, generamos un hash SHA-256 del material
    const rawKey = await window.crypto.subtle.exportKey("raw", masterKey);
    const hmacKey = await window.crypto.subtle.importKey(
        "raw", rawKey, { name: "HMAC", hash: "SHA-256" }, false, ["sign"]
    );

    const signature = await window.crypto.subtle.sign("HMAC", hmacKey, tokenInfo);
    
    // Convertir el buffer a string hexadecimal (Authentication Hash)
    return Array.from(new Uint8Array(signature))
        .map(b => b.toString(16).padStart(2, "0"))
        .join("");
}

/**
 * 3. Cifra un secreto (texto plano o JSON stringificado) usando la Data Encryption Key (DEK)
 */
export async function encryptPayload(plainText, dekKey) {
    const encoder = new TextEncoder();
    const dataBuffer = encoder.encode(plainText);
    
    // Generar un Vector de Inicialización (Nonce) aleatorio y único de 12 bytes
    const nonce = window.crypto.getRandomValues(new Uint8Array(12));

    const encryptedBuffer = await window.crypto.subtle.encrypt(
        { name: "AES-GCM", iv: nonce, tagLength: 128 },
        dekKey,
        dataBuffer
    );

    // En AES-GCM de WebCrypto, el tag de autenticación se añade automáticamente al final del ciphertext
    const fullBuffer = new Uint8Array(encryptedBuffer);
    const ciphertextBuffer = fullBuffer.slice(0, fullBuffer.byteLength - 16);
    const tagBuffer = fullBuffer.slice(fullBuffer.byteLength - 16);

    // Conversión a formatos transportables en JSON (Hexadecimal / Base64)
    const arrayToHex = (arr) => Array.from(arr).map(b => b.toString(16).padStart(2, "0")).join("");

    return {
        encrypted_payload: btoa(String.fromCharCode(...ciphertextBuffer)), // Base64
        nonce: arrayToHex(nonce),
        tag: arrayToHex(tagBuffer)
    };
}