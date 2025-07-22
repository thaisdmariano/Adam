import json
import random
import glob
import unicodedata
from pathlib import Path

import streamlit as st

# ----------------------------
# Página
# ----------------------------
st.set_page_config(page_title="🤖 Chatbot Cósmico", page_icon="✨")
st.title("🤖 Chatbot Cósmico")

# ----------------------------
# Helpers
# ----------------------------
def normalize_str(s: str) -> str:
    """Remove acentos, lowercase e normaliza espaços."""
    nf = unicodedata.normalize("NFKD", s)
    ascii_only = nf.encode("ASCII", "ignore").decode()
    return " ".join(ascii_only.lower().split())

def load_phrases() -> dict[str, list[str]]:
    """
    Procura por JSONs de frases:
      - na pasta ./frases/*.json
      - no diretório raiz como frases_<alguma_coisa>.json
    """
    paths = glob.glob("frases/*.json") + glob.glob("frases_*.json")
    db: dict[str, list[str]] = {}
    for p in paths:
        stem = Path(p).stem
        # remove prefixo 'frases_'
        if stem.startswith("frases_"):
            stem = stem[len("frases_"):]
        raw_key = stem.replace("_", " ")
        key_norm = normalize_str(raw_key)
        with open(p, encoding="utf-8") as f:
            data = json.load(f)
        # compacta estruturas em lista simples
        if isinstance(data, list):
            phrases = data
        elif isinstance(data, dict):
            if "frases" in data and isinstance(data["frases"], list):
                phrases = data["frases"]
            else:
                phrases = []
                for sub in data.values():
                    if isinstance(sub, list):
                        phrases.extend(sub)
        else:
            phrases = []
        db[key_norm] = phrases
    return db

entities = load_phrases()

# DEBUG: lista de keys carregadas
st.sidebar.markdown("**Entidades carregadas:**")
for k in sorted(entities.keys()):
    st.sidebar.write("-", k)

# ----------------------------
# Hierarquia de seleção
# ----------------------------
top_categories = [
    "Inomináveis",
    "Titãs",
    "Deuses",
    "Criaturas",
    "Anjos",
    "Demônios",
    "Humanos",
]

sub_map = {
    "Titãs": ["Benevolentes", "Malevolentes"],
    "Deuses": ["Nobre", "Opressor"],
    "Humanos": ["Raro", "Comum"],
}

singular = {
    "Inomináveis": "Inomináveis",
    "Titãs": "Titãs",
    "Deuses": "Deus",
    "Criaturas": "Criatura",
    "Anjos": "Anjo",
    "Demônios": "Demônio",
    "Humanos": "Humano",
}

