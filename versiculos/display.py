#!/usr/bin/env python3
"""
Módulo de exibição: renderiza versículos no terminal com formatação colorida.
"""

import textwrap
import shutil

RESET  = "\033[0m"
BOLD   = "\033[1m"
YELLOW = "\033[33m"
CYAN   = "\033[36m"
GREEN  = "\033[32m"


def _largura_terminal(maximo: int = 72) -> int:
    return min(shutil.get_terminal_size().columns, maximo)


def exibir(referencia: str, texto: str, titulo: str = "Versículo do Dia") -> None:
    """Exibe um versículo dentro de uma caixa colorida."""
    largura = _largura_terminal()
    borda = "─" * (largura - 2)

    print(f"\n{CYAN}┌{borda}┐{RESET}")

    espacos = (largura - 2 - len(titulo)) // 2
    pad_dir = largura - 2 - espacos - len(titulo)
    print(f"{CYAN}│{RESET}{' ' * espacos}{BOLD}{YELLOW}{titulo}{RESET}{' ' * pad_dir}{CYAN}│{RESET}")

    print(f"{CYAN}├{borda}┤{RESET}")

    for linha in textwrap.wrap(f'"{texto}"', width=largura - 6):
        pad = largura - 2 - len(linha) - 2
        print(f"{CYAN}│{RESET}  {GREEN}{linha}{RESET}{' ' * pad}{CYAN}│{RESET}")

    ref_fmt = f"— {referencia}"
    pad_ref = largura - 2 - len(ref_fmt) - 2
    print(f"{CYAN}│{RESET}  {BOLD}{YELLOW}{ref_fmt}{RESET}{' ' * pad_ref}{CYAN}│{RESET}")

    print(f"{CYAN}└{borda}┘{RESET}\n")


def listar_resultados(resultados: list[tuple[str, str]], titulo_prefixo: str = "") -> None:
    """Exibe uma lista de versículos encontrados numa busca."""
    if not resultados:
        print(f"\n{YELLOW}Nenhum versículo encontrado.{RESET}\n")
        return

    prefixo = f"{titulo_prefixo} " if titulo_prefixo else ""
    print(f"\n{BOLD}{CYAN}{prefixo}Encontrados: {len(resultados)} versículo(s){RESET}\n")
    for i, (ref, texto) in enumerate(resultados, 1):
        exibir(ref, texto, titulo=f"{titulo_prefixo} {i}/{len(resultados)}".strip())
