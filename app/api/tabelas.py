from fastapi import APIRouter, Query
from app.scraper import scrape_tabelas
from typing import Optional

router = APIRouter()

@router.get("/tabelas")
def get_tabelas(
    ano: int = Query(..., description="Ano da consulta"),
    opcao: str = Query(..., description="Opção de categoria"),
    subopcao: Optional[str] = Query(None, description="Subopção da categoria")
):
    try:
        tabelas = scrape_tabelas(ano, subopcao, opcao)

        return {
            "ano": ano,
            "opcao": opcao,
            "subopcao": subopcao,
            "total_linhas": len(tabelas),
            "tabela": tabelas
        }

    except Exception as e:
        return {"erro": str(e)}