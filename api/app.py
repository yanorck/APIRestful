# app.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declarative_base, sessionmaker  # Modificado

import os

# Configurações do banco de dados
DATABASE_URL = os.getenv('DATABASE_URL')


# Criação da instância do FastAPI
app = FastAPI()

# Configuração do SQLAlchemy
Base = declarative_base()  
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Modelo de dados
class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)

# Criar as tabelas no banco de dados
Base.metadata.create_all(bind=engine)

# Pydantic model para validação
class ItemCreate(BaseModel):
    name: str
    description: str

@app.post("/items")
def create_item(item: ItemCreate):
    db = SessionLocal()
    db_item = Item(name=item.name, description=item.description)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    db.close()
    return db_item

@app.get("/items/{item_id}")
def read_item(item_id: int):
    db = SessionLocal()
    item = db.query(Item).filter(Item.id == item_id).first()
    db.close()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.get("/items")
def read_items():
    db = SessionLocal()
    items = db.query(Item).all()
    db.close()
    return items
