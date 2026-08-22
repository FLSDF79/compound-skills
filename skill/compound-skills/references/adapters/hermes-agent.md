# Adapter — Hermes Agent e frameworks de agente com filesystem

Para agentes de terminal com acesso a arquivos (ex.: [NousResearch
hermes-agent](https://github.com/NousResearch/hermes-agent)) rodando local
ou em VPS 24/7. O `compound.py` é Python puro, stdlib, sem rede — roda em
qualquer Linux/macOS onde o agente rode.

## Instalação

```bash
git clone https://github.com/FLSDF79/compound-skills.git
mkdir -p ~/.hermes/skills          # ou o diretório de conhecimento do seu agente
cp -r compound-skills/skill/compound-skills ~/.hermes/skills/
COMPOUND_SKILLS_ROOT=~/.hermes/skills \
  python3 ~/.hermes/skills/compound-skills/scripts/compound.py status
```

Ajuste `COMPOUND_SKILLS_ROOT` para onde o SEU agente lê playbooks. O padrão do
script (`~/.claude/skills`) serve Claude; para outros hosts, exporte a variável
no perfil do shell ou no serviço do agente.

## Índice do agente — 7 linhas, nunca o playbook inteiro

No arquivo de sistema do agente (ex.: `~/.hermes/HERMES.md`, `AGENTS.md` ou
equivalente):

```markdown
## SELF IMPROVEMENT COMPOUND SKILLS
Manual apenas: /evoluir. Nunca ao fim de tarefa.
Crescimento contínuo em profundidade; largura com teto (cota mensal + orçamento de descrições).
Antes de criar: scan de novelty, Regra de 3, probes de regressão.
Playbook: ~/.hermes/skills/compound-skills/SKILL.md
Script:   compound.py (status, scan, probe-run, sanitize, protect)
Um motor só. Não criar primos (self-improve, evolution, harvest).
```

## Regras específicas de agente 24/7

1. **O motor mora onde mora o skills root real.** Se você tem agente em VPS
   (primário) e agente desktop (backup), instale o motor no que gerencia as
   skills de verdade. Dois motores em dois hosts derivam — mesmo problema de
   colar o bloco portátil E instalar a pasta.
2. **Ciclo nunca roda autônomo.** Agente 24/7 com gatilho automático de
   auto-evolução é exatamente o anti-padrão que a ativação manual existe para
   impedir. `/evoluir` vem do dono, por mensagem, nunca de cron.
3. **Guarda de custo vale dobrado.** Qualquer automação do agente que invoque
   LLM segue o guardrail do motor: prefixo de guarda, teto horário/diário,
   circuit breaker, modelo barato. Um loop de auto-melhoria sem teto em VPS é
   uma fatura, não um recurso.
4. **Skills que exigem OAuth interativo, 2FA ou filesystem local** ficam no
   agente desktop, nunca no VPS. O motor respeita essa fronteira: `protect add`
   nelas e edite só com o dono presente.

## Ledger

O agente tem filesystem, então o ledger padrão (`~/.compound-skills/ledger.md`)
funciona integralmente — backup, diff, rollback e sanitize inclusos. Não use a
memória conversacional do agente como ledger: memória guarda fato, não
procedimento, e resume sem avisar.
