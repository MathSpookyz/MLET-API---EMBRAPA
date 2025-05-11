from fastapi import APIRouter, Form, HTTPException, status
from app.auth.security import verificar_senha
from app.auth.auth import criar_token
from app.auth.models import usuarios_fake

router = APIRouter()

@router.post("/login")
def login(username: str = Form(...), password: str = Form(...)):
    usuario = usuarios_fake.get(username)

    if not usuario or not verificar_senha(password, usuario["senha_hash"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciais inválidas")

    token = criar_token({"sub": username})

    return {"access_token": token, "token_type": "bearer"}