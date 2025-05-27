from jose import jwt
from datetime import datetime
from typing import Optional, Annotated
from pydantic import BaseModel
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials, OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Depends, FastAPI, HTTPException, status

# Chave secreta (coloque algo mais seguro em produção)
SECRET_KEY = "minha-chave-super-secreta"
ALGORITHM = "HS256"

# Security Dependency
security = HTTPBearer()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class Usuario(BaseModel):
    username: str
    senha_hash: str

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None

def criar_token(dados: dict) -> str:
    return jwt.encode(dados, SECRET_KEY, algorithm=ALGORITHM)

# def verificar_token(token: str) -> Optional[dict]:
    # try:
        # return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    # except jwt.JWTError:
        # return None


async def verificar_token(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except HTTPException:
        raise credentials_exception
    user = username
    if user is None:
        raise credentials_exception
    return user