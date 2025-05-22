import requests
from bs4 import BeautifulSoup
import re
from diskcache import Cache
from app.datasource.db_queries import salvar_dataframe
import pandas as pd

cache = Cache("./cache") 

def separar_texto_concatenado(texto):
    # Separa palavras concatenadas com letras maiúsculas no meio
    return re.split(r'(?<=[a-z])(?=[A-Z])', texto)

def limpar_linha(dados_linha):
    """Remove entradas irrelevantes e separa textos agrupados"""
    ignorar = {"TOPO", "DOWNLOAD", ""}
    resultado = []
    for campo in dados_linha:
        if campo.upper() in ignorar:
            continue
        # Verifica se o campo parece ter nomes ou palavras concatenadas
        if len(campo) > 40 and not " " in campo:
            resultado.extend(separar_texto_concatenado(campo))
        else:
            resultado.append(campo.strip())
    return resultado

def scrape_tabelas(ano: int, subopcao: str, opcao: str = None):
    base_url = "http://vitibrasil.cnpuv.embrapa.br/index.php"
    url = f"{base_url}?ano={ano}&subopcao={subopcao}&opcao={opcao}"

    if subopcao:
        url = f"{base_url}?ano={ano}&subopcao={subopcao}&opcao={opcao}"
    else:
        url = f"{base_url}?ano={ano}&opcao={opcao}"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    tabela_principal = soup.find("table", class_="tb_base tb_dados")

    if not tabela_principal:
        raise ValueError(f"[Erro] Nenhuma tabela encontrada para ano={ano}, opcao={opcao}, subopcao={subopcao}")

    dados_tabela = []
    for linha in tabela_principal.find_all("tr"):
        colunas = linha.find_all(["td", "th"])
        dados_linha = [coluna.get_text(strip=True) for coluna in colunas]

        if dados_linha and any(campo.strip() for campo in dados_linha):
            dados_limpos = limpar_linha(dados_linha)
            if dados_limpos:
                dados_tabela.append(dados_limpos)

    if dados_tabela:
        df = pd.DataFrame(dados_tabela)
        nome_tabela = f"tabela_{opcao}_{subopcao}_{ano}".replace("-", "_")
        salvar_dataframe(nome_tabela, df)

    return dados_tabela
