---
name: ig-humano
description: >-
  Tira de um texto o que soa a IA (travessões, vocabulário de máquina, gerúndio,
  caracteres invisíveis, hashtags, saudações) e dá-lhe uma nota de 0 a 100 em
  cinco testes, em PT-PT e na voz da Tânia Silveira. Usar sempre que um texto
  tem de soar humano, quando a Tânia diz "humaniza", "isto soa a IA", "limpa
  isto", e antes de mostrar qualquer legenda, guião, comentário ou DM.
---

# ig-humano

Antes de escrever, carrega a skill `tania-brand-context` e lê `references/tom-de-voz.md`.

Há duas ferramentas nesta pasta e funcionam mesmo. Usa-as em vez de avaliar a olho.

```bash
python3 humanize.py rascunho.txt --report -o limpo.txt   # limpa e diz o que mudou
python3 detect.py rascunho.txt limpo.txt                  # nota antes e depois
```

As duas leem `slop.json`. É o léxico da Tânia: as palavras proibidas dela, o
vocabulário típico de IA em português, os vícios do Instagram e os padrões de
estrutura. Se ela usa uma palavra que o ficheiro corta, tira-a do ficheiro.

## O que é limpo automaticamente

1. **Caracteres invisíveis.** Os que o teclado não produz e que vêm agarrados
   ao texto copiado.
2. **Tipografia.** O travessão a meio da frase passa a vírgula. **Exceção:** o
   travessão no início da linha fica, porque é assim que a Tânia escreve o CTA
   na legenda ("— Se queres…").
3. **Léxico.** "crucial", "potencializar", "jornada", "incrível", "no mundo
   atual", "hoje quero partilhar", "negociozinho"… Cada palavra é trocada por
   uma simples ou apagada.

## O que é só assinalado (reescreves tu)

O gerúndio, "não é só X, é Y", "não só… mas também", a pergunta encenada
numa linha ("O resultado?"), as tríades, os emojis 🚀🔥💡✨🎯💪, as hashtags,
a saudação a abrir, "você/vocês", as exclamações a mais, os diminutivos e as
palavras em maiúsculas seguidas.

Reescreve cada linha assinalada à mão, sem mudar o sentido, e volta a correr
`detect.py`. É isto que leva a nota de REVIEW a PASS.

## Os cinco testes (0–100, mais alto = mais humano)

| teste | o que mede |
| --- | --- |
| BURSTINESS | se o tamanho das frases varia (a máquina escreve tudo igual) |
| SPECIFICITY | números, nomes e lugares por cada 100 palavras |
| SLOP DENSITY | palavras do léxico por cada 100 palavras |
| FINGERPRINT | invisíveis, travessões a meio da frase, aspas curvas |
| VOICE | tu/eu por cada 100 palavras e vícios de estrutura |

PASS = nota geral ≥ 70 e nenhum teste abaixo de 55.

## Diz isto com honestidade

São regras locais e nada é enviado para fora. **Não** são o GPTZero nem outro
detetor e não garantem o veredito deles. Nunca digas à Tânia que um texto é
"indetetável".

## Ordem

1. `humanize.py` → 2. reescreve o que foi assinalado → 3. `detect.py` antes/depois
→ 4. se não passou, corrige o teste mais fraco (duas voltas é normal; cinco
voltas significa que o rascunho é para deitar fora) → 5. mostra o texto limpo
e a nota, nunca só a nota.
