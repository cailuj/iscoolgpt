# 🚀 **IsCoolGPT – Assistente Inteligente em Nuvem (FastAPI + FLAN-T5 + AWS ECS)**

O **IsCoolGPT** é um assistente baseado em IA que utiliza o modelo **FLAN-T5** para responder perguntas relacionadas a cloud computing.
A API foi desenvolvida com **FastAPI**, empacotada via **Docker**, automatizada com **GitHub Actions** e implantada de forma totalmente gerenciada no **AWS ECS Fargate**, utilizando também ALB, ECR e CloudWatch.

Este repositório contém todo o backend do sistema, incluindo a arquitetura do projeto, os serviços, os modelos, o roteamento e o pipeline de deploy.

---

# 📂 **Estrutura do Projeto**

A estrutura do código segue uma organização clara e modular, focada em separação de responsabilidades:

```
.
├── .github/workflows/
│   └── deploy-ecr.yml       # Pipeline CI/CD para build e deploy automático na AWS
│
├── app/
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py       # Schemas Pydantic para validar entrada e saída da API
│   │
│   ├── routers/
│   │   ├── __init__.py
│   │   └── chat.py          # Router contendo o endpoint /chat/
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── llm_client.py    # Cliente do modelo FLAN-T5 + lógica de geração
│   │   └── config.py        # Configurações e variáveis de ambiente
│   │
│   ├── __init__.py
│
├── .env                     # Variáveis de ambiente locais (não sobe para produção)
├── Dockerfile               # Build da aplicação com Python + dependências
├── ecs-task.json            # Definição da Task do ECS (imagem, env vars, CPU/RAM, logs)
├── main.py                  # Arquivo principal da API (app FastAPI + health check)
├── requirements.txt         # Dependências Python
└── .gitignore
```

---

# ⚙️ **Tecnologias Utilizadas**

| Área         | Tecnologia                                      |
| ------------ | ----------------------------------------------- |
| Backend      | FastAPI, Python 3.11                            |
| LLM          | FLAN-T5 Small (HuggingFace/Transformers)        |
| Infra        | Docker, AWS ECS Fargate, AWS ECR                |
| Rede         | Application Load Balancer, Security Groups, VPC |
| Logs         | AWS CloudWatch                                  |
| CI/CD        | GitHub Actions                                  |
| Configuração | dotenv, Pydantic, loguru                        |

---

# 🧠 **Modelo de Linguagem – FLAN-T5 Small**

O modelo utilizado é:

```
google/flan-t5-small
```

### Motivos da escolha:

* Baixo consumo de memória
* Rodar 100% em CPU
* Reduz drasticamente erros 502/504 no ECS
* Ótimo desempenho para tarefas text-to-text
* Rápido e estável em execução serverless

---

# 🚀 **Como Executar Localmente**

### 1️⃣ Instale as dependências:

```bash
pip install -r requirements.txt
```

### 2️⃣ Configure seu `.env`

```
MODEL_NAME=google/flan-t5-small
MAX_NEW_TOKENS=128
TEMPERATURE=0.7
TOP_P=0.9
HF_TOKEN=opcional
```

### 3️⃣ Execute a API:

```bash
uvicorn main:app --reload --port 8080
```

### 4️⃣ Acesse:

```
http://localhost:8080/docs
```

---

# 🐳 **Executando via Docker**

### Build:

```bash
docker build -t iscoolgpt .
```

### Run:

```bash
docker run -p 8080:8080 iscoolgpt
```

---

# 📡 **Endpoints Principais**

## 🟢 **GET /health**

Retorna status da API e nome do modelo carregado.

Resposta:

```json
{
  "status": "ok",
  "model": "google/flan-t5-small"
}
```

---

## 🟣 **POST /chat/**

Recebe uma pergunta e retorna a resposta gerada pelo LLM.

Exemplo:

```json
{
  "question": "What is AWS EC2?"
}
```

Resposta:

```json
{
  "answer": "Amazon EC2 is a cloud service that provides virtual machines...",
  "model": "google/flan-t5-small"
}
```

---

# 🧩 **Explicação dos Principais Arquivos**

---

## 📌 `main.py`

* Inicializa a aplicação FastAPI.
* Registra o router `/chat`.
* Configura o endpoint `/health`.

---

## 📌 `app/models/schemas.py`

Define os formatos de entrada e saída usando **Pydantic**:

* `ChatRequest`
* `ChatResponse`

Garantindo validação automática no Swagger.

---

## 📌 `app/routers/chat.py`

Contém:

* O endpoint `/chat/`
* Chamada ao LLM via `llm_client`

---

## 📌 `app/services/config.py`

Centraliza:

* Variáveis de ambiente
* Configurações do modelo
* Parâmetros de geração

Ótimo para uso no ECS.

---

## 📌 `app/services/llm_client.py`

É o coração do sistema.

Funções:

* Carrega o modelo FLAN-T5, com cache (`@lru_cache`)
* Monta o prompt
* Gera texto com o pipeline Transformers
* Retorna a resposta já tratada

---

## 📌 `Dockerfile`

Cria a imagem Python slim com:

* Dependências do projeto
* Instalação do PyTorch CPU
* Uvicorn como servidor

---

## 📌 `ecs-task.json`

Arquivo usado pelo ECS contendo:

* Nome da imagem do ECR
* CPU/memória alocadas
* Variáveis de ambiente da aplicação
* Configuração do log driver
* Mapeamento de porta
* Nome do container

---

## 📌 `.github/workflows/deploy-ecr.yml`

Pipeline automático:

1. Build da imagem
2. Push para o ECR
3. Renderização da Task Definition
4. Deploy no ECS Fargate

---

# ☁️ **Arquitetura de Deploy na AWS**

A API está hospedada em:

### **AWS ECS Fargate**

Execução 100% serverless do container.

### **AWS ECR**

Repositório das imagens Docker.

### **Application Load Balancer**

Distribui tráfego HTTP para as tasks.

### **Target Group com health check**

Usa `/health`.

### **AWS CloudWatch Logs**

Armazena logs do backend.

### **VPC**

Sub-redes privadas + security groups.

---

# 🔄 **Fluxo CI/CD**

1. Dev faz push na `main`
2. GitHub Actions dispara workflow
3. Build da imagem Docker
4. Push para o ECR
5. Renderização da Task ECS com a nova imagem
6. ECS faz rolling update automaticamente

Nenhuma ação manual é necessária após configurar.

---

# 🧭 **Possível Evolução**

* Criar interface web (HTML/JS)
* Hospedar no **S3 + CloudFront**
* Consumir API /chat/ pelo frontend
* Adicionar autenticação JWT
* Histórico de chat e contexto persistente
* Adicionar embeddings para melhorar respostas

---
