# Use uma imagem base Python
FROM python:3.11

# Defina o diretório de trabalho
WORKDIR /app

# Copie o arquivo de requisitos e instale as dependências
COPY requirements.txt .

RUN pip install -r requirements.txt

# Copie o restante da aplicação
COPY . .

# Exponha a porta 8080
EXPOSE 8000

# Comando para iniciar a aplicação
CMD ["uvicorn", "app.api:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
