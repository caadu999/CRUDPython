# EBAC - CRUD de Livros

Projeto de estudos desenvolvido durante o curso da EBAC, com o objetivo de praticar a construção de uma API REST para um CRUD (Create, Read, Update, Delete) utilizando Python, evoluído com cache em Redis e tarefas em segundo plano com Celery.

## 📚 Sobre o projeto

A aplicação simula o gerenciamento de um acervo de livros, permitindo cadastrar, listar (com paginação e ordenação), atualizar e remover registros através de uma API, com autenticação básica protegendo os endpoints de livros.

Além do CRUD, o projeto conta com:

- **Cache no Redis** na listagem de livros (30 segundos).
- **Tarefas assíncronas com Celery** (soma e fatorial), usando o Redis como broker e backend de resultados.
- **Histórico das últimas 50 tarefas** enviadas, guardado no Redis.

## 🛠️ Tecnologias utilizadas

- Python 3.14
- FastAPI — framework para construção da API
- SQLAlchemy — ORM para comunicação com o banco de dados
- SQLite — banco de dados local (`livros.db`)
- Redis — cache da listagem, broker e backend do Celery
- Celery — processamento de tarefas em segundo plano
- Poetry — gerenciamento de dependências e ambiente virtual
- HTTP Basic Auth — autenticação simples via `HTTPBasicCredentials`
- Uvicorn — servidor ASGI para rodar a aplicação
- Docker / Docker Compose — containerização da aplicação

## 🗂️ Estrutura do projeto

```
.
├── main.py              # API FastAPI (rotas, modelos, cache e autenticação)
├── celery_app.py        # Configuração do Celery
├── tasks.py             # Tarefas do Celery (somar e fatorial)
├── Dockerfile
├── docker-compose.yml   # Serviços: app, redis e celery
├── pyproject.toml       # Dependências (Poetry)
├── poetry.lock
└── .env                 # Variáveis de ambiente (não versionado)
```

## 🏗️ Arquitetura

O `docker-compose.yml` sobe três serviços:

| Serviço  | Função                                                  |
| -------- | ------------------------------------------------------- |
| `app`    | API FastAPI, exposta na porta `8000`                    |
| `redis`  | Cache da listagem e broker/backend do Celery            |
| `celery` | Worker que consome a fila `livros` e executa as tarefas |

A API e o worker compartilham o mesmo código (volume `.:/app`) e se comunicam com o Redis pelo nome do serviço (`redis`).

## 🔐 Variáveis de ambiente

A aplicação depende das seguintes variáveis de ambiente:

| Variável       | Descrição                                          | Exemplo                 |
| -------------- | -------------------------------------------------- | ----------------------- |
| `DATABASE_URL` | URL de conexão com o banco de dados (SQLite)       | `sqlite:///./livros.db` |
| `MEU_USER`     | Usuário para autenticação básica                   | `admin`                 |
| `MINHA_SENHA`  | Senha para autenticação básica                     | `senha123`              |
| `REDIS_HOST`   | Host do Redis (nome do serviço no Docker Compose)  | `redis`                 |
| `REDIS_PORT`   | Porta do Redis                                     | `6379`                  |
| `REDIS_URL`    | (Opcional) URL completa do Redis usada pelo Celery | `redis://redis:6379/0`  |

Crie um arquivo `.env` na raiz do projeto com essas variáveis antes de executar a aplicação:

```
DATABASE_URL=sqlite:///./livros.db
MEU_USER=admin
MINHA_SENHA=senha123
REDIS_HOST=redis
REDIS_PORT=6379
```

> Rodando fora do Docker, use `REDIS_HOST=localhost`. No `main.py` o valor padrão é `localhost`, e no `celery_app.py` é `redis`.

## ▶️ Como executar

Você pode executar o projeto localmente com Poetry ou via Docker Compose.

### Opção 1: Docker Compose

O projeto já conta com um `docker-compose.yml` configurado, que lê as variáveis do arquivo `.env` (`env_file: .env`).

