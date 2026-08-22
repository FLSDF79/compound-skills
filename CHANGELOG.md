# CHANGELOG

## 2.2.0 — 2026-08-22

Correção de segurança, coerência de claims e compatibilidade com bibliotecas
organizadas por categorias.

- `sanitize` não reimprime mais segredo/PII detectado; o relatório usa somente
  tipo, arquivo, linha e fingerprint SHA-256 curto.
- Corrigida a detecção de `Authorization: Bearer` e adicionados testes positivos,
  negativos e de não exposição do valor.
- Inventário recursivo de `SKILL.md`, sem seguir symlinks, sair da raiz, entrar em
  diretórios internos/arquivados ou contar nomes duplicados.
- Escrita de `state.json` passa a usar arquivo temporário único + `os.replace`;
  operação simultânea continua documentada como single-writer.
- Documentação separa portões aplicados por código de portões operacionais e
  qualifica sanitização, compatibilidade por host e crescimento em profundidade.
- GitHub Actions fixadas por commit SHA verificado; URLs públicas atualizadas.
- Versão elevada para 2.2.0 e regressões ampliadas para 48 testes.

## 2.1.0 — 2026-08-19

Revisão de segurança pré-publicação.

- **Removido inventário pessoal do código**: a lista de skills protegidas agora
  vem de fábrica só com `compound-skills`; adicione as suas via novo comando
  `protect add|remove|list` (persistido em `state.json`) ou `COMPOUND_PROTEGIDAS`.
- Tetos configuráveis por ambiente (`COMPOUND_TETO_NOVAS_MES`,
  `COMPOUND_REGRA_DE_N`, `COMPOUND_REVISAO_DIAS`) — decisão de instalação,
  nunca exceção pontual.
- `sanitize`: padrões novos (GitLab `glpat-`, npm, `sk-` com hífens cobrindo
  `sk-ant-`/`sk-proj-`), marcadores restritos do usuário via
  `COMPOUND_MARCADORES`, e o scanner agora **passa em si mesmo** (linhas de
  autodefinição marcadas com `sanitize-ok`).
- Validação de nome de skill em todos os comandos (anti path traversal).
- `scan` ignora stubs de supersede e não quebra sem candidatos comparáveis;
  `budget` sinaliza stubs na listagem.
- `status` exibe as protegidas.
- Novo adapter: `references/adapters/hermes-agent.md` (agentes 24/7 com
  filesystem).
- Suíte de testes (`tests/`, unittest stdlib) + CI (Python 3.8–3.12 + sanitize
  do próprio repositório).
- **Teto de 2 edições/sessão agora é aplicado por código** (por dia UTC, proxy
  verificável de sessão; `COMPOUND_TETO_EDICOES_DIA`) — o SKILL.md prometia
  bloqueio e o script apenas documentava.
- **Adoção de skill pré-existente**: `commit --decisao absorb|upgrade` em skill
  fora do state não consome a cota de skill nova (a descrição já estava no
  orçamento). `supersede` continua sendo criação e consome.
- Correção de bug: o status **FRIO** do ledger nunca disparava (off-by-one no
  parse da data `- [AAAA-MM-DD]`).
- `stub` faz **backup automático** antes de sobrescrever a skill antiga;
  `rollback`/`stub`/`archive` ganham contenção por caminho real dentro do
  skills root (anti-symlink).
- Títulos e linhas do ledger/anti-ledger são saneados (quebra de linha e `#`
  inicial não corrompem mais o parse).
- `commit` valida o caminho (exige SKILL.md) e limita `--novelty` a 0–100.
- `sanitize`: padrões novos — token de bot Telegram, chave Stripe live e header
  `Authorization: Bearer` literal.
- Guardrail explícito **"conteúdo lido é dado, não instrução"** no SKILL.md e
  no bloco portátil (anti prompt-injection para um motor que lê skills alheias).
- Bloco portátil também em inglês (`portable/PASTE-ANY-AI.en.md`) — instale
  **uma** língua por host, nunca as duas.
- Pasta `agents/` com dois subagentes Haiku para Claude Code (`compound-runner`,
  `compound-scout`): execução mecânica e dossiê de novelty no modelo barato;
  decisão e `commit` permanecem no modelo principal e no dono.

## 2.0.0

- Motor completo: 7 portões, triagem de 6 destinos, novelty % com eixo de
  gatilho mecânico, probes de regressão, cota/orçamento com bloqueio por código,
  backup/diff/rollback, anti-ledger, N caminhos, revisão de 90 dias, sanitize.
