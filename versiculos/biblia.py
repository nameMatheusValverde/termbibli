#!/usr/bin/env python3
"""
Baixa a Bíblia completa em português de um repositório público no GitHub
e salva em cache local. Suporta múltiplas versões (aa, acf, nvi).

Estrutura do JSON baixado:
[
  { "abbrev": "gn", "name": "Gênesis", "chapters": [["verso1", "verso2"], ...] },
  ...
]
"""

import json
import random
import re
import unicodedata
import urllib.error
import urllib.request
from pathlib import Path
from datetime import date

VERSOES: dict[str, str] = {
    "aa":  "Almeida Atualizada",
    "acf": "Almeida Corrigida Fiel",
    "nvi": "Nova Versão Internacional",
}

VERSAO_PADRAO = "aa"

_URL_BASE = "https://raw.githubusercontent.com/thiagobodruk/biblia/master/json/{versao}.json"
_DIR = Path(__file__).parent

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


def _cache_path(versao: str) -> Path:
    return _DIR / f"biblia_cache_{versao}.json"


def _normalizar(texto: str) -> str:
    """Remove acentos para busca robusta (força → forca)."""
    nfd = unicodedata.normalize("NFD", texto.lower())
    return "".join(c for c in nfd if unicodedata.category(c) != "Mn")


def _baixar(versao: str) -> list:
    url = _URL_BASE.format(versao=versao)
    nome = VERSOES.get(versao, versao.upper())
    print(f"Baixando Bíblia ({nome})...", end="", flush=True)
    try:
        with urllib.request.urlopen(url, timeout=10) as resp:
            print(" [conectado]", end="", flush=True)
            dados = json.loads(resp.read().decode("utf-8-sig"))
        print(" [salvando]", end="", flush=True)
        _cache_path(versao).write_text(json.dumps(dados, ensure_ascii=False), encoding="utf-8")
        print(" Pronto!")
        return dados
    except urllib.error.URLError as e:
        print(f"\nErro: Não foi possível conectar à internet.\n   {e}")
        print("   Verifique sua conexão e tente novamente.")
        raise SystemExit(1)
    except json.JSONDecodeError as e:
        print(f"\nErro: JSON inválido recebido da internet: {e}")
        raise SystemExit(1)


def carregar(versao: str = VERSAO_PADRAO) -> list:
    """Retorna a Bíblia completa. Usa cache se já baixou antes."""
    cache = _cache_path(versao)
    if cache.exists():
        try:
            dados = json.loads(cache.read_text(encoding="utf-8"))
            if not isinstance(dados, list) or len(dados) != 66:
                print("Cache corrompido, refazendo download...")
                cache.unlink()
                return _baixar(versao)
            return dados
        except (json.JSONDecodeError, UnicodeDecodeError):
            print("Cache corrompido, refazendo download...")
            cache.unlink()
            return _baixar(versao)
    return _baixar(versao)


def info_cache(versao: str = VERSAO_PADRAO) -> dict | None:
    """Retorna informações sobre o cache local, ou None se não existir."""
    cache = _cache_path(versao)
    if not cache.exists():
        return None
    from datetime import datetime
    stat = cache.stat()
    try:
        dados = json.loads(cache.read_text(encoding="utf-8"))
        total = sum(len(cap) for livro in dados for cap in livro["chapters"])
    except Exception:
        total = 0
    return {
        "versao": versao,
        "nome": VERSOES.get(versao, versao.upper()),
        "total_versos": total,
        "tamanho_mb": stat.st_size / (1024 * 1024),
        "atualizado": datetime.fromtimestamp(stat.st_mtime).strftime("%d/%m/%Y %H:%M:%S"),
        "fonte": _URL_BASE.format(versao=versao),
    }


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
    """Busca versículos que contenham o termo (case e acento insensitive)."""
    termo_norm = _normalizar(termo)
    vistos: set[str] = set()
    resultados = []
    for livro in biblia:
        for cap_idx, capitulo in enumerate(livro["chapters"]):
            for ver_idx, texto in enumerate(capitulo):
                if (termo_norm in _normalizar(texto)
                        or termo_norm in _normalizar(livro["name"])):
                    ref = f"{livro['name']} {cap_idx + 1}:{ver_idx + 1}"
                    if ref not in vistos:
                        vistos.add(ref)
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


def encontrar_indices(biblia: list, referencia: str) -> tuple | None:
    """Converte 'Livro cap:ver' em (book_idx, cap_idx, ver_idx) ou None."""
    try:
        match = re.search(r"^(.+)\s+(\d+):(\d+)$", referencia.strip())
        if not match:
            return None
        livro_nome, cap_str, ver_str = match.groups()
        cap_idx = int(cap_str) - 1
        ver_idx = int(ver_str) - 1
        livro_lower = livro_nome.lower().strip()
        for i, livro in enumerate(biblia):
            if livro["name"].lower() == livro_lower:
                if 0 <= cap_idx < len(livro["chapters"]):
                    if 0 <= ver_idx < len(livro["chapters"][cap_idx]):
                        return i, cap_idx, ver_idx
                return None
    except (ValueError, AttributeError):
        pass
    return None
