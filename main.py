# API DE LIVROS
#
#
#

from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets
from pydantic import BaseModel
from typing import Optional
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

DATABASE_URL = "sqlite:///./livros.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

app = FastAPI(
    title="API de Livros",
    description="API para gerenciamento de livros",
    version="1.0.0",
)

livros = {}

MEU_USER = "admin"
MINHA_SENHA = "admin"

security = HTTPBasic()


class LivroDB(Base):
    __tablename__ = "Livros"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    autor = Column(String, index=True)
    ano = Column(Integer)
    editora = Column(String, index=True)


class Livro(BaseModel):
    nome: str
    autor: str
    ano: int
    editora: str


Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def autenticar_user(credentials: HTTPBasicCredentials = Depends(security)):
    is_username_correct = secrets.compare_digest(
        credentials.username,
        MEU_USER,
    )
    is_password_correct = secrets.compare_digest(credentials.password, MINHA_SENHA)

    if not (is_username_correct and is_password_correct):
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Basic"},
        )


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}


@app.get("/livros")
def get_livros(
    page: int = Query(1, ge=1, description="Número da página"),
    limit: int = Query(10, ge=1, le=100, description="Número de livros por página"),
    db: Session = Depends(get_db),
    credentials: HTTPBasicCredentials = Depends(autenticar_user),
):
    livros = db.query(LivroDB).offset((page - 1) * limit).limit(limit).all()

    if not livros:
        raise HTTPException(status_code=404, detail="Livros não encontrados")

    total = db.query(LivroDB).count()

    return {
        "page": page,
        "limit": limit,
        "total": total,
        "livros": [
            {
                "id": livro.id,
                "nome": livro.nome,
                "autor": livro.autor,
                "ano": livro.ano,
                "editora": livro.editora,
            }
            for livro in livros
        ],
    }


@app.post("/livros")
def post_livro(
    livro: Livro,
    credentials: HTTPBasicCredentials = Depends(autenticar_user),
    db: Session = Depends(get_db),
):
    db_livro = (
        db.query(LivroDB)
        .filter(LivroDB.nome == livro.nome, LivroDB.autor == livro.autor)
        .first()
    )
    if db_livro:
        raise HTTPException(status_code=400, detail="Livro já cadastrado")
    novo_livro = LivroDB(
        nome=livro.nome, autor=livro.autor, ano=livro.ano, editora=livro.editora
    )
    db.add(novo_livro)
    db.commit()
    db.refresh(novo_livro)
    return {"message": "Livro cadastrado com sucesso"}


@app.put("/livros/{id}")
def update_livro(
    id: int,
    livro: Livro,
    credentials: HTTPBasicCredentials = Depends(autenticar_user),
    db: Session = Depends(get_db),
):
    db_livro = db.query(LivroDB).filter(LivroDB.id == id).first()
    if not db_livro:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    db_livro.nome = livro.nome
    db_livro.autor = livro.autor
    db_livro.ano = livro.ano
    db_livro.editora = livro.editora
    db.commit()
    db.refresh(db_livro)
    return {"message": "Livro atualizado com sucesso"}


@app.delete("/livros/{id}")
def delete_livro(
    id: int,
    credentials: HTTPBasicCredentials = Depends(autenticar_user),
    db: Session = Depends(get_db),
):
    db_livro = db.query(LivroDB).filter(LivroDB.id == id).first()

    if not db_livro:
        raise HTTPException(status_code=404, detail="Livro não encontrado")

    db.delete(db_livro)
    db.commit()

    return {"message": "Livro deletado com sucesso"}
