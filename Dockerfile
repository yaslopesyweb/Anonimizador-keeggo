FROM python:3.11-slim

# Não bufferizar stdout/stderr
ENV PYTHONUNBUFFERED=1
WORKDIR /app

# Dependências de sistema necessárias para construir pacotes e para spaCy
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       build-essential \
       gcc \
       git \
       curl \
       wget \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements e instalar
COPY requirements.txt ./

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Baixar o modelo do spaCy (pt_core_news_lg)
RUN python -m spacy download pt_core_news_lg

# Copiar o restante da aplicação
COPY . /app

EXPOSE 8501

CMD ["streamlit", "run", "anonimizador_streamlit.py", "--server.port=8501", "--server.address=0.0.0.0"]
