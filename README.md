# Anonimizador Keeggo

Aplicação Streamlit para anonimização de nomes pessoais em transcrições (ex.: chats ou reuniões Teams).  
Processamento 100% local — ideal para uso interno quando dados não podem sair da sua rede.

---

## 🚀 Quick Start (3 maneiras de rodar)

Escolha uma das opções abaixo:

### 1️⃣ **Modo Automático (Recomendado para primeiro uso)**

O script `setup.sh` (ou `setup.bat` no Windows) configura tudo automaticamente.

**Linux / macOS:**
```bash
git clone <URL_DO_REPO> anonimizador
cd anonimizador
chmod +x setup.sh
./setup.sh
```

**Windows:**
```cmd
git clone <URL_DO_REPO> anonimizador
cd anonimizador
setup.bat
```

Pronto! 🎉 O script vai:
- ✓ Verificar se Python 3 está instalado
- ✓ Criar um ambiente virtual (`.venv`)
- ✓ Instalar todas as dependências Python
- ✓ Baixar o modelo de linguagem spaCy
- ✓ Mostrar instruções de como iniciar

**Após o setup, rode:**
```bash
source .venv/bin/activate  # Linux/macOS
# ou
.venv\Scripts\activate.bat  # Windows

streamlit run anonimizador_streamlit.py
```

Abra `http://localhost:8501` no navegador.

---

### 2️⃣ **Modo Manual Local (Desenvolvimento)**

Se preferir fazer passo a passo (útil para desenvolvimento):

**Pré-requisitos:**
- Python 3.8+ (recomendado 3.11)
- pip

**Passos:**

```bash
# 1. Clonar repositório
git clone <URL_DO_REPO> anonimizador
cd anonimizador

# 2. Criar ambiente virtual
python -m venv .venv

# 3. Ativar ambiente virtual
# Linux/macOS:
source .venv/bin/activate
# Windows (PowerShell):
.\.venv\Scripts\Activate.ps1

# 4. Atualizar pip e instalar dependências
pip install --upgrade pip
pip install -r requirements.txt

# 5. Baixar modelo spaCy (primeira vez, leva alguns minutos)
python -m spacy download pt_core_news_lg

# 6. Rodar a aplicação
streamlit run anonimizador_streamlit.py
```

Acesse `http://localhost:8501` no navegador.

---

### 3️⃣ **Modo Container (Docker) - Produção**

Ideal para ambientes que precisam de portabilidade e sem dependências locais.

**Pré-requisitos:**
- Docker e Docker Compose instalados

**Opção A: Com Docker Compose (Recomendado)**

```bash
git clone <URL_DO_REPO> anonimizador
cd anonimizador

# Build e rodar
docker compose up --build

# Em outro terminal, verificar status
docker compose logs -f
```

Acesse `http://localhost:8501`.

**Opção B: Docker direto (sem compose)**

```bash
# Build
docker build -t anonimizador:latest .

# Rodar (desenvolvimento com volume local)
docker run --rm -p 8501:8501 -v "$PWD":/app anonimizador:latest

# Rodar (produção, sem volume)
docker run --rm -p 8501:8501 anonimizador:latest
```

**Rebuild após mudar dependências:**

Se você adicionar novos pacotes em `requirements.txt`:

```bash
docker compose build --no-cache
docker compose up
```

---

## 📋 O que é esta aplicação?

### Funcionalidades

- 🧠 **Detecção Inteligente**: Detecta nomes próprios com spaCy e regras simples (inclui nomes em diálogos como "João:")
- ✏️ **Entrada Manual**: Permite adicionar nomes que não foram detectados automaticamente
- 🏷️ **Anonimização**: Substitui nomes por tags padronizadas (ex: `<<PESSOA_1>>`) e gera um mapeamento
- 📊 **Exportação**: Baixa o texto anonimizado e o mapeamento em CSV
- 📁 **Múltiplos Formatos**: Aceita `.txt`, `.docx` (Word) e `.vtt` (WebVTT, padrão Teams)
- 💾 **Histórico Local**: Mantém histórico de transcrições processadas (sidebar)

### Arquivos principais

```
anonimizador/
├── anonimizador_streamlit.py    # Interface principal (Streamlit)
├── Dockerfile                    # Multi-stage para container
├── docker-compose.yml            # Orquestração Docker
├── requirements.txt              # Dependências Python
├── setup.sh / setup.bat          # Scripts de setup automático
├── .env.example                  # Template de variáveis
├── .gitignore                    # Git ignore (venv, cache, etc)
└── README.md                     # Este arquivo
```

---

## 📖 Como usar a aplicação

1. **Envie um arquivo ou cole a transcrição**
   - Aceita: `.txt`, `.docx` (Word), `.vtt` (WebVTT/Teams)
   - Ou cole diretamente na caixa de texto

