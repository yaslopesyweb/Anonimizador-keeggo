# Anonimizador

Aplicação Streamlit para anonimização de nomes pessoais em transcrições (ex.: chats ou reuniões Teams).
Processamento 100% local — ideal para uso interno quando dados não podem sair da sua rede.

Principais arquivos
- `anonimizador_streamlit.py` — interface principal (Streamlit).
- `anonimizador_interativo.py` / `anonimizador_interativo2.py` — scripts auxiliares/alternativos.
- `anonimizar_transcricao.py` — funções de anonimização reutilizáveis.
- `requirements.txt` — dependências Python.
- `Dockerfile`, `docker-compose.yml` — para rodar em container.

Funcionalidades
- Detecta nomes próprios com spaCy e regras simples (inclui nomes em diálogos como "João:").
- Permite adicionar nomes manualmente (casos que o modelo não detectou).
- Substitui nomes por tags padronizadas (ex.: `<<PESSOA_1>>`) e gera um mapeamento.
- Permite baixar o texto anonimizado e o mapeamento em CSV.

Pré-requisitos
- Python 3.8+ (recomendado 3.11)
- pip
- (Opcional) Docker e Docker Compose para rodar em container

Instalação e execução local (recomendado para desenvolvimento)

1. Clonar o repositório (ou copiar os arquivos para uma pasta local):

```bash
git clone <URL_DO_REPO> anonimizador
cd anonimizador
```

2. Criar e ativar um ambiente virtual (recomendado):

Linux / macOS:
```bash
python -m venv .venv
source .venv/bin/activate
```

Windows (PowerShell):
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3. Instalar dependências:

```bash
pip install --upgrade pip
pip install -r requirements.txt
# Se necessário, baixe o modelo spaCy (pode levar alguns minutos):
python -m spacy download pt_core_news_lg
```

4. Rodar a aplicação:

```bash
streamlit run anonimizador_streamlit.py
```

Acesse `http://localhost:8501` no navegador.

Rodando com Docker (recomendado para produção ou para evitar instalar dependências locais)

1. Build e run com Docker Compose:

```bash
docker compose up --build
```

2. Ou com Docker diretamente:

```bash
docker build -t anonimizador:latest .
docker run --rm -p 8501:8501 -v "$PWD":/app anonimizador:latest
```

Observações sobre Docker
- O `Dockerfile` baixa o modelo spaCy durante a build; a imagem resultante pode ser grande.
- O `docker-compose.yml` monta o diretório do projeto dentro do container por conveniência de desenvolvimento.

Como usar a aplicação (passo a passo)
1. Envie ou cole a transcrição (arquivo `.txt` ou cole na área de texto).
2. A aplicação detecta automaticamente nomes com spaCy. Na seção "Pessoas detectadas":
	- Você verá os nomes detectados.
	- Use o campo "Adicionar nomes manualmente" para incluir nomes que não foram detectados automaticamente (separe por vírgula, ponto-e-vírgula ou nova linha).
	- Selecione os nomes que deseja anonimizar (por padrão, todos já vêm selecionados).
	- A pré-visualização mostra trechos com as ocorrências encontradas para validação.
3. Clique em "Anonimizar agora".
4. Você poderá visualizar o texto original e o anonimizado lado a lado, além de baixar:
	- Texto anonimizado (`anonimizado.txt`)
	- Mapeamento de tags para nomes originais (`mapeamento.csv`)

Boas práticas
- Não adicione seu ambiente virtual (`venv/` ou `.venv/`) ao repositório — o `.gitignore` já ignora essas pastas.
- Se for publicar no GitHub, crie um `requirements.txt` atualizado e um `LICENSE` adequado.

Privacidade e segurança
- A ferramenta foi desenhada para processamento local. Não envie dados sensíveis para serviços externos sem revisão legal.

Resolução de problemas
- Erro ao carregar o modelo spaCy: execute `python -m spacy download pt_core_news_lg` e reinicie.
- Streamlit não inicia: verifique se a porta `8501` está livre e se o ambiente virtual está ativado.

Contribuição
- Abra uma issue explicando o que gostaria de mudar ou envie um pull request.


Contato
- Desenvolvido por Yasmin Lopes 

