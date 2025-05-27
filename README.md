Projeto Viniculas - Tech Challenge Fiap

O Projeto segue a seguinte arquitetura:
/app - raiz do projeto
- /api - endpoint que podem ser acessados externamente
- /cache - cache de dados
- /datasource - acesso a dados externos e banco de dados
- /security - controle de acesso e geração de token de segurança

## Arquitetura da aplicação
![arquitetura](./projeto-fiap.drawio.png)


## Gráfico de fluxo de acesso da aplicação
```mermaid
sequenceDiagram
    box Green Python Backend
    actor Usuário
    participant RestBackend
    participant Scraper
    participant Cache
    end
    box Blue Site Embrapa
    participant Vitivinicultura
    end    
    Usuário->>RestBackend: Chamada do endpoint /producao
    RestBackend->> Scraper: Requisita busca de dados da Vinicula
    Scraper ->> Cache: Valida cache de dados
    Scraper ->> Vitivinicultura: Dados expirados, busca de dados direto no site
    Vitivinicultura ->> Scraper: Retorno de dados
    RestBackend->>Usuário: Resposta REST com os dados buscados sobre produção
```

Buildar imagem com "sudo DOCKER_BUILDKIT=1 docker-compose build"
Executar imagem com "sudo docker-compose up -d"