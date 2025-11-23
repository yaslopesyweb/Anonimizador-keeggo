# anonimizador_streamlit_final.py
# Versão final com histórico no sidebar (arquivo separado)
# Run: streamlit run anonimizador_streamlit_final.py

import os
import streamlit as st
import spacy
from collections import OrderedDict
import pandas as pd
import base64
import unicodedata
import re
from datetime import datetime

# -------------------------
# HISTÓRICO LOCAL
# -------------------------
HIST_DIR = "historico"
os.makedirs(HIST_DIR, exist_ok=True)

# ---------------------------------------------------------
# CONFIG DA PÁGINA + FAVICON LOCAL
# ---------------------------------------------------------
st.set_page_config(
    page_title="Anonimizador Local",
    page_icon="Isotipos.png",
    layout="wide"
)

# ---------------------------------------------------------
# Função utilitária para carregar imagem em base64
# ---------------------------------------------------------
def load_image_as_base64(path):
    try:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except Exception:
        return None

# tenta carregar logo que você enviou
logo_header_base64 = load_image_as_base64("logokeeggo_brancoeverde.png")
fallback_uploaded_logo = "/mnt/data/5e6c247b-e704-45b6-8d72-e27c664b2476.png"
if not logo_header_base64 and os.path.exists(fallback_uploaded_logo):
    logo_header_base64 = load_image_as_base64(fallback_uploaded_logo)

# ---------------------------------------------------------
# CORES OFICIAIS KEEGGO (TEMA ESCURO)
# ---------------------------------------------------------
primary_light = "#22B2A7"
primary_dark = "#028981"
aqua = "#2FEBDE"
graphite = "#202020"
light_gray = "#E6E6E6"
white = "#FFFFFF"

