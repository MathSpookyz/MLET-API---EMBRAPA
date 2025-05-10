from fastapi import APIRouter, Query
from app.scraper import scrape_tabelas

router = APIRouter()

@router.get("/tabelas")
def get_tabelas(
    ano: int = Query(..., description="Ano da consulta"),
    subopcao: str = Query(..., description="Subopção da categoria"),
    opcao: str = Query(..., description="Opção de categoria")
):
    try:
        tabelas = scrape_tabelas(ano, subopcao, opcao)
        return {"ano": ano, "opcao": opcao, "tabelas": tabelas, "subopcao": subopcao}
    except Exception as e:
        return {"erro": str(e)}