# Use uma imagem base Python
FROM python:3.11-slim

# Defina o diretório de trabalho
WORKDIR /app

# Copie o arquivo de requisitos e instale as dependências
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copie o restante da aplicação
COPY . .

# Exponha a porta 8000
EXPOSE 8000

# Comando para iniciar a aplicação
CMD ["python", "main.py"]
