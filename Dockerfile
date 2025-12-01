FROM python:3.11-slim AS builder

WORKDIR /app

# Evita erros de compilação
RUN apt-get update && apt-get install -y \
    git \
    libprotobuf-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

COPY . .

FROM python:3.11-slim

WORKDIR /app

# Copia libs do usuário
COPY --from=builder /root/.local /root/.local
COPY . .

ENV PATH=/root/.local/bin:$PATH

EXPOSE 8080

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]