import requests
from bs4 import BeautifulSoup
import re
import logging
import sys
from diskcache import Cache
from app.datasource.db_queries import salvar_dataframe
import pandas as pd

# Configuração do logger para salvar em arquivo e imprimir no console
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(name)s | %(message)s',
    handlers=[
        logging.FileHandler("scraper.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("ScraperVitibrasil")

# Inicializa cache opcional
cache = Cache("./cache")

def separar_texto_concatenado(texto):
    # Separa palavras concatenadas com letras maiúsculas no meio
    partes = re.split(r'(?<=[a-z])(?=[A-Z])', texto)
    logger.debug(f"Separando texto concatenado: '{texto}' => {partes}")
    return partes

def limpar_linha(dados_linha):
    #Remove entradas irrelevantes e separa textos agrupados
    ignorar = {"TOPO", "DOWNLOAD", ""}
    resultado = []

    for campo in dados_linha:
        if campo.upper() in ignorar:
            logger.debug(f"Ignorando campo: '{campo}'")
            continue
        # Verifica se o campo parece ter nomes ou palavras concatenadas
        if len(campo) > tamanho_minimo and " " not in campo:
            separado = separar_texto_concatenado(campo)
            resultado.extend(separado)
            logger.debug(f"Campo longo separado: '{campo}' => {separado}")
        else:
            resultado.append(campo.strip())

    return resultado

def scrape_tabelas(ano: int, subopcao: str, opcao: str = None, salvar: bool = True, usar_cache: bool = True):
    #Faz scraping da tabela do site Vitibrasil, com cache e salvamento opcional.
    logger.info(f"Iniciando scraping: ano={ano}, subopcao={subopcao}, opcao={opcao}")
    base_url = "http://vitibrasil.cnpuv.embrapa.br/index.php"
    params = {'ano': ano}
    if subopcao:
        params['subopcao'] = subopcao
    if opcao:
        params['opcao'] = opcao

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(base_url, params=params, headers=headers)
        response.raise_for_status()
        logger.info(f"Requisição bem-sucedida: {response.url}")
    except requests.RequestException as e:
        logger.error(f"Erro na requisição HTTP: {e}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")

    # Ajuste na busca da tabela: checa se ambas classes estão presentes
    tabela_principal = soup.find("table", class_=lambda c: c and "tb_base" in c and "tb_dados" in c)

    if not tabela_principal:
        logger.warning("Tabela principal não encontrada na página.")
        return []

    dados_tabela = []
    total_linhas = 0

    for linha in tabela_principal.find_all("tr"):
        colunas = linha.find_all(["td", "th"])
        dados_linha = [coluna.get_text(strip=True) for coluna in colunas]

        if dados_linha and any(campo.strip() for campo in dados_linha):
            dados_limpos = limpar_linha(dados_linha)
            if dados_limpos:
                dados_tabela.append(dados_limpos)
                total_linhas += 1
                logger.debug(f"Linha processada: {dados_limpos}")

    logger.info(f"Total de linhas processadas: {total_linhas}")
    return dados_tabela

    
