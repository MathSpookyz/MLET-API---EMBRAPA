from fastapi import FastAPI
from app.api.acesso import router as login_router
from app.api.tabelas import router as tabelas_router

app = FastAPI(title="API EMBRAPA - Raspagem de Tabelas")

app.include_router(login_router)
app.include_router(tabelas_router)

from fastapi import FastAPI
from app.api.acesso import router as login_router
from app.api.tabelas import router as tabelas_router

app = FastAPI(title="API EMBRAPA - Raspagem de Tabelas")

if __name__ == "__main__":
    import uvicorn
    import os

    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