# ---------------------------------------------------------
# INJETAR CSS TEMA ESCURO + HEADER COM LOGO NO HEADER DO STREAMLIT
# + estilos para sidebar histórico e alertas
# ---------------------------------------------------------
st.markdown(
    f"""
    <style>
        /* APP */
        .stApp {{
            background-color: {graphite};
            color: {light_gray};
        }}
        .block-container {{
            background-color: {graphite};
            padding-top: 120px !important; /* espaço para o header fixo */
        }}
        h1, h2, h3, h4, h5, h6, label, p {{
            color: {light_gray} !important;
        }}

        /* SIDEBAR */
        section[data-testid="stSidebar"] {{
            background-color: #111111;
            color: {light_gray};
        }}
        section[data-testid="stSidebar"] .sidebar-content {{
            padding-top: 12px;
        }}

        /* Botões principais */
        .stButton>button {{
            background-color: {primary_dark} !important;
            color: white !important;
            border-radius: 6px;
            padding: 8px 18px;
            font-weight: 600;
        }}
        .stButton>button:hover {{
            background-color: {primary_light} !important;
            color: black !important;
        }}

        /* Textareas */
        textarea, .stTextArea>div>div>textarea {{
            background-color: #1A1A1A !important;
            color: {white} !important;
        }}

        /* Footer */
        .footer-keeggo {{
            text-align: center;
            color: {light_gray};
            margin-top: 24px;
            font-size: 13px;
        }}
        .credit-yasmin {{
            text-align: right;
            font-size: 12px;
            color: {aqua};
            margin-top: 10px;
        }}

        /* HEADER oficial do Streamlit */
        header[data-testid="stHeader"] {{
            background-color: #0E1117 !important;
            height: 70px;
        }}

        /* Insere a logo no header usando ::before (ajuste left para alinhar) */
        header[data-testid="stHeader"]::before {{
            content: "";
            position: absolute;
            top: 10px;
            left: 50px; /* movido um pouco para a direita para não colidir com o botão do sidebar */
            width: 160px;
            height: 50px;
            background-image: url("data:image/png;base64,{logo_header_base64 or ''}");
            background-size: contain;
            background-repeat: no-repeat;
            background-position: left center;
            z-index: 9999;
        }}

        /* ALERTA de sucesso customizado (Keeggo) */
        .stAlert {{
            border-radius: 6px !important;
            padding: 10px 14px !important;
            font-weight: 600 !important;
        }}
        .stAlert[data-testid="stStatusElement"] {{
            background-color: {primary_light} !important;
            color: #ffffff !important;
            border: 1px solid {primary_dark} !important;
        }}

        /* HISTÓRICO no SIDEBAR (estilo ChatGPT-like) */
        .sidebar-history-title {{
            color: {primary_light};
            font-size: 16px;
            font-weight: 700;
            margin-bottom: 10px;
            margin-left: 4px;
        }}
        .sidebar-history-container {{
            max-height: 420px;
            overflow-y: auto;
            padding-right: 6px;
            margin-top: 8px;
        }}

        /* Item do histórico: apenas emoji + nome, bolinha aparece só no hover */
        .sidebar-item {{
            display: flex;
            align-items: center;
            gap: 8px;
            padding: 8px 12px;
            background-color: #1A1A1A;
            border-radius: 10px;
            color: {light_gray};
            font-size: 14px;
            cursor: pointer;
            transition: 0.18s ease;
            border: 1px solid transparent;
        }}

        .sidebar-item:hover {{
            background-color: {primary_dark};
            border-color: {primary_light};
            color: white;
        }}

        .sidebar-item-emoji {{
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 28px;
            height: 28px;
            border-radius: 999px;
            background-color: transparent; /* fica transparente até hover */
            transition: 0.18s ease;
        }}

        .sidebar-item:hover .sidebar-item-emoji {{
            background-color: {primary_light}; /* bolinha verde claro aparece só no hover */
            color: {graphite};
        }}

        .sidebar-item .name {{
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }}

        /* scrollbar pequena no histórico */
        .sidebar-history-container::-webkit-scrollbar {{
            width: 8px;
        }}
        .sidebar-history-container::-webkit-scrollbar-thumb {{
            background-color: #2b2b2b;
            border-radius: 4px;
        }}
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------------------------------------------------
# Inserir a tag <img> no corpo (fallback caso header ::before não carregue a imagem)
# ---------------------------------------------------------
if not logo_header_base64:
    # tenta exibir de forma tradicional
    if os.path.exists("logokeeggo_brancoeverde.png"):
        st.image("logokeeggo_brancoeverde.png", width=160)
    elif os.path.exists("Isotipos.png"):
        st.image("Isotipos.png", width=160)

# ---------------------------------------------------------
# SIDEBAR: HISTÓRICO APENAS (sem configurações)
# ---------------------------------------------------------
st.sidebar.markdown("<div class='sidebar-history-title'>Histórico</div>", unsafe_allow_html=True)
st.sidebar.markdown("<div class='sidebar-history-container'>", unsafe_allow_html=True)

# lista arquivos no diretório (exibe mais recentes primeiro)
def list_history_files():
    files = []
    for f in os.listdir(HIST_DIR):
        path = os.path.join(HIST_DIR, f)
        if os.path.isfile(path):
            files.append((os.path.getmtime(path), f))
    files.sort(reverse=True)  # mais novos primeiro
    return [f for _, f in files]

hist_files = list_history_files()

# render items as clickable divs using query params
for filename in hist_files:
    safe_name = filename.replace("'", "\\'").replace('"', '\\"')
    button_html = f"""
        <div class="sidebar-item" onclick="window.location.href='/?history={safe_name}'">
            <div class="name">{filename}</div>
        </div>
    """
    st.sidebar.markdown(button_html, unsafe_allow_html=True)

st.sidebar.markdown("</div>", unsafe_allow_html=True)

# limpar histórico
if st.sidebar.button("Limpar histórico", key="clear_hist"):
    for f in os.listdir(HIST_DIR):
        try:
            os.remove(os.path.join(HIST_DIR, f))
        except Exception:
            pass
    st.rerun()

# ---------------------------------------------------------
# HEADER DO CONTEÚDO (TITULO)
# ---------------------------------------------------------
st.markdown(
    f"""
    <div style='margin-left: 220px; margin-top: -60px;'>
        <h1 style='color:{primary_light}; margin:0;'>Anonimizador Local</h1>
        <div style='color:{light_gray};'>Ferramenta interna para uso dos colaboradores Keeggo. Processamento 100% local.</div>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("---")

# ---------------------------------------------------------
# CARREGAR MODELO
# ---------------------------------------------------------
@st.cache_resource
def load_model(name="pt_core_news_lg"):
    try:
        return spacy.load(name)
    except Exception as e:
        st.error(f"Erro ao carregar modelo spaCy '{name}': {e}")
        st.stop()

# carrega modelo fixo (não exposto no sidebar)
nlp = load_model("pt_core_news_lg")


# ---------------------------------------------------------
# DETECÇÃO INTELIGENTE DE NOMES (NÃO PEGA PALAVRAS INDESEJADAS)
# ---------------------------------------------------------
def detect_persons(nlp, text):
    doc = nlp(text)
    spacy_names = [ent.text for ent in doc.ents if ent.label_.upper() in ("PER", "PERSON")]
    spacy_names = list(OrderedDict.fromkeys(spacy_names))
    fullnames = [n for n in spacy_names if len(n.split()) > 1]
    firstnames_spacy = [n for n in spacy_names if len(n.split()) == 1]
    dialog_name_regex = r"\b([A-ZÁÉÍÓÚÂÊÔÃÕ][a-záéíóúâêôãõç]+)(?=\s*:)"
    dialog_names = re.findall(dialog_name_regex, text)
    firstnames = list(OrderedDict.fromkeys(firstnames_spacy + dialog_names))
    final_names = OrderedDict()
    for fn in firstnames:
        matched = False
        for fullname in fullnames:
            if fn.lower() in fullname.lower().split():
                final_names[fullname] = True
                matched = True
                break
        if not matched:
            final_names[fn] = True
    for fn in fullnames:
        final_names[fn] = True
    people = list(final_names.keys())
    spans = []
    for p in people:
        for match in re.finditer(rf"\b{re.escape(p)}\b", text):
            spans.append((match.start(), match.end(), p))
    return people, spans

def normalize_name(name):
    name = "".join(
        c for c in unicodedata.normalize("NFD", name)
        if unicodedata.category(c) != "Mn"
    )
    name = name.lower().strip()
    name = re.sub(r"\b(da|de|do|das|dos|e)\b", " ", name)
    name = re.sub(r"\s+", " ", name).strip()
    return name

# ---------------------------------------------------------
# ANONIMIZADOR – EVITA REPETIÇÕES
# ---------------------------------------------------------
def anonymize_by_names(text, selected_names):
    canonical = {}
    tag_counter = 1
    occurrences = []
    selected_sorted = sorted(selected_names, key=lambda x: len(x), reverse=True)
    for name in selected_sorted:
        start = 0
        while True:
            idx = text.find(name, start)
            if idx == -1:
                break
            occurrences.append((idx, idx + len(name), name))
            start = idx + len(name)
    occurrences.sort(key=lambda x: x[0])
    result = text
    for s, e, name in reversed(occurrences):
        canon = normalize_name(name)
        if canon not in canonical:
            canonical[canon] = f"<<PESSOA_{tag_counter}>>"
            tag_counter += 1
        tag = canonical[canon]
        result = result[:s] + tag + result[e:]
    mapping = []
    for canon, tag in canonical.items():
        for name in selected_sorted:
            if normalize_name(name) == canon:
                mapping.append((tag, name))
                break
    return result, mapping

# ---------------------------------------------------------
# INPUT
# ---------------------------------------------------------
st.header("1) Envie ou cole a transcrição")
uploaded = st.file_uploader("Arquivo .txt", type=["txt"])

# Carregar via query params (clicou no histórico)
params = st.query_params
input_text = ""

if "history" in params:
    hist_file = params["history"]
    # streamlit pode retornar lista ou string
    if isinstance(hist_file, list):
        hist_file = hist_file[0]

    hist_path = os.path.join(HIST_DIR, hist_file)
    if os.path.exists(hist_path):
        with open(hist_path, "r", encoding="utf-8") as h:
            input_text = h.read()
        st.success(f"Histórico carregado: {hist_file}")


# Se não veio via histórico, verificar upload ou textarea
if not input_text:
    if uploaded:
        input_text = uploaded.read().decode("utf-8", errors="ignore")
    else:
        input_text = st.text_area("Ou cole aqui:", height=250)

# Se não houver texto -> parar antes de detectar nomes
if not input_text or not input_text.strip():
    st.stop()

# ---------------------------------------------------------
# DETECTAR NOMES (após garantir que input_text existe)
# ---------------------------------------------------------
unique_persons, spans = detect_persons(nlp, input_text)

st.header("2) Pessoas detectadas")
col1, col2 = st.columns([2, 3])

with col1:
    selected = st.multiselect(
        "Selecione os nomes a anonimizar",
        options=unique_persons,
        default=unique_persons
    )

with col2:
    st.subheader("Amostra")
    if spans:
        preview = []
        for s, e, txt in spans[:8]:
            ctx = input_text[max(0, s - 25):min(len(input_text), e + 25)]
            preview.append("..." + ctx.replace("\\n", " ") + "...")
        st.code("\\n\\n".join(preview))

# ---------------------------------------------------------
# ANONIMIZAR
# ---------------------------------------------------------
st.header("3) Anonimizar")

if st.button("Anonimizar agora"):
    # salva original no histórico with timestamp (ou usa nome do upload)
    if uploaded and hasattr(uploaded, "name"):
        filename = uploaded.name
    else:
        # se veio do histórico, tenta manter o mesmo nome; senão cria um com timestamp
        filename = f"transcricao_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

    save_path = os.path.join(HIST_DIR, filename)
    try:
        with open(save_path, "w", encoding="utf-8") as f:
            f.write(input_text)
    except Exception as e:
        st.error(f"Erro ao salvar no histórico: {e}")

    anon_text, mapping = anonymize_by_names(input_text, selected)

    st.success("Anonimização concluída!")

    left, right = st.columns(2)
    with left:
        st.subheader("Original")
        st.text_area("", input_text, height=300)
    with right:
        st.subheader("Anonimizado")
        st.text_area("", anon_text, height=300)

    df = pd.DataFrame(mapping, columns=["tag", "original"])
    st.subheader("Mapeamento")
    st.dataframe(df)
    st.download_button("Baixar texto anonimizado", anon_text.encode(), "anonimizado.txt")
    st.download_button("Baixar mapeamento", df.to_csv(index=False).encode(), "mapeamento.csv")

# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown('<div class="footer-keeggo">Ferramenta interna Keeggo. Nenhum dado é enviado à nuvem.</div>', unsafe_allow_html=True)
st.markdown('<div class="credit-yasmin">Desenvolvido por Yasmin Araujo Santos Lopes - Cloud & DevOps</div>', unsafe_allow_html=True)
