#!/usr/bin/env python3
"""
biblia_visual.py — Leitor visual interativo da Bíblia completa (curses).

Uso direto:
    python3 biblia_visual.py
    python3 biblia_visual.py "Gênesis 1:1"   # abre e destaca o versículo

Via termbibli:
    termbibli --visual
    termbibli --dia --visual
"""

import curses
import sys
import os
import textwrap

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import biblia as bib


# ── Cores (par curses) ────────────────────────────────────────────────────────
COR_BORDA    = 1   # cyan sobre preto
COR_LIVRO    = 2   # amarelo sobre preto  (livro selecionado)
COR_VERSO    = 3   # verde sobre preto
COR_DESTAQUE = 4   # preto sobre amarelo  (versículo destacado)
COR_NORMAL   = 5   # branco sobre preto
COR_HEADER   = 6   # branco bold sobre azul


def _init_cores():
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(COR_BORDA,    curses.COLOR_CYAN,   -1)
    curses.init_pair(COR_LIVRO,    curses.COLOR_YELLOW, -1)
    curses.init_pair(COR_VERSO,    curses.COLOR_GREEN,  -1)
    curses.init_pair(COR_DESTAQUE, curses.COLOR_BLACK,  curses.COLOR_YELLOW)
    curses.init_pair(COR_NORMAL,   curses.COLOR_WHITE,  -1)
    curses.init_pair(COR_HEADER,   curses.COLOR_WHITE,  curses.COLOR_BLUE)


def _wrap_capitulo(capitulo: list, largura: int) -> list[tuple[int, str]]:
    """Retorna lista de (ver_idx, linha_texto) com quebra de linha."""
    linhas = []
    for vi, texto in enumerate(capitulo):
        prefixo = f"{vi + 1:>3}. "
        indent  = " " * len(prefixo)
        wraps   = textwrap.wrap(texto, width=largura - len(prefixo) - 1) or [""]
        for j, linha in enumerate(wraps):
            linhas.append((vi, (prefixo if j == 0 else indent) + linha))
    return linhas


