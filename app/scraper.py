import requests
from bs4 import BeautifulSoup

def scrape_tabelas(ano: int, subopcao: str, opcao: str):
    base_url = "http://vitibrasil.cnpuv.embrapa.br/index.php"
    url = f"{base_url}?ano={ano}&subopcao={subopcao}&opcao={opcao}"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    tabelas_html = soup.find_all("table")

    todas_tabelas = []

    for tabela in tabelas_html:
        linhas = tabela.find_all("tr")
        dados_tabela = []

        for linha in linhas:
            colunas = linha.find_all(["td", "th"])
            dados_linha = [coluna.get_text(strip=True) for coluna in colunas]
            if dados_linha:
                dados_tabela.append(dados_linha)

        if dados_tabela:
            todas_tabelas.append(dados_tabela)

    return todas_tabelas