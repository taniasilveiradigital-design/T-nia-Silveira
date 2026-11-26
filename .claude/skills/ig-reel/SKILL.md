---
name: ig-reel
description: >-
  Escreve um Reel para a Tânia Silveira a partir de uma ideia: três ganchos
  avaliados, o guião falado, o texto no ecrã e os tempos de cada parte, em
  PT-PT e na voz dela. Usar quando a Tânia pede um Reel, um guião, um gancho,
  "faz um reel sobre X", "o que digo neste vídeo", ou vai gravar e não tem a
  primeira frase.
---

# ig-reel

## Antes de escrever

1. Carrega a skill `tania-brand-context`: `references/tom-de-voz.md`,
   `references/conteudos.md` e `references/clientes-e-provas.md`.
2. Lê `skills/tania-brand-context/references/ganchos-e-reels-sarah.md` neste
   repositório. **Essas regras mandam sobre tudo o que está aqui.**
3. Lê os textos dos outros dias da mesma semana e da semana anterior (pasta
   `copies/`) para não repetires o tema nem o ângulo.
4. Se a ideia é fraca, não enchas. Faz uma pergunta só: o que aconteceu, a quem
   e quanto custou ou rendeu. Um Reel precisa de uma coisa concreta e verdadeira.

## 1. Três ganchos, de fórmulas diferentes

Cada gancho tem uma versão falada e uma versão para o ecrã (no máximo 6 palavras).
Dá a cada um nota de 0 a 3 em cada um dos 4 critérios da Sarah, num total de 12:

| critério | pergunta |
| --- | --- |
| Identificação | a dona da marca reconhece-se logo? |
| Tensão | há perda, risco ou contradição? |
| Especificidade | há um momento ou detalhe concreto? |
| Curiosidade | fica uma pergunta por responder? |

Mostra a tabela. Abaixo de 8/12 ainda não há gancho, recomeça. Recusa sempre:
uma saudação, "neste vídeo…", um número sozinho a abrir, a história a abrir,
"para de fazer scroll".

## 2. O guião

- **Reel que ensina** (pilares 1, 2 e 3): segue a estrutura de 9 passos da Sarah,
  até 1:30 (cerca de 200 palavras). Fala como numa reunião com a cliente.
  **Sem listas e sem "primeiro, segundo":** as decisões ligam-se umas às outras.
- **Reel de opinião ou de bastidores:** 30 a 45 segundos, uma ideia só.
- Uma ideia por linha, porque cada linha é um corte na edição.
- Números em vez de adjetivos. Se faltar um número, deixa `{{o teu número}}` e
  assinala-o. **Nunca inventes clientes, números nem resultados.**

## 3. Tempos

Põe o guião num ficheiro, uma linha por parte, e corre:

```bash
python3 beats.py guiao.txt --target 75
```

Usa 150 palavras por minuto por defeito. Se a Tânia já se cronometrou, usa `--wpm`.
Corrige o que for assinalado: um gancho com mais de 3 segundos, ou uma parte
com mais de 4 segundos sem mudar o que está no ecrã.

## 4. Humaniza

Passa o guião pela `ig-humano` antes de o mostrar.

## 5. Entrega

O guião num bloco, o texto do ecrã numa lista separada com os tempos, e:

```
REEL PRONTO
gancho:     "…"  11/12
tamanho:    1:12, 14 partes
ecrã:       6 cartões
humano:     84 PASS
legenda:    corre /ig-legenda a seguir
```

**Texto no ecrã:** no máximo 6 palavras por cartão, o gancho aparece logo no
primeiro frame, legendas na parte falada (a maioria vê sem som). Fica longe do
fundo do ecrã e da margem direita, onde estão a legenda e os botões.

Esta skill só escreve. A Tânia grava e publica.
