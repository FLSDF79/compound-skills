# SELF IMPROVEMENT COMPOUND SKILLS

**Motor de evolução composta para ecossistemas de skills de IA — com poda
obrigatória.** Favorece crescimento contínuo em *profundidade* (cada skill pode
ficar melhor a cada ciclo) e impõe teto rígido em *largura* (quantidade de skills,
orçamento de contexto). Profundidade sem teto é uma tese operacional, não uma
garantia matemática ou de compatibilidade do host.

O repositório fornece adaptadores para Claude Code, Cursor/Codex, Hermes e outros
agentes com filesystem, além de um bloco portátil degradado para chats. Adaptador
documentado não equivale a compatibilidade certificada em todos os hosts.

> **English TL;DR** — A compounding self-improvement engine for AI skill
> ecosystems, with mandatory pruning. It promotes continued growth in *depth*
> while applying hard caps to *width*. Its seven gates are an operational
> playbook; quota, edit limits, context budget and path protections are enforced
> in code, while triage, approval, probes and external review still require the
> operator. Zero dependencies, pure Python stdlib, no network calls or telemetry.
> Docs are in Brazilian Portuguese; a degraded portable version is available at
> [`portable/PASTE-ANY-AI.en.md`](portable/PASTE-ANY-AI.en.md).

---

## Por que este motor existe

Todo sistema de "auto-melhoria" de agentes comete o mesmo erro: confunde duas
grandezas que crescem de formas opostas.

| | Como cresce | Como deve ser tratada |
|---|---|---|
| **Profundidade** — qualidade, casos de borda, mapa de alternativas, pitfalls reais | Composta; o corpo só carrega quando a skill dispara | **Crescimento contínuo** |
| **Largura** — quantidade de skills, soma das descrições, superfície de gatilho | Imposto permanente em toda conversa; colisões crescem em n²/2 | **Teto rígido** |

Doze skills profundas batem sessenta rasas. A pergunta padrão não é "isso vira
skill?" — é **"isso *precisa* virar skill?"**. Na maioria das vezes, não precisa.
Este motor força essa conversa honesta, com números.

## O que ele faz de diferente

1. **Triagem de 6 destinos** — descarte, regra de índice, script, ledger,
   aprofundar existente (o *default*), skill nova (a exceção). Para no destino
   mais barato que resolve.
2. **Novelty % medido, não sentido** — `overlap = goal(0-40) + mechanism(0-30) +
   triggers(0-30)`. O eixo de gatilho é calculado mecanicamente contra as skills
   instaladas; os outros dois você declara com justificativa. O número decide:
   ABSORB / UPGRADE / SUPERSEDE / SKIP.
3. **Probes de regressão de gatilho** — 3 frases que *devem* disparar, 1 que
   *não* deve. Detecta gatilho quebrado por edição e colisão entre skills antes
   de publicar. É a rede de segurança que motores de auto-melhoria não têm.
4. **Portões aplicados por código: cota, edições, orçamento e caminhos** — o script *bloqueia* (exit ≠ 0),
   não avisa: 1 skill nova/mês, 2 edições/dia (proxy verificável de sessão) e
   orçamento somado de descrições. Largura é soma zero. E adotar uma skill que
   já existia no disco não consome cota — só criação consome.
5. **Backup, diff, rollback** — a CLI oferece uma rede de segurança reversível;
   o operador ainda precisa executar backup/diff no momento correto.
6. **Anti-ledger** — registra o que **não** funcionou, com o motivo. Falha
   registrada fecha um caminho inteiro por duas linhas e não se repete.
7. **N caminhos** — após cada entrega, o mapa de alternativas da skill cresce
   (quando ganha, custo, critério de morte de cada caminho). É o vetor de
   crescimento sem teto: para dentro, não para os lados.
8. **Data de morte** — toda skill nasce com revisão em 90 dias: manter, fundir
   ou arquivar. Telemetria local de uso decide, não memória afetiva. Motor de
   criação sem ciclo de morte é entropia com changelog.
9. **Sanitizador pré-publicação best-effort** — procura padrões conhecidos de
   segredos (chaves de API, tokens, JWT,
   strings de conexão), PII brasileira (CPF, CNPJ, agência+conta) e caminhos
   pessoais antes de qualquer `git push`.
10. **Separação de poderes** — o motor propõe; um auditor externo (outra skill,
    outro agente ou revisão humana) julga. Quem cria não audita sozinho.

## Instalação

