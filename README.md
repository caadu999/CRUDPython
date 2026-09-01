# EBAC - CRUD de Livros

Projeto de estudos desenvolvido durante o curso da **EBAC**, com o objetivo de praticar a construção de uma API REST para um CRUD (Create, Read, Update, Delete) utilizando Python.

## 📚 Sobre o projeto

A aplicação simula o gerenciamento de um acervo de livros, permitindo cadastrar, listar, atualizar e remover registros através de uma API, com autenticação básica protegendo os endpoints.

## 🛠️ Tecnologias utilizadas

- **Python**
- **FastAPI** — framework para construção da API
- **SQLAlchemy** — ORM para comunicação com o banco de dados
- **SQLite** — banco de dados local (`livros.db`)
- **Poetry** — gerenciamento de dependências e ambiente virtual
- **HTTP Basic Auth** — autenticação simples via `HTTPBasicCredentials`
- **Uvicorn** — servidor ASGI para rodar a aplicação


## ▶️ Como executar

1. Instale as dependências com o Poetry:
   ```bash
   poetry install
   ```

2. Ative o ambiente virtual:
   ```bash
   poetry shell
   ```

3. Execute a aplicação:
   ```bash
   uvicorn main:app --reload
   ```

4. Acesse a documentação interativa da API em:
   ```
   http://127.0.0.1:8000/docs
   ```

## ✅ Funcionalidades

- Cadastrar livros
- Listar livros
- Atualizar informações de um livro
- Remover um livro
- Autenticação básica nos endpoints protegidos

## 🎓 Contexto

Este repositório foi criado exclusivamente para fins didáticos, como parte das atividades práticas do curso de Python da **EBAC (Escola Britânica de Artes Criativas e Tecnologia)**.