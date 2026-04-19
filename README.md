# terbibli

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
| **GitHub (thiagobodruk/biblia)** | Fonte da Bíblia completa em JSON — versão **Almeida Atualizada (AA)** |

### Bibliotecas Python (todas nativas — sem instalação extra)

| Biblioteca | Uso no projeto |
|---|---|
| `argparse` | Leitura e validação dos argumentos da linha de comando |
| `json` | Leitura e escrita do cache local da Bíblia (`biblia_cache.json`) |
| `random` | Sorteio aleatório de livro, capítulo e versículo |
| `urllib.request` | Download do JSON da Bíblia direto do GitHub |
| `pathlib` | Manipulação de caminhos de arquivo de forma multiplataforma |
| `datetime` | Cálculo do versículo fixo do dia baseado na data atual |
| `textwrap` | Quebra automática do texto do versículo |
| `shutil` | Detecção da largura real do terminal |
| `curses` | Leitor visual interativo da Bíblia completa |

---

## Estrutura do Projeto

```
versiculos/
├── terbibli           # Executável — ponto de entrada do comando
├── biblia.py          # Download, cache e lógica (aleatorio, do_dia, buscar, buscar_tema)
├── display.py         # Formatação e cores no terminal (caixas ANSI)
├── biblia_visual.py   # Leitor visual interativo (curses TUI)
└── biblia_cache.json  # Gerado automaticamente na 1ª execução (não versionar)
```

---

## Requisitos

- Python 3.10 ou superior
- Conexão com internet **apenas na primeira execução** (para baixar a Bíblia)
- Terminal com suporte a cores ANSI

Para verificar sua versão do Python:
```bash
python3 --version
```

---

## Instalação

### Linux

```bash
git clone https://github.com/nameMatheusValverde/termbibli.git
cd termbibli/versiculos

chmod +x terbibli
ln -sf "$PWD/terbibli" ~/.local/bin/terbibli
```

Se `~/.local/bin` não estiver no PATH, adicione ao `~/.bashrc` ou `~/.zshrc`:
```bash
export PATH="$HOME/.local/bin:$PATH"
```

### macOS

```bash
git clone https://github.com/nameMatheusValverde/termbibli.git
cd termbibli/versiculos

chmod +x terbibli

# Opção 1 — link simbólico (recomendado)
mkdir -p ~/.local/bin
ln -sf "$PWD/terbibli" ~/.local/bin/terbibli
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc

# Opção 2 — via /usr/local/bin (requer sudo)
sudo ln -sf "$PWD/terbibli" /usr/local/bin/terbibli
```

> No macOS o Python nativo pode ser o 2.x. Instale o Python 3 via [Homebrew](https://brew.sh): `brew install python`

### Windows

**Via WSL (recomendado):** instale o WSL e siga as instruções do Linux acima.

**Via PowerShell (sem WSL):**

```powershell
git clone https://github.com/nameMatheusValverde/termbibli.git
cd termbibli\versiculos

# Executa diretamente
python terbibli

# Cria alias permanente no perfil do PowerShell
Add-Content $PROFILE "`nfunction terbibli { python '$PWD\terbibli' @args }"
. $PROFILE
```

> O leitor visual (`--visual`) requer um terminal com suporte a curses. No Windows, use o Windows Terminal com WSL para a melhor experiência.

---

## Como usar

```bash
terbibli                       # versículo aleatório
terbibli --dia                 # mesmo versículo durante todo o dia
terbibli --buscar <palavra>    # busca por palavra no texto ou livro
terbibli --tema <tema>         # busca por tema predefinido
terbibli --total               # exibe o total de versículos na Bíblia
terbibli --temas               # lista todos os temas disponíveis
terbibli --info                # informações sobre o cache local da Bíblia
terbibli --visual              # abre o leitor visual da Bíblia completa
terbibli --dia --visual        # versículo do dia destacado no leitor visual
```

### Exemplos

```bash
terbibli --buscar amor
terbibli --buscar salmos
terbibli --buscar "1 João"     # livros numerados funcionam normalmente
terbibli --buscar forca        # busca sem acento encontra "força"
terbibli --tema alegria
terbibli --tema tristeza
terbibli --tema obediência
terbibli --info
terbibli --dia --visual
```

---

## Temas disponíveis

Use `terbibli --temas` para listar todos. Os principais:

| Tema | Palavras-chave buscadas |
|---|---|
| `amor` | amor, amar, amou, amará |
| `fé` | fé, fiel, fidelidade, crer, crença |
| `esperança` | esperança, esperar, aguardar |
| `paz` | paz, pacífico, pacificador |
| `alegria` | alegria, alegre, regozijar, regozijo, júbilo |
| `tristeza` | tristeza, triste, chorar, choro, lamentação, pranto |
| `obediência` | obedecer, obediente, obediência, obedeceu |
| `graça` | graça, gracioso, misericórdia |
| `perdão` | perdão, perdoar, perdoa, perdoado |
| `sabedoria` | sabedoria, sábio, entendimento, discernimento |
| `força` | força, forte, fortalecer, poderoso |
| `cura` | cura, curar, sarar, saúde |
| `oração` | oração, orar, orai, rogai |
| `salvação` | salvação, salvo, salvar, redenção |
| `ressurreição` | ressurreição, ressuscitar, ressuscitou |
| `gratidão` | gratidão, grato, agradecer, graças |
| `humildade` | humildade, humilde, humilhar |

---

## Leitor Visual (`--visual`)

O leitor visual abre uma interface interativa no terminal com a Bíblia completa:

- **Painel esquerdo:** lista de todos os 66 livros
- **Painel direito:** versículos do capítulo atual com numeração
- Quando chamado com `--dia --visual` ou `--visual` após um versículo aleatório, o versículo exibido aparece **destacado em amarelo** na posição exata da Bíblia

### Navegação

| Tecla | Ação |
|---|---|
| `↑` / `↓` | Rolar versículos |
| `←` / `→` | Capítulo anterior / próximo |
| `PgUp` / `PgDn` | Rolar página inteira |
| `Home` / `End` | Ir ao início / fim do capítulo |
| `q` ou `Esc` | Sair |

---

## Cache local

A Bíblia é baixada automaticamente na primeira execução e salva em `versiculos/biblia_cache.json`. Nas execuções seguintes, o arquivo local é usado diretamente — sem acesso à internet.

Se o cache estiver corrompido, o terbibli detecta automaticamente e refaz o download.

Para inspecionar o cache:

```bash
terbibli --info
# Cache da Bíblia
#   Versículos : 31.104
#   Tamanho    : 3.8 MB
#   Atualizado : 18/04/2026 19:57:41
#   Fonte      : https://raw.githubusercontent.com/...
```

---

## Segurança

O termo passado em `--buscar` é validado antes de qualquer processamento:

- Não pode ser vazio
- Máximo de 100 caracteres
- Apenas letras, números, espaços, caracteres acentuados e símbolos básicos (`- ' ( ) : . , ;`) são aceitos

---
