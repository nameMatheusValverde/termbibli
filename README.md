# Termu Linux — terbibli

Ferramenta de linha de comando em Python que exibe versículos bíblicos no terminal com formatação colorida. A Bíblia completa em português (Almeida Atualizada — 31.104 versículos) é baixada automaticamente na primeira execução e salva em cache local, sem necessidade de nenhuma dependência externa.

---

## Como foi feito

O projeto foi desenvolvido com auxílio do **Claude Code** — a CLI oficial da Anthropic para o modelo de inteligência artificial Claude. Todo o código foi gerado e refinado de forma interativa diretamente no terminal, sem uso de editor de código ou IDE para escrita manual.

O processo foi:
1. Prompt descrevendo o objetivo (exibir versículos no terminal ao abrir)
2. Claude Code gerou a estrutura inicial com versículos fixos em um vetor
3. Após feedback, foi refatorado para buscar a Bíblia completa automaticamente via internet
4. Ajustes de encoding (UTF-8 BOM) e chaves do JSON foram corrigidos iterativamente
5. Renomeado para **Termu Linux** com comando `terbibli` e camada de validação de entrada

---

## Linguagem e Ferramentas

| Ferramenta | Descrição |
|---|---|
| **Python 3.10+** | Linguagem principal do projeto |
| **Claude Code** | IA utilizada para gerar e refinar o código |
| **GitHub (thiagobodruk/biblia)** | Fonte da Bíblia completa em JSON |

### Bibliotecas Python (todas nativas — sem instalação extra)

| Biblioteca | Uso no projeto |
|---|---|
| `argparse` | Leitura e validação dos argumentos da linha de comando (`--dia`, `--buscar`, etc.) |
| `json` | Leitura e escrita do cache local da Bíblia (`biblia_cache.json`) |
| `random` | Sorteio aleatório de livro, capítulo e versículo |
| `urllib.request` | Download do JSON da Bíblia direto do GitHub sem dependências externas |
| `pathlib` | Manipulação de caminhos de arquivo de forma multiplataforma |
| `datetime` | Cálculo do versículo fixo do dia baseado na data atual |
| `textwrap` | Quebra automática do texto do versículo conforme a largura do terminal |
| `shutil` | Detecção da largura real do terminal para formatação da caixa |

---

## Estrutura do Projeto

```
versiculos/
├── terbibli          # Executável — ponto de entrada do comando
├── biblia.py         # Download, cache e lógica (aleatorio, do_dia, buscar)
├── display.py        # Formatação e cores no terminal (caixas com ANSI escape codes)
└── biblia_cache.json # Gerado automaticamente na 1ª execução (não versionar)
```

---

## Requisitos

- Python 3.10 ou superior
- Conexão com internet **apenas na primeira execução** (para baixar a Bíblia)
- Terminal com suporte a cores ANSI (qualquer terminal moderno no Linux/macOS)

Para verificar sua versão do Python:
```bash
python3 --version
```

---

## Instalação

```bash
# Clone o repositório
git clone https://github.com/nameMatheusValverde/termbibli.git
cd versiculos

# Torne o executável e crie o atalho no terminal
chmod +x terbibli
ln -sf "$PWD/terbibli" ~/.local/bin/terbibli
```

Não é necessário instalar nenhuma dependência. Na primeira execução o próprio programa baixa e salva a Bíblia localmente.

---

## Como usar

```bash
terbibli                     # versículo aleatório
terbibli --dia               # mesmo versículo durante todo o dia
terbibli --buscar <palavra>  # busca por palavra no texto ou livro
terbibli --total             # exibe o total de versículos na Bíblia
```

### Exemplos

```bash
terbibli --buscar amor
terbibli --buscar salmos
terbibli --dia
```

---

## Segurança

O termo passado em `--buscar` é validado antes de qualquer processamento:

- Não pode ser vazio
- Máximo de 100 caracteres
- Apenas letras, espaços e caracteres acentuados do português são aceitos

---

## .gitignore recomendado

```
biblia_cache.json
.claude/settings.local.json
```
