import psycopg2
import pandas as pd
from sqlalchemy import create_engine
from app.security.authentication import Usuario

def get_engine():
    engine = create_engine(
        ''
    )
    return engine


def salvar_dataframe(nome_tabela: str, df: pd.DataFrame):
    # Connection parameters for PostgreSQL over the internet
    conn = get_engine()
    nome_tabela = nome_tabela.replace(" ", "_").replace("-", "_").lower()
    # Write the DataFrame to PostgreSQL
    df.to_sql(nome_tabela, conn, if_exists="replace", index=False, method='multi')
    conn.close()

def listar_tabelas():
    try:
        conn = get_engine()
        query = """
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
            AND table_type = 'BASE TABLE';
        """
        tabelas = pd.read_sql(query, conn)
        return tabelas["name"].tolist()
    except Exception as e:
        return [f"[Erro] {str(e)}"]
    
    
def salvar_usuario(usuario: Usuario):
    try:
        conn = get_engine()
        conn.execute(
            """
            INSERT INTO users (username, password)
            VALUES (%s, %s, %s)
            """,
            (usuario.username, usuario.password)
        )
        print(f"User '{usuario.username}' added successfully.")
    except Exception as e:
        return [f"[Erro] {str(e)}"]
    finally:
        conn.close()