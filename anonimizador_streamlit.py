# anonimizador_streamlit.py
# Streamlit local web app for anonymizing PERSON names in Teams transcripts
# Run: streamlit run anonimizador_streamlit.py

import os
import streamlit as st
import spacy
from collections import OrderedDict
import pandas as pd
from io import StringIO
import csv
import base64
import unicodedata
import re
import base64

# ---------------------------------------------------------
# CONFIG DA PÁGINA + FAVICON LOCAL
# ---------------------------------------------------------
st.set_page_config(
    page_title="Anonimizador Local",
    page_icon="Isotipos.png",
    layout="wide"
)
def load_image_as_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

logo_header_base64 = load_image_as_base64("logokeeggo_brancoeverde.png")

st.markdown(f"""
    <style>

    /* Aumenta a barra superior e ajusta fundo */
    header[data-testid="stHeader"] {{
        background-color: #0A0A0A;
        height: 70px;
    }}

    /* Remove padding lateral que afasta a logo */
    header[data-testid="stHeader"] > div:first-child {{
        padding-left: 15px;
    }}

    /* Insere a logo */
    header[data-testid="stHeader"]::before {{
        content: "";
        position: absolute;
        top: 10px;
        left: 70px;
        width: 160px;   /* ajuste o tamanho da logo aqui */
        height: 50px;
        background-image: url("data:image/png;base64,{logo_header_base64}");
        background-size: contain;
        background-repeat: no-repeat;
        background-position: left center;
    }}
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# CORES OFICIAIS KEEGGO (TEMA ESCURO)
# ---------------------------------------------------------
primary_light = "#22B2A7"
primary_dark = "#028981"
aqua = "#2FEBDE"
graphite = "#202020"
light_gray = "#E6E6E6"
white = "#FFFFFF"

# caminhos das imagens (devem estar na mesma pasta)
logo_path = "logokeeggo_brancoeverde.png"
isotipo_path = "Isotipos.png"

# fallback: use uploaded file path available no ambiente (imagem enviada na sessão)
# developer provided path (local no container). Ajuste se quiser usar este arquivo como logo:
fallback_uploaded_logo = "/mnt/data/5e6c247b-e704-45b6-8d72-e27c664b2476.png"

def load_image_as_base64(path):
    try:
        with open(path, "rb") as img:
            return base64.b64encode(img.read()).decode()
    except Exception:
        return None

# ---------- Carrega a logo em base64 (agora definido antes do uso) ----------
logo_base64 = load_image_as_base64(logo_path)

# se arquivo principal não existir, tenta isotipo_path
if not logo_base64:
    logo_base64 = load_image_as_base64(isotipo_path)

# se ainda não existir, tenta o fallback (se existir no ambiente)
if not logo_base64 and os.path.exists(fallback_uploaded_logo):
    logo_base64 = load_image_as_base64(fallback_uploaded_logo)

# ---------------------------------------------------------
# INJETAR CSS TEMA ESCURO + HEADER COM LOGO FIXA DENTRO DO HEADER DO STREAMLIT
# ---------------------------------------------------------
st.markdown(
    f"""
    <style>
        .stApp {{
            background-color: {graphite};
            color: {light_gray};
        }}
        .block-container {{
            background-color: {graphite};
            padding-top: 110px !important; /* espaço para o header fixo */
        }}
        h1, h2, h3, h4, h5, h6, label, p {{
            color: {light_gray} !important;
        }}
        section[data-testid="stSidebar"] {{
            background-color: #111111;
        }}
        section[data-testid="stSidebar"] * {{
            color: {light_gray} !important;
        }}
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
        textarea, .stTextArea>div>div>textarea {{
            background-color: #1A1A1A !important;
            color: {white} !important;
        }}
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
        [data-testid="stHeader"] {{
            background-color: #0E1117 !important;
            height: 70px;
        }}

        /* LOGO posicionada dentro do header */
        .custom-header-logo {{
            position: fixed;
            left: 20px;
            top: 15px;
            height: 45px;
            z-index: 9999;
        }}

    </style>
    """,
    unsafe_allow_html=True
)

# Inserir a tag <img> somente se logo_base64 existir para evitar NameError ou HTML vazio
if logo_base64:
    st.markdown(
        f'<img src="data:image/png;base64,{logo_base64}" class="custom-header-logo">',
        unsafe_allow_html=True
    )
else:
    # fallback visual: usar st.image para não falhar (não fica no header oficial, mas evita erro)
    if os.path.exists(logo_path):
        st.image(logo_path, width=160)
    elif os.path.exists(isotipo_path):
        st.image(isotipo_path, width=160)
    elif os.path.exists(fallback_uploaded_logo):
        st.image(fallback_uploaded_logo, width=160)
    else:
        # opcional: log para ajudar debug
        st.write("")  # nada visível

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
# SIDEBAR
# ---------------------------------------------------------
st.sidebar.header("Configurações")
model_name = st.sidebar.text_input("Modelo spaCy", value="pt_core_news_lg")
show_debug = st.sidebar.checkbox("Mostrar debug", value=False)

nlp = load_model(model_name)

# ---------------------------------------------------------
# INPUT
# ---------------------------------------------------------
st.header("1) Envie ou cole a transcrição")
uploaded = st.file_uploader("Arquivo .txt", type=["txt"])

if uploaded:
    input_text = uploaded.read().decode("utf-8", errors="ignore")
else:
    input_text = st.text_area("Ou cole aqui:", height=250)

if not input_text:
    st.stop()

# ---------------------------------------------------------
# DETECTAR NOMES
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
            preview.append("..." + ctx.replace("\n", " ") + "...")
        st.code("\n\n".join(preview))

# ---------------------------------------------------------
# ANONIMIZAR
# ---------------------------------------------------------
st.header("3) Anonimizar")

if st.button("Anonimizar agora"):
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