# ----------------------------
# Narrativas de “Quem é você?”
# ----------------------------
descriptions = {
    "Inomináveis": {
        "texto": (
            "Eu sou o Inominável, aquele que existe acima de todas as manifestações do universo. "
            "Sou um ser Antigo, de forma Indistinguível, do tipo Energia. "
            "Minha hierarquia é Elevada e pertenço ao plano Cósmico. "
            "Tenho tamanho Colossal e minha idade é Incontável. "
            "Meu gênero é Indistinguível. Minha influência: Manifestação."
        )
    },
    "Titãs Benevolentes": {
        "texto": (
            "Eu sou um Titã Benevolente, dedicado à criação e proteção. "
            "Sou de forma Natural, do tipo Matéria. "
            "Minha hierarquia é Imperial e pertenço ao plano Planetário. "
            "Tenho o tamanho de um Gigante e a idade de 13 bilhões de anos. "
            "Meu gênero pode ser Feminino, Masculino ou Não binário. "
            "Minha influência é Criação. "
            "Sou Dedicado, Apoiador, Inspirador, Protetor, Supremo, e Inteligível."
        )
    },
    "Titãs Malevolentes": {
        "texto": (
            "Eu sou um Titã Malevolente, cuja força molda a fraqueza para alimentar a submissão. "
            "Sou de forma Natural, do tipo Matéria. "
            "Minha hierarquia é Imperial e pertenço ao plano Planetário. "
            "Tenho o tamanho de um Gigante e a idade de 13 bilhões de anos. "
            "Meu gênero pode ser Feminino, Masculino ou Não binário. "
            "Minha influência é Criação. "
            "Sou Relapso, Egóico, Manipulador, Insidioso, e acredito que ser planeta é ser estrela."
        )
    },
    "Deus Nobre": {
        "texto": (
            "Eu sou o Deus Nobre, aquele que governa com sabedoria e equilíbrio. "
            "Sou de forma Humanoide, do tipo Fragmentação. "
            "Minha hierarquia é Reinado e pertenço ao plano Local. "
            "Tenho o tamanho Maior e minha idade é de 4,8 bilhões de anos. "
            "Meu gênero pode ser Feminino, Masculino ou Não binário. "
            "Minha influência é Governança. "
            "Sou Amoral, Intelectual, Sensato, Sensível, Ético, Completo, Equilibrado e Perfeito."
        )
    },
    "Deus Opressor": {
        "texto": (
            "Eu sou o Deus Opressor, aquele que governa pela moral e a submissão. "
            "Sou de forma Humanoide, do tipo Fragmentação. "
            "Minha hierarquia é Reinado e pertenço ao plano Local. "
            "Tenho o tamanho Maior e minha idade é de 4,8 bilhões de anos. "
            "Meu gênero pode ser Feminino, Masculino ou Não binário. "
            "Minha influência é Governança. "
            "Sou Moralista, Emotivo, Insensato, Incompleto, Desequilibrado e Imperfeito."
        )
    },
    "Criatura": {
        "texto": (
            "Eu sou uma Criatura, nascida da matéria e da célula. "
            "Minha hierarquia é Subordinação e pertenço ao plano Local. "
            "Tenho o tamanho Médio e idade de até 1 milhão de anos. "
            "Meu gênero pode ser Feminino, Masculino ou Não binário. "
            "Minha influência é Tratamento."
        )
    },
    "Anjo": {
        "texto": (
            "Eu sou um Anjo, o mensageiro alado da operação celestial. "
            "Sou de forma Humanoide Alado, do tipo Molecular. "
            "Minha hierarquia é Subserviência e pertenço ao plano Celestial. "
            "Tenho o tamanho Menor e idade de até 10 mil anos. "
            "Meu gênero pode ser Feminino ou Masculino. "
            "Minha influência é Operação."
        )
    },
    "Demônio": {
        "texto": (
            "Eu sou um Demônio, aquele que te faz acreditar que se libertou do sistema, e te faz continuar a servi-lo. "
            "Sou de forma Animal Humanoide, do tipo Molecular. "
            "Minha hierarquia é Subserviência e pertenço ao plano Infernal. "
            "Tenho o tamanho Menor e idade indefinida. "
            "Meu gênero pode ser Feminino, Masculino ou Não binário. "
            "Minha influência é Agente."
        )
    },
    "Humano Raro": {
        "texto": (
            "Eu sou um Humano Raro, aquele que pensa, sente e constrói. "
            "Sou de forma Humana, do tipo Atômico. "
            "Minha hierarquia é Engrenagem e pertenço ao plano Terrestre. "
            "Tenho o tamanho Pequeno e idade média de até 190 anos. "
            "Meu gênero pode ser Feminino, Masculino ou Não binário. "
            "Minha influência é Construção."
        )
    },
    "Humano Comum": {
        "texto": (
            "Eu sou um Humano Comum, parte da engrenagem do mundo. "
            "Sou de forma Humana, do tipo Atômico. "
            "Minha hierarquia é Engrenagem e pertenço ao plano Terrestre. "
            "Tenho o tamanho Pequeno e idade média de até 190 anos. "
            "Meu gênero pode ser Feminino, Masculino ou Não binário. "
            "Minha influência é Servidão total sem jamais questionar."
        )
    },
}

# ----------------------------
# UI: seleção de categoria/subcategoria
# ----------------------------
cat = st.selectbox("Classe", top_categories)
if cat in sub_map:
    sub = st.selectbox("Subclasse", sub_map[cat])
    entity = f"{singular[cat]} {sub}"
else:
    entity = singular[cat]

# inicializa estado
if "last_resp" not in st.session_state:
    st.session_state.last_resp = ""
if "history" not in st.session_state:
    st.session_state.history = []

# ----------------------------
# Callbacks
# ----------------------------
def show_description():
    bloco = descriptions.get(entity)
    texto = bloco["texto"] if bloco else "Descrição não disponível."
    st.session_state.last_resp = texto
    st.session_state.history.append((entity, texto))

def new_phrase():
    key = normalize_str(entity)
    pool = entities.get(key, [])
    if not pool:
        texto = "Nenhuma frase disponível."
    else:
        vistos = [m for e, m in st.session_state.history if e == entity]
        candidatos = [f for f in pool if f not in vistos]
        texto = random.choice(candidatos) if candidatos else random.choice(pool)
    st.session_state.last_resp = texto
    st.session_state.history.append((entity, texto))

# ----------------------------
# Botões
# ----------------------------
c1, c2 = st.columns(2)
with c1:
    st.button("Quem é você?", on_click=show_description)
with c2:
    st.button("Nova Frase", on_click=new_phrase)

st.markdown("---")

# exibe só a última resposta (sem rolar)
if st.session_state.last_resp:
    st.markdown(f"### 💬 {st.session_state.last_resp}")