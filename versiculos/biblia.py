#!/usr/bin/env python3
"""
Baixa a Bíblia completa em português (Almeida Atualizada) de um repositório
público no GitHub e salva em cache local (biblia_cache.json).

Estrutura do JSON baixado:
[
  { "abbrev": "gn", "book": "Gênesis", "chapters": [["verso1", "verso2"], ...] },
  ...
]
"""

import json
import random
import urllib.request
from pathlib import Path
from datetime import date

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