def _tela(stdscr, dados: list, destaque_orig: tuple | None):
    """Wrapper que mantém o highlight do versículo durante toda a sessão."""
    curses.curs_set(0)
    _init_cores()

    book_idx  = destaque_orig[0] if destaque_orig else 0
    cap_idx   = destaque_orig[1] if destaque_orig else 0
    ver_scroll  = 0
    book_scroll = 0
    centralizado = False   # scroll automático feito apenas na primeira renderização

    while True:
        h, w = stdscr.getmaxyx()
        stdscr.erase()

        LIVRO_W = max(18, min(24, w // 5))
        VERSO_X = LIVRO_W + 1
        VERSO_W = w - VERSO_X

        livro    = dados[book_idx]
        capitulo = livro["chapters"][cap_idx] if cap_idx < len(livro["chapters"]) else []

        # Cabeçalho global
        titulo  = " termbibli — Bíblia Visual "
        atalhos = " q:sair  ←→:capítulo  ↑↓:rolar  PgUp/PgDn "
        header  = titulo + atalhos.rjust(w - len(titulo) - 1)[: w - len(titulo) - 1]
        try:
            stdscr.addstr(0, 0, header[:w], curses.color_pair(COR_HEADER) | curses.A_BOLD)
        except curses.error:
            pass

        # Separador
        for row in range(1, h - 1):
            try:
                stdscr.addch(row, LIVRO_W, "│", curses.color_pair(COR_BORDA))
            except curses.error:
                pass

        # Painel de livros
        for i in range(h - 2):
            idx = i + book_scroll
            if idx >= len(dados):
                break
            nome = dados[idx]["name"][: LIVRO_W - 3]
            if idx == book_idx:
                attr, marker = curses.color_pair(COR_LIVRO) | curses.A_BOLD, "►"
            else:
                attr, marker = curses.color_pair(COR_NORMAL), " "
            try:
                stdscr.addstr(i + 1, 0, f"{marker} {nome}", attr)
            except curses.error:
                pass

        # Cabeçalho de versículos
        cap_header = f" {livro['name']}  —  Capítulo {cap_idx + 1} / {len(livro['chapters'])}"
        try:
            stdscr.addstr(1, VERSO_X, cap_header[: VERSO_W - 1],
                          curses.color_pair(COR_BORDA) | curses.A_BOLD)
        except curses.error:
            pass

        linhas    = _wrap_capitulo(capitulo, VERSO_W)
        area      = h - 3

        # Centraliza na primeira vez que chega no capítulo do destaque
        if (not centralizado and destaque_orig
                and destaque_orig[0] == book_idx
                and destaque_orig[1] == cap_idx):
            alvo_ver = destaque_orig[2]
            primeira = next((li for li, (vi, _) in enumerate(linhas) if vi == alvo_ver), 0)
            ver_scroll = max(0, primeira - area // 2)
            centralizado = True

        # Renderiza versículos com highlight
        for row in range(area):
            li = row + ver_scroll
            if li >= len(linhas):
                break
            vi, linha = linhas[li]

            eh_dest = (
                destaque_orig is not None
                and destaque_orig[0] == book_idx
                and destaque_orig[1] == cap_idx
                and destaque_orig[2] == vi
            )
            attr = curses.color_pair(COR_DESTAQUE) | curses.A_BOLD if eh_dest else curses.color_pair(COR_VERSO)
            try:
                stdscr.addstr(row + 2, VERSO_X, linha[: VERSO_W - 1], attr)
            except curses.error:
                pass

        # Rodapé
        dest_info = ""
        if destaque_orig:
            dest_info = f"  ★ {dados[destaque_orig[0]]['name']} {destaque_orig[1]+1}:{destaque_orig[2]+1}"
        rodape = f" Livro {book_idx+1}/{len(dados)}  Cap {cap_idx+1}/{len(livro['chapters'])}{dest_info}"
        try:
            stdscr.addstr(h - 1, 0, rodape[: w - 1], curses.color_pair(COR_BORDA))
        except curses.error:
            pass

        stdscr.refresh()

        key = stdscr.getch()

        if key in (ord('q'), ord('Q'), 27):
            break
        elif key == curses.KEY_UP:
            ver_scroll = max(0, ver_scroll - 1)
        elif key == curses.KEY_DOWN:
            ver_scroll = min(max(0, len(linhas) - area), ver_scroll + 1)
        elif key == curses.KEY_PPAGE:
            ver_scroll = max(0, ver_scroll - area)
        elif key == curses.KEY_NPAGE:
            ver_scroll = min(max(0, len(linhas) - area), ver_scroll + area)
        elif key == curses.KEY_HOME:
            ver_scroll = 0
        elif key == curses.KEY_END:
            ver_scroll = max(0, len(linhas) - area)
        elif key == curses.KEY_LEFT:
            if cap_idx > 0:
                cap_idx -= 1
            elif book_idx > 0:
                book_idx -= 1
                cap_idx = len(dados[book_idx]["chapters"]) - 1
            ver_scroll = 0
            centralizado = False
        elif key == curses.KEY_RIGHT:
            if cap_idx < len(livro["chapters"]) - 1:
                cap_idx += 1
            elif book_idx < len(dados) - 1:
                book_idx += 1
                cap_idx = 0
            ver_scroll = 0
            centralizado = False

        if book_idx < book_scroll:
            book_scroll = book_idx
        elif book_idx >= book_scroll + (h - 2):
            book_scroll = book_idx - (h - 2) + 1


def run(dados: list, referencia: str | None = None):
    """Ponto de entrada chamado pelo termbibli."""
    destaque = bib.encontrar_indices(dados, referencia) if referencia else None
    curses.wrapper(_tela, dados, destaque)


if __name__ == "__main__":
    ref   = sys.argv[1] if len(sys.argv) > 1 else None
    dados = bib.carregar()
    run(dados, ref)
