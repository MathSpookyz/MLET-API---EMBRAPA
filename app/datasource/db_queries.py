import psycopg2
import pandas as pd
from sqlalchemy import create_engine
from app.infra.env_variable import database_access, MetaData, Table, Column, Integer, String
from pydantic import BaseModel


class Usuario(BaseModel):
    username: str
    senha_hash: str

def get_engine():
    engine = create_engine(
        database_access
    )
    return engine


def salvar_dataframe(nome_tabela: str, df: pd.DataFrame):
    # Connection parameters for PostgreSQL over the internet
    conn = get_engine()
    nome_tabela = nome_tabela.replace(" ", "_").replace("-", "_").lower()
    # Write the DataFrame to PostgreSQL
    # df.to_sql(nome_tabela, conn, if_exists="append", index=False, method='multi')
    df.to_sql(nome_tabela, con=conn, index=False, if_exists='replace')

def listar_tabelas():
    try:
        conn = get_engine()
        query = """
            SELECT table_name
            FROM tables
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
        # Define a table
        metadata = MetaData()
        users = Table('users', metadata,
            Column('id', Integer, primary_key=True,autoincrement=True),
            Column('username', String),
            Column('password', String)
        )

        # Create the table if it does not exist
        metadata.create_all(conn, checkfirst=True)

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

def obter_usuario_db(username: str):
    try:
        conn = get_engine()
        conn.execute("""
            SELECT username, senha_hash 
            FROM users 
            WHERE username = %s
            """, (username,))
        user = conn.fetchone()
        
        if user:
            return {
                "username": user[0],
                "senha_hash": user[1]
            }
        return None
        
    except Exception as e:
        raise Exception(
            status_code="500",
            detail=f"Database error: {str(e)}"
        )