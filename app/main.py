from fastapi import FastAPI
from app.api.acesso import router as login_router
from app.api.tabelas import router as tabelas_router

app = FastAPI(title="API EMBRAPA - Raspagem de Tabelas")

app.include_router(login_router)
app.include_router(tabelas_router)