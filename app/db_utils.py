import sqlite3
import pandas as pd

def listar_tabelas(caminho_db: str = "app/dados.db"):
    try:
        conn = sqlite3.connect(caminho_db)
        tabelas = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';", conn)
        return tabelas["name"].tolist()
    except Exception as e:
        return [f"[Erro] {str(e)}"]