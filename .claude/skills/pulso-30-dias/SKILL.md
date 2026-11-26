---
name: pulso-30-dias
description: >-
  Pesquisa o que se disse nos últimos 30 dias sobre uma marca, uma pessoa, um
  concorrente ou um tema de moda e entrega um resumo curto com fontes e
  ângulos de conteúdo, em PT-PT. Usar quando a Tânia diz "o que se diz sobre
  X", "pesquisa esta marca antes da reunião", "o que está a acontecer em X",
  "últimos 30 dias", ou antes de um Diagnóstico ou de uma sessão Tafetá 360.
---

# pulso-30-dias

Versão leve de um motor de pesquisa americano: sem chaves pagas, sem cookies
do browser, só pesquisa na web.

## Para que serve (exemplos)

- Antes de uma reunião com uma cliente: o que a marca fez este mês (coleção
  nova, campanha, saldos, imprensa, queixas).
- O Fio da Semana: o que uma marca ou uma loja anda a fazer.
- O mercado: o que se diz de um tema (produção nacional, Shein, prazos, tecidos).

## Como pesquisar

1. Usa `WebSearch` (modo "extended" quando precisas de coisas recentes) com o
   tema + o mês e o ano atuais. Faz várias pesquisas de uma vez: em português,
   em inglês se a marca for internacional, e "site:" para fontes específicas.
2. Fontes que contam para moda em Portugal: o site da marca, o Instagram e o
   TikTok da marca (o que aparece na pesquisa), imprensa (ECO, Expresso,
   Público, Jornal de Negócios, Dinheiro Vivo, Portugal Têxtil, Jornal Têxtil,
   Fashion Network, BoF, Vogue PT, NiT), Reddit e fóruns, avaliações (Trustpilot,
   Portal da Queixa), anúncios ativos (Biblioteca de Anúncios da Meta), vagas
   de emprego (dizem para onde a marca vai crescer).
3. Abre as páginas que importam com o agente `web-fetch`. Não te fiques pelos
   resumos.
4. **Só conta o que tem data nos últimos 30 dias.** O que for mais antigo vai
   para um bloco à parte, "contexto".

## Entrega

```
PULSO: {tema}, {data} a {data}

O QUE ACONTECEU (3 a 6 pontos, cada um com data e fonte)
O QUE AS PESSOAS DIZEM (citações curtas, com a fonte)
O QUE ISTO SIGNIFICA (a leitura da Tânia: produto, margem, posicionamento, decisão)
ÂNGULOS DE CONTEÚDO (2 a 3, prontos para /ig-reel ou /ig-plano)
FONTES (lista com links)
```

## Regras

- **Nunca inventes.** Se não encontraste, diz "não encontrei nada de X nos
  últimos 30 dias" e diz onde procuraste.
- Separa o facto (com fonte) da leitura (opinião da Tânia).
- Não entres em contas, não uses cookies, não peças chaves pagas.
- Escreve em PT-PT, curto, na voz de `tania-brand-context/references/tom-de-voz.md`.
