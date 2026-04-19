#!/usr/bin/env python3
"""
Baixa a Bíblia completa em português (Almeida Atualizada) de um repositório
público no GitHub e salva em cache local (biblia_cache.json).

Estrutura do JSON baixado:
[
  { "abbrev": "gn", "name": "Gênesis", "chapters": [["verso1", "verso2"], ...] },
  ...
]
"""

import json
import random
import urllib.request
from pathlib import Path
from datetime import date

# Temas predefinidos: cada chave é o nome do tema e o valor é a lista de
# palavras-chave buscadas simultaneamente (OR lógico).
TEMAS: dict[str, list[str]] = {
    "amor":          ["amor", "amar", "amou", "amará"],
    "fé":            ["fé", "fiel", "fidelidade", "crer", "crença", "crentes"],
    "esperança":     ["esperança", "esperar", "aguardar"],
    "paz":           ["paz", "pacífico", "pacificador"],
    "alegria":       ["alegria", "alegre", "regozijar", "regozijo", "júbilo"],
    "tristeza":      ["tristeza", "triste", "chorar", "choro", "lamentação", "pranto"],
    "obediência":    ["obedecer", "obediente", "obediência", "obedeceu", "obedeceis"],
    "graça":         ["graça", "gracioso", "misericórdia"],
    "perdão":        ["perdão", "perdoar", "perdoa", "perdoado"],
    "sabedoria":     ["sabedoria", "sábio", "entendimento", "discernimento"],
    "força":         ["força", "forte", "fortalecer", "poderoso"],
    "cura":          ["cura", "curar", "sarar", "saúde", "sãos"],
    "oração":        ["oração", "orar", "orai", "rogai", "suplicar"],
    "salvação":      ["salvação", "salvo", "salvar", "redenção", "redentor"],
    "vida":          ["vida eterna", "vida abundante"],
    "ressurreição":  ["ressurreição", "ressuscitar", "ressuscitou"],
    "gratidão":      ["gratidão", "grato", "agradecer", "graças"],
    "humildade":     ["humildade", "humilde", "humilhar"],
}

URL_BIBLIA = "https://raw.githubusercontent.com/thiagobodruk/biblia/master/json/aa.json"
CACHE = Path(__file__).parent / "biblia_cache.json"


def _baixar() -> list:
    print("Baixando Bíblia... (apenas na primeira vez)")
    with urllib.request.urlopen(URL_BIBLIA, timeout=10) as resp:
        dados = json.loads(resp.read().decode("utf-8-sig"))
    CACHE.write_text(json.dumps(dados, ensure_ascii=False), encoding="utf-8")
    return dados


def carregar() -> list:
    """Retorna a Bíblia completa. Usa cache se já baixou antes."""
    if CACHE.exists():
        return json.loads(CACHE.read_text(encoding="utf-8"))
    return _baixar()


def aleatorio(biblia: list) -> tuple[str, str]:
    """Sorteia um versículo aleatório de qualquer livro/capítulo."""
    livro = random.choice(biblia)
    cap_idx = random.randrange(len(livro["chapters"]))
    capitulo = livro["chapters"][cap_idx]
    ver_idx = random.randrange(len(capitulo))
    texto = capitulo[ver_idx]
    referencia = f"{livro['name']} {cap_idx + 1}:{ver_idx + 1}"
    return referencia, texto


def do_dia(biblia: list) -> tuple[str, str]:
    """Retorna o mesmo versículo durante todo o dia."""
    random.seed(date.today().toordinal())
    resultado = aleatorio(biblia)
    random.seed()
    return resultado


def buscar(biblia: list, termo: str) -> list[tuple[str, str]]:
    """Busca versículos que contenham o termo no texto ou no nome do livro."""
    termo = termo.lower()
    resultados = []
    for livro in biblia:
        for cap_idx, capitulo in enumerate(livro["chapters"]):
            for ver_idx, texto in enumerate(capitulo):
                if termo in texto.lower() or termo in livro["name"].lower():
                    ref = f"{livro['name']} {cap_idx + 1}:{ver_idx + 1}"
                    resultados.append((ref, texto))
    return resultados


def buscar_tema(biblia: list, tema: str) -> list[tuple[str, str]]:
    """Busca versículos por tema predefinido (OR entre as palavras-chave do tema)."""
    palavras = [p.lower() for p in TEMAS.get(tema, [])]
    if not palavras:
        return []
    vistos: set[str] = set()
    resultados = []
    for livro in biblia:
        for cap_idx, capitulo in enumerate(livro["chapters"]):
            for ver_idx, texto in enumerate(capitulo):
                texto_lower = texto.lower()
                if any(p in texto_lower for p in palavras):
                    ref = f"{livro['name']} {cap_idx + 1}:{ver_idx + 1}"
                    if ref not in vistos:
                        vistos.add(ref)
                        resultados.append((ref, texto))
    return resultados


def encontrar_indices(biblia: list, referencia: str):
    """Converte 'Livro cap:ver' em (book_idx, cap_idx, ver_idx) ou None."""
    try:
        partes = referencia.rsplit(" ", 1)
        livro_nome = partes[0]
        cap_str, ver_str = partes[1].split(":")
        cap_idx = int(cap_str) - 1
        ver_idx = int(ver_str) - 1
        for i, livro in enumerate(biblia):
            if livro["name"] == livro_nome:
                return i, cap_idx, ver_idx
    except Exception:
        pass
    return None
