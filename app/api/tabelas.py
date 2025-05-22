from fastapi import APIRouter, Query, Depends
from app.scraper import scrape_tabelas
from typing import Optional
from app.security.authentication import Usuario, verificar_token
from pydantic import BaseModel
import time

router = APIRouter()

@router.get("/tabelas")
def get_tabelas_range(
    ano_inicio: int = Query(..., description="Ano inicial da consulta"),
    ano_fim: int = Query(..., description="Ano final da consulta"),
    opcao: str = Query(..., description="Opção de categoria"),
    subopcao: Optional[str] = Query(None, description="Subopção da categoria (opcional)"),
    intervalo: float = 1.5,  # para o sleep
    user: Usuario = Depends(verificar_token)
):
    resultados = []

    for ano in range(ano_inicio, ano_fim + 1):
        try:
            tabelas = scrape_tabelas(ano, subopcao, opcao)
            resultados.append({
                "ano": ano,
                "total_linhas": len(tabelas),
                "tabela": tabelas
            })
        except Exception as e:
            resultados.append({
                "ano": ano,
                "erro": str(e)
            })

        time.sleep(intervalo)  # sleep entre requisições

    return {
        "intervalo_usado": intervalo,
        "anos_consultados": list(range(ano_inicio, ano_fim + 1)),
        "resultados": resultados
    }
