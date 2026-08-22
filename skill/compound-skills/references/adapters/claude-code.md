# Adapter — Claude Code / Claude Desktop

Overlap com o formato nativo de Skills: alto (~70%). Decisão correta: **UPGRADE do
formato nativo**, não um sistema paralelo.

## Instalação

```bash
git clone https://github.com/FLSDF79/compound-skills.git
cp -r compound-skills/skill/compound-skills ~/.claude/skills/
python3 ~/.claude/skills/compound-skills/scripts/compound.py status
```

## Índice (`~/.claude/CLAUDE.md`) — 8 linhas, nunca o playbook inteiro

```markdown
## SELF IMPROVEMENT COMPOUND SKILLS
Manual apenas: /evoluir. Nunca ao fim de tarefa.
Crescimento contínuo em profundidade; largura com teto (1 skill nova/mês, 16k chars de descrições).
Antes de criar: scan de novelty, Regra de 3, probes de regressão.
Playbook: ~/.claude/skills/compound-skills/SKILL.md
Um motor só. Não criar skills primas (self-improve, evolution, harvest).
```

## Integração com auditoria

Se você tem uma skill de auditoria (`/checkup` ou similar), **delegue a ela** a
verificação de colisão e segredos. Não reimplemente. O motor propõe; o auditor julga.

## O que não fazer

- Não usar memória do host como ledger. Memória esquece procedimento
- Não colar o bloco portátil no `CLAUDE.md` se você já instalou a pasta — nascem dois
  motores
