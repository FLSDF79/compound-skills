# Os 6 destinos, com casos resolvidos

A dúvida quase sempre é entre 3, 5 e 6. Os casos abaixo são reais.

## Os três erros mais frequentes

### Erro 1 — skill que devia ser script

**Padrão:** "Toda vez que empacoto uma skill, rodo validate, depois package, depois
copio para outputs."

- Tentação: skill `empacotador`.
- **Destino correto: 3.** Três comandos em ordem fixa, nenhuma decisão muda conforme
  o contexto. Um `.sh` de seis linhas resolve, com custo zero de contexto permanente.

### Erro 2 — skill que devia ser linha no índice

**Padrão:** "Sempre que criar skill, quero as duas versões: padrão e portátil."

- **Destino correto: 2.** É preferência permanente de saída, não método. Cabe em uma
  linha e vale para todo contexto sem precisar de gatilho.

### Erro 3 — skill criada na primeira ocorrência

**Padrão:** "Esse jeito de estruturar a resposta ficou excelente."

- **Destino correto: 4.** Uma execução boa é resultado, não padrão. A Regra de 3
  existe para filtrar entusiasmo. Se o método for bom mesmo, ele reaparece.
- Este é o erro mais caro porque *parece* produtividade.

## Destino 5 vs 6

### Caso A — aprofundar (5)

**Padrão:** "Descobri um jeito melhor de tratar links de LinkedIn na análise de vídeo."

- Já existe skill cobrindo "análise de vídeo de qualquer fonte". LinkedIn é caso de
  borda **dentro** do domínio, não domínio novo.
- Skill nova aqui criaria colisão imediata: as duas disparariam no mesmo link.
- Score típico: goal 40, mech 26, trig ~24 → novelty ≈ 10% → **ABSORB**.

### Caso B — criar (6), e passou nos quatro portões

**Padrão:** "Preparar cartões de contexto para conversa ao vivo em óculos, com limite
duro de 5.000 caracteres e formato de cue."

- Domínio genuinamente novo: hardware específico, restrição técnica dura, formato de
  saída sem paralelo no ecossistema.
- Score: goal 6, mech 8, trig ~5 → novelty ≈ 81% → **SUPERSEDE/criar**.

### Caso C — fundir, não coexistir

**Padrão:** duas skills disputando "organizar minhas notas".

- A saída correta **não** é ajustar as descrições para conviverem. Descrição ajustada
  volta a colidir na próxima edição — é remendo, não conserto.
- **Funda o domínio numa skill e stube a outra.**
- Precedente real: duas skills irmãs viraram uma fundida, e as duas antigas foram
  arquivadas. Deu certo, e o ecossistema ficou menor e mais capaz.

## Destino 1 — descartar

**Caso D:** "Aquele prompt específico que resolveu o relatório do dia 12."
Contexto irrepetível. O valor estava no resultado, que já foi entregue.

**Caso E:** "A forma como reescrevi aquele parágrafo ficou boa."
Qualidade pontual de escrita raramente é padrão reutilizável — é julgamento aplicado
ao caso.

## Destino 2 — regra no índice

**Caso F:** "Nunca quero automação chamando LLM sem prefixo de guarda, teto horário e
circuit breaker."
Vale em todo canal, não tem gatilho, vale sempre. Uma linha, não uma skill.

## Destino 3 — implementação direta

**Caso G:** "Preciso monitorar consumo semanalmente."
Virou três scripts e um agendador. Nenhuma skill envolvida, custo zero de contexto,
e roda sozinho.

Lição: **automação recorrente é infraestrutura, não skill.** Skill é o que precisa de
julgamento no momento de usar.

## Destino 4 — ledger

**Caso H:** "Esse jeito de cruzar duas notas semanticamente distantes parece
poderoso."
Registrar na primeira vez. Se aparecer em três contextos distintos — pesquisa, aula,
ideação — aí sobe.

## Fronteira difícil

**Caso I — padrão bom, cota esgotada.** Três ocorrências, sem colisão, mas já houve
skill nova no mês.

- **Destino: 4**, marcado como prioridade do mês seguinte.
- Não é conflito de regras. Padrão bom sobrevive a trinta dias, e a espera é um teste
  a mais.
- Nunca peça exceção de cota. O teto existe justamente para os casos em que incomoda.

**Caso J — padrão bom, orçamento de contexto estourado.** Aqui a decisão é mais dura:
alguma skill precisa **sair** para esta entrar. Se nenhuma merece sair, esta não
merece entrar. Largura é soma zero, e essa é a conversa honesta que a maioria dos
sistemas evita ter.
