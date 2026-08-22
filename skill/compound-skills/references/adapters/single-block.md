# Adapter — hosts de bloco único (ChatGPT, Gemini, custom instructions)

Hosts que não leem pastas recebem o motor completo em um bloco: use
`portable/PASTE-ANY-AI.md`, colado em Custom Instructions / System Prompt /
Gem Knowledge.

## Limitações honestas neste modo

| Recurso | Funciona? |
|---|---|
| Triagem de 6 destinos | sim |
| Score de novelty | sim, mas os três eixos são todos por julgamento — sem o cálculo mecânico de gatilho |
| Regra de 3, cota, revisão 90 dias | sim, se o ledger for persistente |
| Probes de regressão | **parcial** — sem script, a checagem é por leitura |
| Backup / diff / rollback | **não** — sem filesystem não há rede de segurança |
| Orçamento de contexto | **manual** — conte os caracteres você mesmo |
| Sanitizador de segredos | **não** |

Onde não há rollback, a mitigação é procedimental: **antes de editar qualquer
playbook, cole a versão atual inteira numa mensagem do chat.** Fica sendo o backup.
Feio, mas funciona, e é infinitamente melhor que nada.

## Ledger sem filesystem

Precisa de um lugar **persistente e editável**: um documento fixo, um canvas, uma
nota. Memória do host **não serve** — memória guarda fato, não procedimento, e
resume sem avisar.

Sem ledger persistente, o efeito composto simplesmente não existe: cada sessão
recomeça e o motor vira decoração.
