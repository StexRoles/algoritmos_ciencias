import hashlib

def generar_sha256(mensaje: str) -> str:
    # Crear objeto SHA-256 y procesar el mensaje
    hash_sha256 = hashlib.sha256()
    hash_sha256.update(mensaje.encode('utf-8'))
    
    return hash_sha256.hexdigest()

# Ejemplo de uso
if __name__ == "__main__":
    texto = "Hola Mundo!"
    resultado = generar_sha256(texto)
    print(f"Texto original: {texto}")
    print(f"Hash SHA-256: {resultado}")
    print(f"Longitud: {len(resultado)} caracteres")