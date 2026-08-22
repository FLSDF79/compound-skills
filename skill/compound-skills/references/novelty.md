# Rubrica de novelty %

Nunca decida entre aprofundar e criar por sensação. Meça, registre o número, e
deixe o número decidir.

## 1. Scan obrigatório antes de qualquer criação

Liste os candidatos nesta ordem:

1. Índice do host (`CLAUDE.md`, `AGENTS.md`, instructions, tabela de rules)
2. Pastas de skills do usuário e do projeto
3. Últimas entradas do ledger
4. Memórias / knowledge que atuem como playbook de fato

Para cada candidato próximo, anote três coisas: *objetivo*, *mecanismo*, *gatilhos*.
Ignore stubs — arquivos que só apontam para outro motor não são candidatos.

Nenhum candidato → novelty 100%. Mesmo assim a Regra de 3, a cota e o orçamento
continuam valendo. Ausência de primo não é licença.

## 2. Os três eixos

```
overlap% = goal(0-40) + mechanism(0-30) + triggers(0-30)
novelty% = 100 - overlap%
```

| Eixo | 0 | Meio | Cheio |
|---|---|---|---|
| **Goal** (0–40) | Outro problema | Mesma família, outro recorte | O **mesmo** job |
| **Mechanism** (0–30) | Outra operação | Mesmos passos, outro nome | O **mesmo** pipeline |
| **Triggers** (0–30) | Outro vocabulário e domínio | Interseção parcial | Os **mesmos** gatilhos |

O eixo de triggers é calculado pelo script, mecanicamente, por sobreposição lexical
contra todas as descrições instaladas. Os dois primeiros exigem julgamento — e é
por isso que o script obriga você a declará-los em vez de inventar um número final.

**Viés deliberado:** o score mecânico pesa mais *containment* (quanto da skill nova
já está coberto pela existente) do que similaridade simétrica. A pergunta certa é
"isso já existe?", não "elas são parecidas?".

## 3. Decisão

| Novelty | Ação | Nome | A antiga |
|---|---|---|---|
| 0–30% | **ABSORB** | mantém | patch mínimo |
| 31–70% | **UPGRADE** | mantém | versão robusta; absorve conceitos **e** tarefas |
| 71–100% | **SUPERSEDE** | novo | stub de 5 linhas; índice retargetado |

Complementos:

- Novelty ≈ 0 e nenhum caso de borda novo → **SKIP**. Skip é o resultado correto na
  maioria dos ciclos, e não é fracasso: é o motor funcionando.
- Várias skills parciais cobrem o job → UPGRADE a mais forte, stub nas outras.
- Built-ins da plataforma → só ABSORB/UPGRADE dentro deles. Nunca supersede.

## 4. Absorver de verdade

Linkar não é absorver. Mova o valor:

1. Copie regras duras, passos, pitfalls e checklists que ainda valem
2. Funda as tarefas — o ritual da antiga passa a ser da vencedora
3. Atualize os gatilhos da vencedora para incluir os da antiga
4. Em SUPERSEDE: stub na antiga + retarget do índice do host
5. Registre a **procedência** no commit (`--absorveu`), para a linhagem ficar auditável
6. Rode os probes das **duas** skills contra a vencedora

O passo 6 é o que separa absorção de amputação. Se os probes da antiga não passam na
nova, você não absorveu — você perdeu capacidade e não percebeu.

## 5. Sobre o nome imposto pelo dono

Se o dono impõe um nome oficial e o número diz UPGRADE, há um conflito real entre
contrato e medida. Resolva assim, e **documente**:

- Nome é contrato oficial do motor → SUPERSEDE, com o número registrado do lado
- Só preferência de nome, novelty ≤ 70% → UPGRADE no lugar natural + alias

O que nunca é aceitável é inflar o número para justificar a pasta nova. Se o número
disse 22% e você escreveu 78%, o motor virou teatro.

## 6. Anti-padrões

- Nascer `foo-v2` sem stubar `foo`
- "Veja também foo" com foo vivo e completo — dois motores derivam
- Superestimar novidade para justificar pasta nova
- Supersede em built-in do host
- Inventar % sem nomear o primo mais próximo
- Registrar o número sem registrar os três eixos que o compuseram
