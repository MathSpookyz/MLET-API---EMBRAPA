import sqlite3
import pandas as pd
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "dados.db")

def salvar_dataframe(nome_tabela: str, df: pd.DataFrame):
    conn = sqlite3.connect(DB_PATH)

    # Trata o nome da tabela para ser compatível com o SQLite
    nome_tabela = nome_tabela.replace(" ", "_").replace("-", "_").lower()

    # Substitui a tabela se ela já existir
    df.to_sql(nome_tabela, conn, if_exists="replace", index=False)

    conn.close()