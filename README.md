# EBAC - CRUD de Livros

Projeto de estudos desenvolvido durante o curso da EBAC, com o objetivo de praticar a construção de uma API REST para um CRUD (Create, Read, Update, Delete) utilizando Python.

## 📚 Sobre o projeto

A aplicação simula o gerenciamento de um acervo de livros, permitindo cadastrar, listar (com paginação), atualizar e remover registros através de uma API, com autenticação básica protegendo os endpoints.

## 🛠️ Tecnologias utilizadas

* Python
* FastAPI — framework para construção da API
* SQLAlchemy — ORM para comunicação com o banco de dados
* SQLite — banco de dados local (`livros.db`)
* Poetry — gerenciamento de dependências e ambiente virtual
* HTTP Basic Auth — autenticação simples via `HTTPBasicCredentials`
* Uvicorn — servidor ASGI para rodar a aplicação
* Docker / Docker Compose — containerização da aplicação

## 🔐 Variáveis de ambiente

A aplicação depende das seguintes variáveis de ambiente:

| Variável       | Descrição                                      | Exemplo                  |
|----------------|-------------------------------------------------|---------------------------|
| `DATABASE_URL` | URL de conexão com o banco de dados (SQLite)    | `sqlite:///./livros.db`  |
| `MEU_USER`     | Usuário para autenticação básica                | `user`                  |
| `MINHA_SENHA`  | Senha para autenticação básica                  | `senha123`               |

Crie um arquivo `.env` na raiz do projeto com essas variáveis antes de executar a aplicação:

```env
DATABASE_URL=sqlite:///./livros.db
MEU_USER=admin
MINHA_SENHA=senha123
```

## ▶️ Como executar

Você pode executar o projeto localmente com Poetry ou via Docker Compose.

### Opção 1: Docker Compose

O projeto já conta com um `docker-compose.yml` configurado, que lê as variáveis do arquivo `.env` (`env_file: .env`).

1. Crie o arquivo `.env` na raiz do projeto (veja a seção [Variáveis de ambiente](#-variáveis-de-ambiente)).

2. Suba a aplicação:

```bash
docker compose up --build
```

3. Acesse a documentação interativa da API em:

```
http://127.0.0.1:8000/docs
```

4. Para parar e remover os containers:

```bash
docker compose down
```

### Opção 2: Poetry (ambiente local)

1. Instale as dependências:

```bash
poetry install
```

2. Ative o ambiente virtual:

```bash
poetry shell
```

3. Defina as variáveis de ambiente (ou crie um arquivo `.env`):

```bash
export DATABASE_URL="sqlite:///./livros.db"
export MEU_USER="user"
export MINHA_SENHA="senha123"
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
* Listar livros com paginação (`GET /livros`)
* Atualizar informações de um livro (`PUT /livros/{id}`)
* Remover um livro (`DELETE /livros/{id}`)
* Autenticação básica (HTTP Basic Auth) em todos os endpoints protegidos

## 📖 Endpoints principais

| Método | Rota            | Descrição                                  | Autenticação |
|--------|-----------------|---------------------------------------------|:-------------:|
| GET    | `/livros`       | Lista livros com paginação (`page`, `limit`) | ✅            |
| POST   | `/livros`       | Cadastra um novo livro                       | ✅            |
| PUT    | `/livros/{id}`  | Atualiza um livro existente                  | ✅            |
| DELETE | `/livros/{id}`  | Remove um livro                              | ✅            |

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