1. Crie o arquivo `.env` na raiz do projeto (veja a seção [Variáveis de ambiente](#-variáveis-de-ambiente)).

2. Suba a aplicação:

```
docker compose up --build
```

3. Acesse a documentação interativa da API em:

```
http://127.0.0.1:8000/docs
```

4. Para parar e remover os containers:

```
docker compose down
```

Comandos úteis:

```
docker compose ps                 # serviços em execução
docker compose logs -f app        # logs da API
docker compose logs -f celery     # logs do worker
docker compose restart celery     # reinicia o worker (após mudar as tarefas)
```

No log do worker, confira se a fila `livros` aparece em `[queues]` e se `tasks.somar` e `tasks.fatorial` aparecem em `[tasks]`.

### Opção 2: Poetry (ambiente local)

É necessário ter um Redis rodando na máquina.

1. Instale as dependências:

```
poetry install
```

2. Defina as variáveis de ambiente (ou crie um arquivo `.env`, que a API carrega automaticamente):

```
export DATABASE_URL="sqlite:///./livros.db"
export MEU_USER="admin"
export MINHA_SENHA="senha123"
export REDIS_HOST="localhost"
```

3. Execute a API:

```
poetry run uvicorn main:app --reload
```

4. Em outro terminal, com as mesmas variáveis exportadas, execute o worker do Celery:

```
poetry run celery -A celery_app:celery_app worker -Q livros --loglevel=info
```

5. Acesse a documentação interativa da API em:

```
http://127.0.0.1:8000/docs
```

## ✅ Funcionalidades

- Cadastrar livros (`POST /livros`), sem permitir duplicidade de nome e autor
- Listar livros com paginação e ordenação (`GET /livros`)
- Atualizar informações de um livro (`PUT /livros/{id}`)
- Remover um livro (`DELETE /livros/{id}`)
- Cache da listagem no Redis por 30 segundos
- Envio de tarefas de soma e fatorial para processamento em segundo plano
- Consulta das tarefas recentes com status e resultado
- Autenticação básica (HTTP Basic Auth) nos endpoints de livros

## 📖 Endpoints principais

| Método | Rota                | Descrição                                                    | Autenticação |
| ------ | ------------------- | ------------------------------------------------------------ | ------------ |
| GET    | `/livros`           | Lista livros (`page`, `size`, `sort_by`, `order`)            | ✅            |
| POST   | `/livros`           | Cadastra um novo livro                                       | ✅            |
| PUT    | `/livros/{id}`      | Atualiza um livro existente                                  | ✅            |
| DELETE | `/livros/{id}`      | Remove um livro                                              | ✅            |
| POST   | `/calcular/soma`    | Envia uma tarefa de soma (`a`, `b`) e devolve o `task_id`    | ❌            |
| POST   | `/calcular/fatorial`| Envia uma tarefa de fatorial (`n`) e devolve o `task_id`     | ❌            |
| GET    | `/tarefas/recentes` | Lista as últimas 50 tarefas com status e resultado           | ❌            |
| GET    | `/debug/redis`      | Lista os livros guardados no Redis (depuração)              | ❌            |
| GET    | `/`                 | Rota de teste                                                | ❌            |
| GET    | `/items/{item_id}`  | Rota de exemplo com parâmetros                               | ❌            |

### Parâmetros do `GET /livros`

| Parâmetro | Padrão | Descrição                                                   |
| --------- | ------ | ----------------------------------------------------------- |
| `page`    | `1`    | Número da página (mínimo 1)                                 |
| `size`    | `10`   | Livros por página (1 a 100)                                 |
| `sort_by` | `id`   | Campo de ordenação: `id`, `nome`, `autor`, `ano`, `editora` |
| `order`   | `asc`  | Direção da ordenação: `asc` ou `desc`                       |

Exemplo: `GET /livros?page=1&size=10&sort_by=nome&order=asc`

### Modelo de dados (`Livro`)

```
{
  "nome": "string",
  "autor": "string",
  "ano": 0,
  "editora": "string"
}
```

### Tarefas com Celery

1. Envie uma tarefa, por exemplo `POST /calcular/soma?a=2&b=3`. Os valores vão como *query params*, sem body. A resposta traz o `task_id`.
2. Consulte `GET /tarefas/recentes`. O status passa por `PENDING`, `STARTED` e `SUCCESS` (cada tarefa leva 3 segundos para simular um processamento demorado).
3. No fatorial, um `n` negativo gera um erro na tarefa, e o status final é `FAILURE`.

## 🧪 Testando no Postman

- **Autenticação:** aba *Authorization* → *Basic Auth* com `MEU_USER` e `MINHA_SENHA`.
- **POST /livros:** *Body* → *raw* → *JSON*, com o modelo de dados acima.
- **POST /calcular/\*:** os valores vão na URL, sem body.

## ⚠️ Pontos de atenção

- As rotas `/calcular/*`, `/tarefas/recentes` e `/debug/redis` não exigem autenticação. Proteja-as antes de qualquer uso fora de estudo.
- Os dados da listagem ficam em cache por 30 segundos, e o cadastro, a atualização e a remoção não invalidam esse cache.
- O SQLite é um arquivo local, e escritas simultâneas podem dar `database is locked`. Para algo além de estudo, prefira PostgreSQL.
- O `.env` e o `livros.db` estão no `.gitignore` e não devem ser versionados.

## 🎓 Contexto

Este repositório foi criado exclusivamente para fins didáticos, como parte das atividades do curso de Python da EBAC.