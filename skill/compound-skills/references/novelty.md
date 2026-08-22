# Rubrica de novelty %

Nunca decida entre aprofundar e criar por sensaÃ§Ã£o. MeÃ§a, registre o nÃºmero, e
deixe o nÃºmero decidir.

## 1. Scan obrigatÃ³rio antes de qualquer criaÃ§Ã£o

Liste os candidatos nesta ordem:

1. Ãndice do host (`CLAUDE.md`, `AGENTS.md`, instructions, tabela de rules)
2. Pastas de skills do usuÃ¡rio e do projeto
3. Ãšltimas entradas do ledger
4. MemÃ³rias / knowledge que atuem como playbook de fato

Para cada candidato prÃ³ximo, anote trÃªs coisas: *objetivo*, *mecanismo*, *gatilhos*.
Ignore stubs â€” arquivos que sÃ³ apontam para outro motor nÃ£o sÃ£o candidatos.

Nenhum candidato â†’ novelty 100%. Mesmo assim a Regra de 3, a cota e o orÃ§amento
continuam valendo. AusÃªncia de primo nÃ£o Ã© licenÃ§a.

## 2. Os trÃªs eixos

```
overlap% = goal(0-40) + mechanism(0-30) + triggers(0-30)
novelty% = 100 - overlap%
```

| Eixo | 0 | Meio | Cheio |
|---|---|---|---|
| **Goal** (0â€“40) | Outro problem | Mesma famÃ­lia, outro recorte | O **mesmo** job |
| **Mechanism** (0â€“30) | Outra operaÃ§Ã£o | Mesmos passos, outro nome | O **mesmo** pipeline |
| **Triggers** (0â€“30) | Outro vocabulÃ¡rio e domÃ­nio | InterseÃ§Ã£o parcial | Os **mesmos** gatilhos |

O eixo de triggers Ã© calculado pelo script, mecanicamente, por sobreposiÃ§Ã£o lexical
contra todas as descriÃ§Ãµes instaladas. Os dois primeiros eixos exigem julgamento â€” e Ã©
por isso que o script obriga vocÃª a declarÃ¡-los em vez de inventar um nÃºmero final.

