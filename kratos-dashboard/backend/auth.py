import bcrypt
#import jwt
from jose import jwt, JWTError
from datetime import datetime, timedelta
from typing import Optional, Dict
from fastapi import HTTPException, status
import os

JWT_SECRET = os.getenv('JWT_SECRET', 'kratos-secret-key-2024')
JWT_ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_HOURS = 24

class AuthManager:
    @staticmethod
    def hash_password(password: str) -> str:
        """Hashea una contraseña usando bcrypt"""
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verifica una contraseña contra su hash"""

        print("Verifica una contraseña contra su hash")
        result = bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

        print("Verifying password:", plain_password, hashed_password, "Result:", result)

        return result
    
    @staticmethod
    def create_access_token(data: Dict) -> str:
        """Crea un token JWT"""

        print('Crea un token JWT')

        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
    
    @staticmethod
    def verify_token(token: str) -> Dict:
        """Verifica y decodifica un token JWT"""
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expirado"
            )
        except jwt.JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido"
            )
    
    @staticmethod
    def get_password_hash(password: str) -> str:
        """Alias para hash_password para compatibilidad"""
        return AuthManager.hash_password(password)

auth_manager = AuthManager()
