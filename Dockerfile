# utilização de imagem base Python
FROM python:3.9-slim

# Define o diretório de trabalho
WORKDIR /app

# Copia o requirements.txt e instala as dependências 
COPY app/requirements.txt .

# Instalação
RUN pip install --no-cache-dir -r requirements.txt

#Copia o código da aplicação
COPY app/ .

# Define a variavel de ambiente 
ENV FLASK_APP=server.py
ENV FLASK_RUN_HOST=0.0.0.0

# Expõe porta
EXPOSE 5000

# Comando para rodar a aplicação
CMD ["flask", "run"]