**ViÃ©s[X™\˜YÎŠŠˆÈØÛÜ™HYXğèXÛÈ\ØHXZ\È
˜ÛÛZ[›Y[
ˆ
]X[ÈHÚÚ[›İ˜Bš°èH\İ0èHÛØ™\È[H^\İ[JHÈ]YHÚ[Z[\šYYHÚ[pê]šXØKˆH\™İ[HÙ\H0êBˆ˜\ÜÛÈ°èH^\İOÈ‹°èÛÈ™[\ÈğèÛÈ\™XÚY\ÏÈ‹‚‚ˆÈÈËˆXÚ\ğèÛÂ‚Ÿ›İ™[HpéğèÛÈ›ÛYHH[YØHŸKK_KK_KK_KK_Ÿ8 $ÌÌ	H
ŠP”ÓÔŠŠˆX[0ê[H]Úpë[š[[ÈŸÌx $ÍÌ	H
Š•TÔQJŠˆX[0ê[H™\œğèÛÈ›Ø\İNÈXœÛÜ™HÛÛ˜ÙZ]ÜÈ
Š™JŠˆ\™Y˜\ÈŸÌx $ÌL	H
Š”ÕTT”ÑQJŠˆ›İ›ÈİXˆHH[š\ÎÈ0ë[™XÙH™]\™Ù]YÈ‚ÛÛ\[Y[ÜÎ‚‚‹H›İ™[H8¢bH™[š[HØ\ÛÈH›Ü™H›İ›È8¡¤ˆ
Š”ÒÒT
Š‹ˆÚÚ\0êHÈ™\İ[YÈÛÜœ™]È˜BˆXZ[ÜšXHÜÈÚXÛÜËH°èÛÈ0êHœ˜XØ\ÜÛÎˆ0êHÈ[İÜˆ[˜Ú[Û˜[™Ë‚‹H°è\šX\ÈÚÚ[È\˜ÚXZ\ÈÛØœ™[HÈ›Øˆ8¡¤ˆTÔQHHXZ\È›ÜKİXˆ˜\Èİ]˜\Ë‚‹HZ[Z[œÈH]Y›Ü›XH8¡¤ˆğìÈP”ÓÔ‹ÕTÔQH[›È[\Ëˆ[˜ØHİ\\œÙYK‚‚ˆÈÈˆXœÛÜ™\ˆH™\™YB‚“[šØ\ˆ°èÛÈ0êHXœÛÜ™\‹ˆ[İ˜HÈ˜[Ü‚‚ŒKˆÛÜYH™YÜ˜\È\˜\Ë\ÜÛÜË]˜[ÈHÚXÚÛ\İÈ]YHZ[™H˜[[BŒ‹ˆ[™H\È\™Y˜\È8 %È›İHH[YØH\ÜØHHÙ\ˆH™[˜ÙYÜ˜BŒËˆ]X[^™HÜÈØ][ÜÈH™[˜ÙYÜ˜H\˜H[˜ÛZ\ˆÜÈH[YØBˆ[HÕTT”ÑQNˆİXˆ˜H[YØH
È™]\™Ù]È0ë[™XÙHÈÜİKˆ™YÚ\İ™HH
Šœ›ØÙY0ê›˜ÚXJŠˆ›ÈÛÛ[Z]
KXXœÛÜ™]X
K\˜HH[šYÙ[HšXØ\ˆ]Y]0è]™[‹ˆ›ÙHÜÈ›Ø™\È\È
Š™X\ÊŠˆÚÚ[ÈÛÛ˜HH™[˜ÙYÜ˜B‚“È\ÜÛÈˆ0êHÈ]YHÙ\\˜HXœÛÜ°éğèÛÈH[\]péğèÛËˆÙHÜÈ›Ø™\ÈH[YØH°èÛÈ\ÜØ[H˜B››İ˜K›Øğêˆ°èÛÈXœÛÜ™]H8 %›Øğêˆ\™]HØ\XÚYYHH°èÛÈ\˜ÙX™]K‚‚ˆÈÈKˆÛØœ™HÈ›ÛYH[\ÜİÈ[ÈÛ›Â‚”ÙHÈÛ›È[\0íYH[H›ÛYHÙšXÚX[HÈ°î›Y\›È^ˆTÔQK0èH[HÛÛ™›]È™X[[™B˜ÛÛ˜]ÈHYYYKˆ™\ÛÛ˜H\ÜÚ[KH
Š™Øİ[Y[JŠ‚‚‹H›ÛYH0êHÛÛ˜]ÈÙšXÚX[È[İÜˆ8¡¤ˆÕTT”ÑQKÛÛHÈ°î›Y\›È™YÚ\İ˜YÈÈYÂ‹HğìÈ™Y™\°ê›˜ÚXHH›ÛYK›İ™[H8¢iÌ	H8¡¤ˆTÔQH›ÈYØ\ˆ˜]\˜[
È[X\Â‚“È]YH[˜ØH0êHXÙZ]0è]™[0êH[™›\ˆÈ°î›Y\›È\˜H\İYšXØ\ˆH\İH›İ˜KˆÙHÈ°î›Y\›Â™\ÜÙHŒ‰HH›Øğêˆ\ØÜ™]™]HÎ	KÈ[İÜˆš\›İHX]›Ë‚‚ˆÈÈ‹ˆ[K\Y°íY\Â‚‹H˜\ØÙ\ˆ›ÛË]Œ˜Ù[HİX˜\ˆ›ÛØ‹H•™Z˜H[X°ê[H›ÛÈˆÛÛH›ÛÈš]›ÈHÛÛ\]È8 %Ú\È[İÜ™\È\š]˜[B‹Hİ\\™\İ[X\ˆ›İšYYH\˜H\İYšXØ\ˆ\İH›İ˜B‹Hİ\\œÙYH[HZ[Z[ˆÈÜİ‹H[™[\ˆ	HÙ[H›ÛYX\ˆÈš[[ÈXZ\È°ìŞ[[Â‹H™YÚ\İ˜\ˆÈ°î›Y\›ÈÙ[H™YÚ\İ˜\ˆÜÈ°êœÈZ^ÜÈ]YHÈÛÛ\\Ù\˜[B