### Claude Code / Claude Desktop

```bash
git clone https://github.com/FLSDF79/compound-skills.git
cp -r compound-skills/skill/compound-skills ~/.claude/skills/
python3 ~/.claude/skills/compound-skills/scripts/compound.py status
```

Depois adicione ao `~/.claude/CLAUDE.md` o índice de 6 linhas descrito em
[`skill/compound-skills/references/adapters/claude-code.md`](skill/compound-skills/references/adapters/claude-code.md).

### Claude.ai (web/app)

Envie a pasta `skill/compound-skills` empacotada como `.skill` (ou use o release
deste repositório) e clique em **Save skill**.

### Cursor / Codex / agentes de repositório

[`references/adapters/cursor-codex.md`](skill/compound-skills/references/adapters/cursor-codex.md)
— rule manual apontando para o playbook; em repositório compartilhado, edição de
playbook vai por pull request e a cota é do repositório, não da pessoa.

### Hermes Agent e agentes 24/7 com filesystem

[`references/adapters/hermes-agent.md`](skill/compound-skills/references/adapters/hermes-agent.md)
— instalação, `COMPOUND_SKILLS_ROOT`, e as quatro regras de agente contínuo
(motor único, ciclo nunca autônomo, guarda de custo de LLM, fronteira
desktop×VPS).

### ChatGPT, Gemini, Perplexity e qualquer IA de chat

Cole [`portable/PASTE-ANY-AI.md`](portable/PASTE-ANY-AI.md) (pt-BR) **ou**
[`portable/PASTE-ANY-AI.en.md`](portable/PASTE-ANY-AI.en.md) (EN) nas Custom
Instructions / System Prompt / Gem — uma língua só por host. **Não** instale a pasta *e* cole o bloco no
mesmo host: dois motores derivam — é exatamente o problema que o motor combate.

### Claude Code — subagentes com modelo barato (opcional)

A pasta [`agents/`](agents/) traz dois subagentes prontos, ambos `model: haiku`,
sem Write/Edit:

```bash
cp compound-skills/agents/*.md ~/.claude/agents/
```

| Camada | Quem | Custo | Faz |
|---|---|---|---|
| 0 | shell puro | zero token | `compound.py status/budget/sanitize/probes` — o grosso do motor |
| 1 | `compound-runner`, `compound-scout` (Haiku) | ~1/3 do Sonnet | executa bateria de comandos, digere saída, monta dossiê de novelty |
| 2 | modelo principal da sessão | cheio | só decide: aprova goal/mech, escolhe destino, autoriza `commit` |

A regra de economia é a ordem das camadas: **o que resolve em shell não sobe
para Haiku; o que Haiku prepara, o modelo principal só julga.** Subagente não
comita, não edita e não desprotege — os portões continuam no dono.

## Primeiro comando (e o mais importante)

```bash
python3 skill/compound-skills/scripts/compound.py budget
```

Se você já usa skills há meses, é provável que esteja acima de 80% do orçamento
sem saber — e isso muda a conversa sobre criar qualquer coisa nova. O motor
começa pelo diagnóstico, não pela criação.

## Comandos

| Comando | Faz |
|---|---|
| `status` | Visão geral: cota, orçamento, ledger, revisões vencidas |
| `budget` | Orçamento de contexto das descrições (stubs sinalizados) |
| `scan "<descrição>" --goal N --mech N` | Novelty % contra o instalado → ABSORB/UPGRADE/SUPERSEDE |
| `ledger-add` / `ledger-list` | Regra de 3: ocorrências antes de virar skill |
| `anti-add` / `anti-list` | Caminhos que falharam — e por quê |
| `probe-add` / `probe-run` | Frases-teste de gatilho; detecta quebra e colisão |
| `backup` / `diff` / `rollback` | Rede de segurança de edição |
| `sanitize <caminho>` | Varredura de segredos/PII antes de publicar |
| `protect add\|remove\|list` | Skills que exigem confirmação escrita a cada edição |
| `commit` / `stub` / `use` | Versão, procedência, telemetria de uso |
| `review-due` / `review-renew` / `archive` | O ciclo de morte dos 90 dias |

Ativação no host de IA: `/evoluir` (ciclo completo), `/evoluir status`,
`/evoluir scan`, `/evoluir revisao`, `/evoluir rollback`. **Manual apenas** —
nunca ao fim de tarefa, nunca por entusiasmo.

### O que o código realmente bloqueia

