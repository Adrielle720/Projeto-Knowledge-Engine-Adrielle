import pandas as pd
import json
import unicodedata
import re
import os

# ─────────────────────────────────────────────
# CONFIGURAÇÃO
# ─────────────────────────────────────────────
MOVIES_CSV = "tmdb_5000_movies.csv"
OUTPUT_PL  = "filmes.pl"

# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────

def normalizar(texto: str) -> str:
    """Converte texto para formato válido em Prolog (átomo)."""
    if not isinstance(texto, str) or texto.strip() == "":
        return "desconhecido"
    texto = unicodedata.normalize("NFKD", texto)
    texto = "".join(c for c in texto if not unicodedata.combining(c))
    texto = texto.lower()
    texto = re.sub(r"[\s\-]+", "_", texto)
    texto = re.sub(r"[^a-z0-9_]", "", texto)
    if texto and texto[0].isdigit():
        texto = "f_" + texto
    return texto or "desconhecido"


def primeiro_genero(genres_json: str) -> str:
    """Extrai o primeiro gênero da coluna JSON de gêneros."""
    try:
        genres = json.loads(genres_json)
        if genres:
            return normalizar(genres[0]["name"])
    except Exception:
        pass
    return "desconhecido"


def extrair_ano(release_date: str) -> int:
    """Extrai o ano da data de lançamento (formato YYYY-MM-DD)."""
    try:
        return int(str(release_date)[:4])
    except Exception:
        return 0


def formatar_numero(valor) -> int:
    """Converte para inteiro, retorna 0 se inválido."""
    try:
        v = int(float(valor))
        return v if v >= 0 else 0
    except Exception:
        return 0


def formatar_nota(valor) -> float:
    """Formata nota como float com 1 casa decimal."""
    try:
        return round(float(valor), 1)
    except Exception:
        return 0.0


def formatar_duracao(valor) -> int:
    try:
        v = int(float(valor))
        return v if v > 0 else 0
    except Exception:
        return 0


def normalizar_idioma(lang: str) -> str:
    mapa = {
        "en": "ingles",
        "fr": "frances",
        "de": "alemao",
        "es": "espanhol",
        "it": "italiano",
        "ja": "japones",
        "zh": "chines",
        "ko": "coreano",
        "pt": "portugues",
        "ru": "russo",
        "hi": "hindi",
        "ar": "arabe",
    }
    return mapa.get(str(lang).lower(), normalizar(str(lang)))


# ─────────────────────────────────────────────
# LEITURA DO CSV
# ─────────────────────────────────────────────

print("Lendo arquivo CSV...")

if not os.path.exists(MOVIES_CSV):
    raise FileNotFoundError(f"Arquivo não encontrado: {MOVIES_CSV}")

df = pd.read_csv(MOVIES_CSV)
print(f"{len(df)} filmes carregados.")

# ─────────────────────────────────────────────
# GERAÇÃO DOS PREDICADOS
# ─────────────────────────────────────────────

# Formato: filme(titulo, genero, ano, duracao_min, nota, bilheteria, orcamento, idioma).

predicados = []
ignorados  = 0

for _, row in df.iterrows():
    titulo     = normalizar(str(row.get("title", "")))
    genero     = primeiro_genero(str(row.get("genres", "[]")))
    ano        = extrair_ano(row.get("release_date", ""))
    duracao    = formatar_duracao(row.get("runtime", 0))
    nota       = formatar_nota(row.get("vote_average", 0))
    bilheteria = formatar_numero(row.get("revenue", 0))
    orcamento  = formatar_numero(row.get("budget", 0))
    idioma     = normalizar_idioma(row.get("original_language", ""))

    if titulo == "desconhecido" or ano == 0:
        ignorados += 1
        continue

    predicado = (
        f"filme({titulo}, {genero}, {ano}, {duracao}, "
        f"{nota}, {bilheteria}, {orcamento}, {idioma})."
    )
    predicados.append(predicado)

# ─────────────────────────────────────────────
# ESCRITA DO ARQUIVO .pl
# ─────────────────────────────────────────────

with open(OUTPUT_PL, "w", encoding="utf-8") as f:
    f.write("% filme(titulo, genero, ano, duracao_min, nota, bilheteria, orcamento, idioma).\n\n")
    for p in predicados:
        f.write(p + "\n")

print(f"Base gerada: {OUTPUT_PL}")
print(f"{len(predicados)} predicados escritos | {ignorados} registros ignorados")