2. **Revise os nomes detectados** (seção "2) Pessoas detectadas")
   - A aplicação detecta nomes automaticamente
   - Use o campo "Adicionar nomes manualmente" para incluir nomes perdidos
   - Separe por vírgula, ponto-e-vírgula ou nova linha
   - A pré-visualização mostra trechos para validação

3. **Selecione os nomes a anonimizar**
   - Por padrão, todos vêm selecionados
   - Desselecione se quiser manter algum nome

4. **Clique em "Anonimizar agora"**
   - Veja o texto original e anonimizado lado a lado
   - Visualize a tabela de mapeamento

5. **Baixe os resultados**
   - `anonimizado.txt` — texto com nomes substituídos
   - `mapeamento.csv` — correspondência entre tags e nomes originais

---

## 🐳 Detalhes do Docker (Multi-Stage)

O `Dockerfile` usa build multi-stage para imagem menor e mais segura:

- **Builder stage**: Compila as dependências Python em wheels
- **Final stage**: Instala apenas os wheels gerados + libs runtime mínimas

Vantagens:
- ✓ Imagem final menor (~50% menor)
- ✓ Sem ferramentas de build (mais seguro)
- ✓ Builds mais previsíveis

---

## ⚙️ Configuração (`.env`)

Copie `.env.example` para `.env` e customize conforme necessário:

```bash
cp .env.example .env
```

Variáveis disponíveis:
- `SPACY_MODEL` — Modelo spaCy a usar (padrão: `pt_core_news_lg`)
- `STREAMLIT_PORT` — Porta (padrão: `8501`)
- `STREAMLIT_SERVER_ADDRESS` — Endereço (padrão: `0.0.0.0`)
- `HISTORY_DIR` — Diretório de histórico (padrão: `historico`)

---

## 🧪 Testando diferentes formatos

### Arquivo `.vtt` (WebVTT/Teams)

O parser do app remove timestamps e mantém apenas as falas. Exemplo:

```
WEBVTT

00:00:00.000 --> 00:00:05.000
João: Olá, como você está?

00:00:05.000 --> 00:00:10.000
Maria: Tudo bem! E você?
```

Resultado após parse: `João: Olá, como você está?\nMaria: Tudo bem! E você?`

### Arquivo `.docx` (Word)

O parser extrai texto dos parágrafos. Se tiver tabelas com transcrições, abra uma issue para estendermos o parser.

### Arquivo `.txt` (Texto puro)

Funciona como esperado, sem processamento especial.

---

## 🔧 Resolução de Problemas

| Problema | Solução |
|----------|---------|
| **Script `setup.sh` não roda** | Execute `chmod +x setup.sh` para dar permissão de execução |
| **Erro no Windows ao rodar `setup.bat`** | Rode como administrador ou em PowerShell com privilégios |
| **Erro ao carregar modelo spaCy** | Execute `python -m spacy download pt_core_news_lg` manualmente |
| **Porta 8501 já está em uso** | Mude a porta: `streamlit run anonimizador_streamlit.py --server.port=8502` |
| **Streamlit não inicia** | Verifique se o `.venv` está ativado e a porta está livre |
| **Erro ao processar `.docx`** | Instale `python-docx`: `pip install python-docx` |
| **Docker não consegue fazer build** | Rode `docker compose build --no-cache` para limpeza completa |

---

## 🔐 Privacidade e Segurança

- ✓ Processamento 100% local — nenhum dado é enviado para a nuvem
- ✓ Arquivos processados ficam no histórico local (pasta `historico/`)
- ✓ Use em ambientes seguros se trabalhar com dados sensíveis
- ⚠️ Revise sempre o mapeamento de nomes antes de compartilhar

---

## 📦 Dependências

**Python packages** (em `requirements.txt`):
- `streamlit>=1.0` — Interface web
- `spacy>=3.5` — Detecção de entidades (NLP)
- `pandas` — Manipulação de dados
- `python-docx>=0.8.11` — Leitura de `.docx`

**System libraries** (no Dockerfile):
- `libxml2`, `libxslt1`, `zlib1g` — Para lxml (python-docx)
- `libffi`, `libssl` — Para pacotes binários

---

## 🤝 Contribuição

Encontrou um bug ou tem uma sugestão?

1. Abra uma **issue** descrevendo o problema/sugestão
2. Envie um **pull request** com a solução
3. Antes de submeter, certifique-se que tudo funciona:
   ```bash
   streamlit run anonimizador_streamlit.py
   # Teste a anonimização com alguns exemplos
   ```

---

## 📄 Licença

Este projeto não inclui licença por padrão. Se for publicar, adicione um arquivo `LICENSE` (ex.: MIT, GPL, etc).

---

## 👤 Contato

Desenvolvido por **Yasmin Lopes** — Cloud & DevOps  
Keeggo © 2025

Para dúvidas ou sugestões, abra uma issue no repositório.

---

**Pronto para usar! Boa anonimização! 🎉**

