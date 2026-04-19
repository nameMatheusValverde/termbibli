# Versículos Bíblicos no Terminal

Aplicativo de linha de comando em Python que exibe versículos bíblicos no terminal com formatação colorida. A Bíblia completa em português (Almeida Atualizada — 31.104 versículos) é baixada automaticamente na primeira execução e salva em cache local, sem necessidade de nenhuma dependência externa.

---

## Como foi feito

O projeto foi desenvolvido com auxílio do **Claude Code** — a CLI oficial da Anthropic para o modelo de inteligência artificial Claude. Todo o código foi gerado e refinado de forma interativa diretamente no terminal, sem uso de editor de código ou IDE para escrita manual.

O processo foi:
1. Prompt descrevendo o objetivo (exibir versículos no terminal ao abrir)
2. Claude Code gerou a estrutura inicial com versículos fixos em um vetor
3. Após feedback, foi refatorado para buscar a Bíblia completa automaticamente via internet
4. Ajustes de encoding (UTF-8 BOM) e chaves do JSON foram corrigidos iterativamente

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
├── main.py           # Ponto de entrada — lê os argumentos e chama os módulos
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
git clone nameMatheusValverde
cd versiculos
```

Não é necessário instalar nenhuma dependência. Na primeira execução o próprio programa baixa e salva a Bíblia localmente.

---

## Como usar

```bash
python3 main.py                      # versículo aleatório
python3 main.py --dia                # mesmo versículo durante todo o dia
python3 main.py --buscar <palavra>   # busca por palavra no texto ou livro
python3 main.py --total              # exibe o total de versículos na Bíblia
```

### Exemplos

```bash
python3 main.py --buscar amor
python3 main.py --buscar salmos
python3 main.py --dia
```

---

## .gitignore recomendado

```
biblia_cache.json
.claude/settings.local.json
```
