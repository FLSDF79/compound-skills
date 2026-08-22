# Os 6 destinos, com casos resolvidos

A dÃºvida quase sempre Ã© entre 3, 5 e 6. Os casos abaixo sÃ£o reais.

## Os trÃªs erros mais frequentes

### Erro 1 â€” skill que devia ser script

**PadrÃ£o:** "Toda vez que empacoto uma skill, rodo validate, depois package, depois
copio para outputs."

- TentaÃ§Ã£o: skill `empacotador`.
- **Destino correto: 3.** TrÃªs comandos em ordem fixa, nenhuma decisÃ£o muda conforme
  o contexto. Um `.sh` de seis linhas resolve, com custo zero de contexto permanente.

### Erro 2 â€” skill que devia ser linha no Ã­ndice

**PadrÃ£o:** "Sempre que criar skill, quero as duas versÃµes: padrÃ£o e portÃ¡til."

- **Destino correto: 2.** Ã‰ preferÃªncia permanente de saÃ­da, nÃ£o mÃ©todo. Cabe em uma
  linha e vale para todo contexto sem precisar de gatilho.

### Erro 3 â€” skill criada na primeira ocorrÃªncia

**PadrÃ£o:** "Esse jeito de estruturar a resposta ficou excelente."

- **Destino correto: 4.** Uma execuÃ§Ã£o boa Ã© resultado, nÃ£o padrÃ£o. A Regra de 3
  existe para filtrar entusiasmo. Se o mÃ©todo for bom mesmo, ele reaparece.
- Este Ã© o erro mais caro porque *parece* produtividade.

## Destino 5 vs 6

### Caso A â€” aprofundar (5)

**PadrÃ£o:** "Descobri um jeito melhor de tratar links de LinkedIn na anÃ¡lise de vÃ­deo."

- JÃ¡ existe skill cobrindo "anÃ¡lise de vÃ­deo de qualquer fonte". LinkedIn Ã© caso de
  borda **dentro** do domÃ­nio, nÃ£o domÃ­nio novo.
- Skill nova aqui criaria colisÃ£o imediata: as duas disparariam no mesmo link.
- Score tÃ­pico: goal 40, mech 26, trig ~24 â†’ novelty â‰ˆ 10% â†’ **ABSORB**.

### Caso B â€” criar (6), e passou nos quatro portÃµes

**PadrÃ£o:** "Preparar cartÃµes de contexto para conversa ao vivo em Ã³culos, com limite
duro de 5.000 caracteres e formato de cue."

- DomÃ­nio genuinamente novo: hardware especÃ­fico, restriÃ§Ã£o tÃ©cnica dura, formato de
  saÃ­da sem paralelo no ecossistema.
- Score: goal 6, mech 8, trig ~5 â†’ novelty â‰ˆ 81% â†’ **SUPERSEDE/criar**.

### Caso C â€” fundir, nÃ£o coexistir

**PadrÃ£o:** duas skills disputando "organizar minhas notas".

- A saÃ­da correta **nÃ£o* Ã© ajustar as descriÃ§Ãµes para conviverem. DescriÃ§Ã£o ajustada
  volta a colidir na prÃ³xima edigÃ£o â€” Ã© remendo, nÃ£o conserto.
- **Funda o domÃ­nio numa skill e stube a outra.**
- Precedente real: duas skills irmÃ¡s viraram uma fundida, e as duas antigas foram
  arquivadas. Deu certo, e o ecossistema ficou menor e mais capaz.

## Destino 1 â€” Descartar

**Caso D:** "Aquele prompt especÃ­fico que resolveu o relatÃ³rio do dia 12."
Contexto irrepetÃ­vel. O valor estava no resultado, que jÃ¡ foi entregue.

**Caso E:** "A forma como reescrevi aquele parÃ¡grafo ficou boa."
Qualidade pontual de escrita raramente Ã© padrÃ£o reutilizÃ¡vel â€” sim julgamento aplicado
ao caso.

## Destino 2 â€” Regra no Ã­ndice

**Caso F:** "Nunca quero automaÃ§Ã£o chamando LLM sem prefixo de guarda, teto horÃ¡rio e
circuit breaker."
Vale em todo canal, nÃ£o tem gatilho, vale sempre. Uma linha, nÃ£o uma skill.

## Destino 3 â€” ImplementaÃ§Ã£o direta

**Caso G:** "Preciso monitorar consumo semanalmente."
Virou trÃªs scripts e um agendador. Nenhuma skill envolvida, custo zero de contexto,
e roda sozinho.

LiÃ§Ã£o : **automaÃ§Ã£o recorrente Ã© infraestrutura, nÃ£o skill.** Skill Ã© o que precisa de
julgamento no momento de usar.

## Destino 4 â€” Ledger

**Caso H:** "Esse jeito de cruzar duas notas semanticamente distantes parece
poderoso."
Registrar na primeira vez. Se aparecer em trÃªs contextos distintos â€” pesquisa, aula,
ideaÃ§Ã£o â€” aÃ­ sobe.

## Fronteira difÃ­cil

**Caso I â€” PadrÃ£o bom, cota esgotada.** TrÃªs ocorrÃªncias, sem colisÃ£o, mas ¨«„¡½ÕÙ”)Í­¥±°¹½Ù„¹¼·©Ì¸((´€¨©•ÍÑ¥¹¼è€Ğ¨¨°µ…É…‘¼½µ¼ÁÉ¥½É¥‘…‘”‘¼·©ÌÍ•Õ¥¹Ñ”¸(´;¼ƒ¤½¹™±¥Ñ¼‘”É•É…Ì¸A…‘Ë¼‰½´Í½‰É•Ù¥Ù”„ÑÉ¥¹Ñ„‘¥…Ì°”„•ÍÁ•É„ƒ¤Õ´Ñ•ÍÑ”(€„µ…¥Ì¸(´9Õ¹„Á—„•á—Ÿ¼‘”½Ñ„¸<Ñ•Ñ¼•á¥ÍÑ”©ÕÍÑ…µ•¹Ñ”Á…É„½Ì…Í½Ì•´ÅÕ”¥¹½µ½‘„¸((¨©…Í¼(ƒŠPA…‘Ë¼‰½´°½Ë…µ•¹Ñ¼‘”½¹Ñ•áÑ¼•ÍÑ½ÕÉ…‘¼¸¨¨ÅÕ¤„‘•¥Ï¼ƒ¤µ…¥Ì‘ÕÉ„è)…±Õµ„Í­¥±°ÁÉ•¥Í„€¨©Í…¥È¨¨Á…É„•ÍÑ„•¹ÑÉ…È¸M”¹•¹¡Õµ„µ•É•”Í…¥È°•ÍÑ„»¼)µ•É•”•¹ÑÉ…È¸1…ÉÕÉ„ƒ¤Í½µ„é•É¼°”•ÍÍ„ƒ¤„½¹Ù•ÉÍ„¡½¹•ÍÑ„ÅÕ”„µ…¥½É¥„‘½Ì)Í¥ÍÑ•µ…Ì•Ù¥Ñ„Ñ•È¸(