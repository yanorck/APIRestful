FROM ubuntu:22.04

# Atualizando o sistema e instalando dependências
RUN apt-get update && \
    apt-get install -y software-properties-common && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update && \
    apt-get install -y python3.10 python3.10-venv python3.10-dev python3-pip && \
    apt-get clean

# Definindo o diretório de trabalho
WORKDIR /api
# Copiando os arquivos de requisitos
COPY requirements.txt . 

# Instalando as dependências
RUN python3.10 -m pip install --no-cache-dir -r requirements.txt

# Copiando o restante dos arquivos da aplicação
COPY . .

# Copiando o script de espera
COPY wait_for_db.py .

# Definindo o comando para rodar a aplicação
CMD ["sh", "-c", "python3.10 wait_for_db.py && uvicorn app:app --host 0.0.0.0 --port 5000"]