Os sete portões formam o playbook completo. O CLI aplica por código cota mensal,
limite diário de edições, orçamento de descrições, validação/contenção de caminhos
e proteção de skills. Regra de 3, triagem, backup/diff, aval humano, execução de
probes e auditoria externa são portões operacionais: o `commit` não consegue provar
sozinho que ocorreram. Automação não substitui disciplina do operador.

## Configuração

Tudo por variável de ambiente — nada de editar código:

| Variável | Default | O que controla |
|---|---|---|
| `COMPOUND_HOME` | `~/.compound-skills` | Estado, ledger, backups |
| `COMPOUND_SKILLS_ROOT` | `~/.claude/skills` | Onde suas skills vivem |
| `COMPOUND_BUDGET_CHARS` | `16000` | Orçamento somado das descrições |
| `COMPOUND_TETO_NOVAS_MES` | `1` | Skills novas por mês |
| `COMPOUND_TETO_EDICOES_DIA` | `2` | Edições gravadas por dia (proxy de sessão) |
| `COMPOUND_REGRA_DE_N` | `3` | Ocorrências antes de elegível |
| `COMPOUND_REVISAO_DIAS` | `90` | Janela até a revisão de morte |
| `COMPOUND_PROTEGIDAS` | *(vazio)* | Protegidas extras, separadas por vírgula |
| `COMPOUND_MARCADORES` | *(vazio)* | Marcadores restritos extras para o sanitize |

**Os defaults são opinativos**, calibrados para ecossistemas de ~15–30 skills.
Ajuste **uma vez, na instalação, com critério** — nunca no meio de um ciclo
porque o teto incomodou. Teto que só vale quando é confortável não é teto.

### Skills protegidas

De fábrica, só a própria `compound-skills` é protegida. Seu inventário pessoal
**não pertence ao código-fonte**: adicione as suas skills de infraestrutura ou
conformidade com `compound.py protect add <nome>` (persiste em `state.json`,
local) ou via `COMPOUND_PROTEGIDAS`. Editar uma protegida exige confirmação
escrita do dono naquela ocasião — confirmação de sessão anterior não vale.

## Segurança e privacidade

- **Zero dependências. Zero rede. Zero telemetria externa.** Python 3.8+ stdlib;
  nenhum `import` de terceiros, nenhuma chamada HTTP, nenhum `exec`/`eval`.
  Tudo que o motor grava fica em `COMPOUND_HOME`, na sua máquina.
- **Nomes de skill validados** contra path traversal em todos os comandos que
  recebem nome.
- **`sanitize` roda no próprio repositório no CI** — o scanner passa em si
  mesmo, e o repo publicado passa no próprio detector de vazamento.
- O scanner é **heurístico**: reduz risco, não o elimina. Releia o diff antes de
  qualquer `git push`. Achados exibem tipo, arquivo, linha e fingerprint curto,
  nunca o valor detectado. Detalhes e reporte de vulnerabilidades:
  [`SECURITY.md`](SECURITY.md).

## Estrutura do repositório

```
compound-skills/
├── skill/compound-skills/      # a Skill instalável (formato Claude/Agent Skills)
│   ├── SKILL.md                # o playbook — 7 portões
│   ├── scripts/compound.py    # o motor CLI (stdlib, ~1000 linhas)
│   └── references/            # triagem, novelty, N-caminhos, adapters por host
├── agents/                    # subagentes Haiku p/ Claude Code (runner + scout)
├── portable/PASTE-ANY-AI.md   # modo degradado para hosts sem filesystem (pt-BR)
├── portable/PASTE-ANY-AI.en.md# idem, em inglês — instale UMA língua por host
├── tests/test_compound.py     # suíte de testes (unittest, sem dependências)
└── .github/workflows/ci.yml   # testes em 3.8–3.12 + sanitize do próprio repo
```

## Filosofia em uma linha

> Skip é o resultado correto na maioria dos ciclos — e não é fracasso: é o motor
> funcionando.

## Licença

[MIT](LICENSE). Construído por
[Fabiano Lopes da Silva](https://www.linkedin.com/in/flsdf79) —
gestão bancária + IA aplicada, Brasília-DF.

## Proveniência

Projeto original de Fabiano Lopes da Silva. Padrões gerais de governança,
engenharia de agentes, TDD e revisão independente informaram o desenho. O projeto
não reivindica autoria sobre ferramentas, formatos ou conceitos de terceiros e
registra absorções específicas quando houver fonte identificável.
