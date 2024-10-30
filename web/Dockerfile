FROM nginx:latest

RUN apt-get -y update
RUN apt-get -y install net-tools iputils-ping

# Copiar o arquivo de configuração do Nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copiar o restante dos arquivos da aplicação (caso tenha)
COPY . /usr/share/nginx/html

COPY hello.txt /