# Adapter — Cursor, Codex e agentes de repositório

## Cursor

Uma rule com `alwaysApply: false` (o motor é manual, não ambiental):

```
.cursor/rules/compound-skills.mdc
```

Aponte para o playbook em vez de colar o conteúdo. Rule que cola o motor inteiro
paga o custo em toda requisição.

## Agentes de repositório (AGENTS.md)

O motor entra como seção curta com ponteiro. Playbooks colhidos vivem em
`.agent/playbooks/`, nunca em `docs/` — pastas de documentação não são abertas pelo
próximo turno.

## Especificidade deste host: o repositório é compartilhado

Aqui o motor sai do domínio pessoal e entra em terreno de equipe. Duas regras extras:

1. **Alteração de playbook vai por pull request**, não por commit direto. O portão de
   auditoria externa vira o review — e isso é uma melhoria, não um atrito
2. **A cota é do repositório, não da pessoa.** Cinco pessoas com cota individual de
   uma skill/mês produzem sessenta skills/ano, que é exatamente o resultado que o
   teto existe para impedir
