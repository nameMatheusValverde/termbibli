#!/usr/bin/env python3
"""
Ponto de entrada do sistema de versículos.

Uso:
    python3 main.py               → versículo aleatório
    python3 main.py --dia         → versículo fixo do dia
    python3 main.py --buscar amor → busca por palavra-chave
    python3 main.py --total       → quantidade de versículos na Bíblia
"""

import argparse
import biblia
import display


def main():
    parser = argparse.ArgumentParser(
        description="Sistema de versículos bíblicos no terminal."
    )
    grupo = parser.add_mutually_exclusive_group()
    grupo.add_argument("--dia",    action="store_true", help="Versículo fixo do dia")
    grupo.add_argument("--buscar", metavar="TERMO",     help="Busca por palavra-chave")
    grupo.add_argument("--total",  action="store_true", help="Total de versículos na Bíblia")

    args = parser.parse_args()

    try:
        dados = biblia.carregar()
    except Exception as e:
        print(f"Erro ao carregar a Bíblia: {e}")
        return

    if args.dia:
        ref, texto = biblia.do_dia(dados)
        display.exibir(ref, texto, titulo="Versículo do Dia")

    elif args.buscar:
        resultados = biblia.buscar(dados, args.buscar)
        display.listar_resultados(resultados)

    elif args.total:
        total = sum(
            len(cap) for livro in dados for cap in livro["chapters"]
        )
        print(f"\nTotal de versículos na Bíblia: {total:,}\n")

    else:
        ref, texto = biblia.aleatorio(dados)
        display.exibir(ref, texto, titulo="Versículo Aleatório")


if __name__ == "__main__":
    main()
