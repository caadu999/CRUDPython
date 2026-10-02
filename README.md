# EBAC - CRUD de Livros

Projeto de estudos desenvolvido durante o curso da EBAC, com o objetivo de praticar a construção de uma API REST para um CRUD (Create, Read, Update, Delete) utilizando Python.

## 📚 Sobre o projeto

A aplicação simula o gerenciamento de um acervo de livros, permitindo cadastrar, listar (com paginação e ordenação), atualizar e remover registros através de uma API, com autenticação básica protegendo os endpoints. A listagem usa **Redis como cache** para reduzir consultas ao banco.

## 🛠️ Tecnologias utilizadas

* Python
* FastAPI — framework para construção da API
* SQLAlchemy — ORM para comunicação com o banco de dados
* SQLite — banco de dados local (`livros.db`)
* Redis — cache da listagem de livros
* Poetry — gerenciamento de dependências e ambiente virtual
* HTTP Basic Auth — autenticação simples via `HTTPBasicCredentials`
* Uvicorn — servidor ASGI para rodar a aplicação
* Docker / Docker Compose — containerização da aplicação e do Redis

## 🔐 Variáveis de ambiente

| Variável       | Descrição                                      | Exemplo                 |
|----------------|------------------------------------------------|-------------------------|
| `DATABASE_URL` | URL de conexão com o banco de dados (SQLite)   | `sqlite:///./livros.db` |
| `MEU_USER`     | Usuário para autenticação básica               | `admin`                 |
| `MINHA_SENHA`  | Senha para autenticação básica                 | `senha123`              |
| `REDIS_HOST`   | Host do Redis (`localhost` ou `redis` no Docker) | `localhost`           |
| `REDIS_PORT`   | Porta do Redis                                 | `6379`                  |

Crie um arquivo `.env` na raiz do projeto antes de executar a aplicação:

```env
DATABASE_URL=sqlite:///./livros.db
MEU_USER=admin
MINHA_SENHA=senha123
REDIS_HOST=localhost
REDIS_PORT=6379
```

> **Importante:** o código precisa ler o host e a porta do Redis das variáveis de ambiente. No `main.py`, use:
>
> ```python
> redis_client = redis.Redis(
>     host=os.getenv("REDIS_HOST", "localhost"),
>     port=int(os.getenv("REDIS_PORT", 6379)),
>     db=0,
>     decode_responses=True,
> )
> ```
>
> Dentro do Docker Compose, o host do Redis é o **nome do serviço** (`redis`), e não `localhost`.

## 🧠 Como o cache funciona

* `GET /livros` guarda cada resposta no Redis por **30 segundos**. A chave inclui `page`, `size`, `sort_by` e `order`, por exemplo: `livros:page=1&size=10&sort_by=id&order=asc`.
* `POST`, `PUT` e `DELETE` também mantêm a chave individual `livro:{id}` no Redis.
* Após criar, editar ou remover um livro, a listagem pode ficar desatualizada por até 30 segundos (até o cache expirar).
* O endpoint `GET /debug/redis` exibe as chaves armazenadas e o TTL de cada uma (útil apenas para estudo).

## ▶️ Como executar

Você pode executar o projeto com Docker Compose (aplicação + Redis) ou localmente com Poetry.

### Opção 1: Docker Compose (recomendada)

1. Crie o arquivo `.env` na raiz do projeto, com `REDIS_HOST=redis` (veja a seção [Variáveis de ambiente](#-variáveis-de-ambiente)).

2. Garanta que o `docker-compose.yml` tenha o serviço do Redis. Exemplo:

```yaml
services:
  app:
    build: .
    ports:
      - "8000:8000"
    env_file: .env
    environment:
      - REDIS_HOST=redis
    depends_on:
      - redis

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
```

3. Suba os serviços:

```bash
docker compose up --build
```

4. Acesse a documentação interativa da API em:

```
http://127.0.0.1:8000/docs
```

5. Para parar e remover os containers:

```bash
docker compose down
```

### Opção 2: Poetry (ambiente local)

Neste modo, a aplicação roda na sua máquina e precisa de um Redis acessível em `localhost:6379`. Escolha uma das formas abaixo para subir o Redis.

#### Redis via Docker (mais simples)

```bash
docker run -d --name redis-livros -p 6379:6379 redis:7-alpine
```

Para parar e remover:

```bash
docker stop redis-livros && docker rm redis-livros
```

#### Redis instalado localmente

* **Ubuntu/Debian:**
  ```bash
  sudo apt update && sudo apt install redis-server
  sudo systemctl start redis-server
  ```
* **macOS (Homebrew):**
  ```bash
  brew install redis
  brew services start redis
  ```
* **Windows:** use o WSL (Ubuntu) e siga os passos do Ubuntu, ou use o Docker.

Para confirmar que o Redis está respondendo:

```bash
redis-cli ping
# PONG
```

#### Rodando a aplicação

1. Instale as dependências:

```bash
poetry install
```

2. Ative o ambiente virtual:

```bash
poetry shell
```

3. Crie o arquivo `.env` (com `REDIS_HOST=localhost`) ou defina as variáveis manualmente:

```bash
export DATABASE_URL="sqlite:///./livros.db"
export MEU_USER="admin"
export MINHA_SENHA="senha123"
export REDIS_HOST="localhost"
export REDIS_PORT="6379"
```

4. Execute a aplicação:

```bash
uvicorn main:app --reload
```

5. Acesse a documentação interativa da API em:

```
http://127.0.0.1:8000/docs
```

## ✅ Funcionalidades

* Cadastrar livros (`POST /livros`)
* Listar livros com paginação e ordenação (`GET /livros`)
* Atualizar informações de um livro (`PUT /livros/{id}`)
* Remover um livro (`DELETE /livros/{id}`)
* Cache da listagem com Redis (TTL de 30 segundos)
* Autenticação básica (HTTP Basic Auth) nos endpoints de livros

## 📖 Endpoints principais

| Método | Rota            | Descrição                                                     | Autenticação |
|--------|-----------------|---------------------------------------------------------------|:------------:|
| GET    | `/livros`       | Lista livros com paginação (`page`, `size`) e ordenação (`sort_by`, `order`) | ✅ |
| POST   | `/livros`       | Cadastra um novo livro                                        | ✅           |
| PUT    | `/livros/{id}`  | Atualiza um livro existente                                   | ✅           |
| DELETE | `/livros/{id}`  | Remove um livro                                               | ✅           |
| GET    | `/debug/redis`  | Mostra as chaves e TTLs do cache (apenas para desenvolvimento) | ❌          |

### Parâmetros de `GET /livros`

| Parâmetro | Padrão | Descrição                                              |
|-----------|--------|--------------------------------------------------------|
| `page`    | `1`    | Número da página                                       |
| `size`    | `10`   | Livros por página (máximo 100)                         |
| `sort_by` | `id`   | Campo de ordenação: `id`, `nome`, `autor`, `ano`, `editora` |
| `order`   | `asc`  | Direção: `asc` ou `desc`                               |

Exemplo:

```bash
curl -u admin:senha123 "http://127.0.0.1:8000/livros?page=1&size=5&sort_by=ano&order=desc"
```

### Modelo de dados (`Livro`)

```json
{
  "nome": "string",
  "autor": "string",
  "ano": 0,
  "editora": "string"
}
```

## 🎓 Contexto

Este repositório foi criado exclusivamente para fins didáticos, como parte das atividades do curso de Python da EBAC.