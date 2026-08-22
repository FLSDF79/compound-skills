# Segurança

## Modelo de ameaça e garantias

- `compound.py` é **Python 3.8+ stdlib puro**: sem dependências, sem chamadas de
  rede, sem `exec`/`eval`/`subprocess`, sem telemetria externa. Todo estado fica
  em `COMPOUND_HOME` (padrão `~/.compound-skills`), local.
- Nomes de skill recebidos por CLI são validados (sem separadores de caminho,
  sem `..`) antes de qualquer operação de arquivo, e operações destrutivas
  (`stub`, `archive`, `rollback`) ainda resolvem o caminho real e o contêm
  dentro do skills root — defesa extra contra symlinks e contra instruções
  maliciosas embutidas em skills lidas (path traversal via prompt injection).
- Operações destrutivas têm rede de segurança: `stub` faz backup automático
  antes de sobrescrever, `archive` é reversível, `rollback` preserva o estado
  atual antes de restaurar.
- O parser de frontmatter é regex mínimo, sem YAML loader — arquivos SKILL.md de
  terceiros são tratados como texto, nunca executados.

## O sanitizador é heurístico

`compound.py sanitize` detecta padrões conhecidos de credenciais (OpenAI/
Anthropic, GitHub, GitLab, npm, Slack, AWS, Google, JWT, chaves privadas,
strings de conexão), PII brasileira (CPF, CNPJ, agência+conta, cartão) e
caminhos pessoais absolutos. Ele **reduz** o risco de vazamento; não o elimina.
Supressões (`# sanitize-ok` e `.sanitizeignore`) são pontos cegos escolhidos —
use com parcimônia e revise o diff antes de todo push.

O relatório nunca imprime o valor detectado: mostra apenas categoria, arquivo,
linha e fingerprint SHA-256 curto para correlação. Mesmo assim, logs públicos
devem ser tratados como artefatos potencialmente sensíveis.

## Concorrência do estado

As gravações de `state.json` usam arquivo temporário único no mesmo diretório e
troca atômica. O projeto não implementa lock de processo: opere em modo
**single-writer** (um comando mutável por `COMPOUND_HOME` de cada vez).

## Reportar vulnerabilidade

Abra uma issue com o rótulo `security` **sem** incluir o segredo/dado exposto no
corpo, ou contate o mantenedor por mensagem direta no LinkedIn. Correções de
sanitização (novos padrões de credencial) são bem-vindas via pull request.
