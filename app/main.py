from fastapi import FastAPI
from app.api.routes import router as api_router

app = FastAPI(title="API EMBRAPA - Raspagem de Tabelas")

app.include_router(api_router, prefix="/api")