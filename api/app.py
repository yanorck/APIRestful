from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
import os
import bcrypt
import jwt
from datetime import datetime, timedelta
from scraping import scrape_data

# Configurações do JWT
SECRET_KEY = os.getenv("SECRET_KEY", "mysecretkey")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 2880 #2 dias de duração do token

# Funções para hash e verificação da senha
def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(stored_password: str, provided_password: str) -> bool:
    return bcrypt.checkpw(provided_password.encode(), stored_password.encode())

# Configurações do banco de dados
DATABASE_URL = os.getenv('DATABASE_URL')
Base = declarative_base()
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Modelo de dados
class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, index=True)
    senha = Column(String)

# Criar as tabelas no banco de dados
Base.metadata.create_all(bind=engine)

# Modelos Pydantic para validação
class UserCreate(BaseModel):
    name: str
    email: str
    senha: str

class UserLogin(BaseModel):
    email: str
    senha: str

# Função para criar o token JWT
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Instância do FastAPI
app = FastAPI()

# Endpoint para registro de usuário
@app.post("/registrar")
def registra_user(user: UserCreate):
    db = SessionLocal()
    
    # Verifica se o usuário já existe
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        db.close()
        raise HTTPException(status_code=409, detail="Email já registrado")
    
    # Hash da senha e criação do novo usuário
    hashed_password = hash_password(user.senha)
    db_user = User(name=user.name, email=user.email, senha=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    # Criação do token JWT para o novo usuário
    token_data = {"sub": db_user.email}
    jwt_token = create_access_token(data=token_data)
    
    db.close()
    return {"jwt": jwt_token}

# Endpoint para login do usuário
@app.post("/login")
def verifica_login(user: UserLogin):
    db = SessionLocal()
    
    # Verifica se o email existe no banco
    userbase = db.query(User).filter(User.email == user.email).first()
    if not userbase:
        db.close()
        raise HTTPException(status_code=401, detail="Email não encontrado")
    
    # Verifica se a senha está correta
    if not verify_password(userbase.senha, user.senha):
        db.close()
        raise HTTPException(status_code=401, detail="Senha e e-mail não conferem")
    
    # Cria o token JWT
    token_data = {"sub": userbase.email}
    jwt_token = create_access_token(data=token_data)
    
    db.close()
    return {"jwt": jwt_token}

# Função principal de consulta token
def consulta(Authorization: str):
    token = Authorization.split(" ")[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        scraped_data = scrape_data("https://myanimelist.net/topanime.php?type=upcoming")
        return scraped_data
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=403, detail="Token expirado")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=403, detail="Token inválido")

# Endpoint para consultar o token
@app.get("/consultar")
def consultar(Authorization: str = Header(None)):
    if Authorization is None:
        raise HTTPException(status_code=403, detail="Autorização ausente")
    return consulta(Authorization)
