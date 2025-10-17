import bcrypt

def generate_hash(password: str) -> str:
    """Genera un hash bcrypt para una contraseña"""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def verify_hash(password: str, hash_str: str) -> bool:
    """Verifica si una contraseña coincide con un hash"""
    return bcrypt.checkpw(password.encode('utf-8'), hash_str.encode('utf-8'))

from jose import jwt, JWTError

f = jwt.encode

print(f)

if __name__ == "__main__":
    password = "admin123"
    
    # Generar nuevo hash
    new_hash = generate_hash(password)
    print(f"Nueva contraseña hash para '{password}': {new_hash}")
    
    # Verificar que funciona
    is_valid = verify_hash(password, new_hash)
    print(f"Verificación: {is_valid}")
    
    # Probar con el hash actual de la BD
    current_hash = "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBdXwtO5S7ZQJi"
    is_current_valid = verify_hash(password, current_hash)
    print(f"Hash actual es válido: {is_current_valid}")
