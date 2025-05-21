from fastapi import APIRouter, Query
from app.scraper import scrape_tabelas
from app.db import salvar_dataframe
from typing import Optional
import time
from app.db_utils import listar_tabelas
import pandas as pd
import sqlite3

router = APIRouter()

DB_PATH = "app/dados.db"  # Caminho fixo para o banco

@router.get("/tabelas/disponiveis", description="Lista todas as tabelas atualmente salvas no banco de dados SQLite")
def get_tabelas_disponiveis():
    return {
        "tabelas_salvas": listar_tabelas()
    }

@router.get("/tabelas")
def get_tabelas_range(
    ano_inicio: int = Query(..., description="Ano inicial da consulta"),
    ano_fim: int = Query(..., description="Ano final da consulta"),
    opcao: str = Query(..., description="Opção de categoria"),
    subopcao: Optional[str] = Query(None, description="Subopção da categoria (opcional)"),
    intervalo: float = 1.5  # para o sleep
):
    resultados = []

    for ano in range(ano_inicio, ano_fim + 1):
        try:
            tabelas = scrape_tabelas(ano, subopcao, opcao)
            resultados.append({
                "ano": ano,
                "fonte": "web",
                "total_linhas": len(tabelas),
                "tabela": tabelas
            })
        except Exception as e:
            nome_tabela = f"tabela_{opcao}_{subopcao}_{ano}".replace("-", "_")
            try:
                with sqlite3.connect(DB_PATH) as conn:
                    df = pd.read_sql(f"SELECT * FROM '{nome_tabela}'", conn)
                    resultados.append({
                        "ano": ano,
                        "fonte": "banco_de_dados",
                        "total_linhas": len(df),
                        "tabela": df.values.tolist()
                    })
            except Exception as db_error:
                resultados.append({
                    "ano": ano,
                    "fonte": "erro",
                    "erro": str(e),
                    "fallback_erro": str(db_error)
                })

        time.sleep(intervalo)

    return {
        "intervalo_usado": intervalo,
        "anos_consultados": list(range(ano_inicio, ano_fim + 1)),
        "resultados": resultados
    }