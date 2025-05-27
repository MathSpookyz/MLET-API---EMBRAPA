from jose import jwt
from datetime import datetime
from typing import Optional

# Chave secreta (coloque algo mais seguro em produção)
SECRET_KEY = "minha-chave-super-secreta"
ALGORITHM = "HS256"

def criar_token(dados: dict) -> str:
    return jwt.encode(dados, SECRET_KEY, algorithm=ALGORITHM)

def verificar_token(token: str) -> Optional[dict]:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.JWTError:
        return None