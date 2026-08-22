# N caminhos — não trave no primeiro que funcionou

O motor não existe para memorizar o que foi feito. Existe para subir o piso **e**
manter o espaço de opções vivo. São coisas diferentes, e a segunda é a que quase
todo sistema de "aprendizado composto" perde.

O risco de um motor que só registra o vencedor: a primeira solução que funcionou vira
a única solução conhecida. O ecossistema fica mais rápido e mais burro ao mesmo
tempo — ótimo local, com confiança crescente.

## O passe (5 minutos, depois de entregar)

1. **Nomeie o objetivo** em uma linha — o objetivo, não a implementação
2. **Nomeie o mecanismo entregue** e por que ganhou *desta vez*
3. **Invente 2–3 alternativas** no mesmo objetivo, mudando **um eixo** por
   alternativa: modelo de dados, runtime, UX, algoritmo, forma de verificação
4. Para cada: *quando ganha*, *custo*, *critério de morte*
5. Grave o mapa dentro da skill
6. **Não implemente** as alternativas, salvo se o entregue estiver errado

Se você não consegue nomear um **modo de falha diferente**, não é um caminho
diferente — é a mesma coisa com outro nome.

## Template

```markdown
## N caminhos (objetivo: <uma linha>)

| # | Mecanismo | Quando ganha | Custo | Matar se |
|---|---|---|---|---|
| **Entregue** | … | … | … | … |
| B | … | … | … | … |
| C | … | … | … | … |
```

Três linhas bastam. Cinco é teto.

## Por que isto favorece crescimento contínuo em profundidade

Adicionar uma linha ao mapa de N caminhos não amplia a **descrição de gatilho**:
o mapa vive no corpo da skill, carregado quando ela dispara. Esse corpo ainda
consome contexto e permanece limitado pelo host.
A descrição — a parte permanente presente no índice de skills — não muda.

Então: a largura tem teto porque cada skill nova adiciona custo permanente. A
profundidade pode crescer sem ampliar essa superfície de gatilho, embora o corpo
ainda custe contexto quando carregado.

É por isso que o crescimento saudável é **para dentro**. A cada ciclo, as mesmas
doze skills carregam mais alternativas mapeadas, mais pitfalls reais, mais critérios
de morte. Depois de dois anos, isso é um ativo denso. A alternativa — sessenta skills
rasas — é um passivo que ninguém consegue auditar.

## Disciplina

- Alternativas têm que ser legais no host: sem violar safety, segredos ou contrato
  de plataforma
- Se só existe um mecanismo legal, escreva `N=1 — o contrato força este caminho`.
  Honestidade vale mais que opção falsa
- O próximo ciclo no mesmo objetivo **atualiza** o mapa. Essa atualização é a subida
- Alternativa que já foi tentada e falhou não fica no mapa: vai para o anti-ledger,
  com o motivo. O mapa guarda opções vivas; o anti-ledger guarda portas fechadas
