from fastapi import APIRouter, Form, HTTPException, status
from app.security.security import verificar_senha
from app.security.authentication import criar_token, Usuario
from app.security.models import usuarios_fake
from app.datasource.db_queries import salvar_usuario

router = APIRouter()

@router.post("/login")
def login(username: str = Form(...), password: str = Form(...)):
    usuario = usuarios_fake.get(username)

    if not usuario or not verificar_senha(password, usuario["senha_hash"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciais inválidas")

    token = criar_token({"sub": username})

    return {"access_token": token, "token_type": "bearer"}

@router.post("/signin")
def login(user: str = Form(...), passw: str = Form(...)):
    usuario = Usuario(username=user, password=passw)
    salvar_usuario(usuario)

    return {"Usuário "+user+" criado"}