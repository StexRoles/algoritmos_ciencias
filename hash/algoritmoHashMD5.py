import hashlib

def generar_md5(mensaje: str) -> str:
    hash_md5 = hashlib.md5()
    hash_md5.update(mensaje.encode('utf-8'))
    
    return hash_md5.hexdigest()

# Ejemplo de uso
if __name__ == "__main__":
    texto = "Hola Mundo!"
    resultado = generar_md5(texto)
    print(f"Texto original: {texto}")
    print(f"Hash MD5: {resultado}")
    print(f"Longitud: {len(resultado)} caracteres")