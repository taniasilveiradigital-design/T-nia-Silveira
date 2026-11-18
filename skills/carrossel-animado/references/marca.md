# A marca da aluna

Faz-se uma vez. Fica guardada em `~/.carrossel-animado/marca.json`, com a forma de `assets/marca-modelo.json`, e todos os carrosséis a seguir usam-na. Faz as perguntas por partes, sem jargão, e aceita "não sei": há sempre um valor por defeito.

## O que perguntar

1. **Quem é:** nome, @ do Instagram, e se escreve em português de Portugal (`pt-PT`) ou do Brasil (`pt-BR`).
2. **O negócio:** o que faz e para quem, numa frase cada.
3. **As cores.** Se tiver as cores da marca, pede os códigos ou uma imagem da marca, e tira deles as seis abaixo. Se não tiver, abre `assets/paletas.png`, onde vê as paletas prontas, e pergunta qual prefere.
4. **As fontes.** Pergunta só duas: a dos títulos e a do texto. Pode dar o nome de uma fonte do Google Fonts, um ficheiro de fonte (`.ttf`, `.otf`, `.woff`, `.woff2`), ou deixar as sugeridas. Uma fonte paga só pode ser usada se ela tiver licença, por isso diz-lhe isso se ela indicar um ficheiro. Em `etiqueta`, usa a fonte do texto, a não ser que ela peça outra.
5. **A voz.** Pede-lhe que cole duas ou três legendas que tenha escrito e gostado. Se ela tiver uma skill ou um documento de voz próprios, usa-os. Tira daí o tom, as regras e as palavras que evita, e guarda frases dela em `exemplos`, tal e qual. Pergunta também se usa hashtags. Mostra-lhe o resumo. Sem exemplos, pergunta como descreveria a forma como fala com as clientes.

## As seis cores

| Campo | Para quê | Regra |
|---|---|---|
| `escuro` | Fundo escuro e texto sobre claros | Muito escuro, quase preto, mesmo numa marca clara |
| `destaque` | A cor forte: posters e fundo dos slides de destaque | A cor principal da marca |
| `claro` | Segunda linha em itálico sobre o escuro | Versão clara do destaque |
| `creme` | Texto sobre o escuro | Quase branco |
| `papel` | Fundo claro, dos slides para guardar | Claro e suave |
| `marcador` | Fundo de palavras em destaque | Claro e vivo |

## Paletas prontas

| Nome | escuro | destaque | claro | creme | papel | marcador |
|---|---|---|---|---|---|---|
| Terracota | `#1c120e` | `#c8653f` | `#eeb394` | `#f8f1e8` | `#f2e8dc` | `#fbf0a4` |
| Floresta | `#101a15` | `#3f8f6b` | `#a8d8bd` | `#f3f6ef` | `#e8eee2` | `#f2ee9a` |
| Noite | `#14161f` | `#6c7cff` | `#b9c2ff` | `#f4f4f8` | `#eceef6` | `#fff3a0` |
| Ameixa | `#1b1020` | `#a0457f` | `#e3aacb` | `#f8f1f5` | `#f1e6ed` | `#fbeea8` |

## Fontes por defeito

`Instrument Serif` para títulos, `Inter` para texto e `JetBrains Mono` para etiquetas. Títulos pedem uma fonte com personalidade. Texto pede uma fonte simples, legível em tamanho pequeno. Uma fonte sem itálico próprio fica inclinada à força: se ficar mal na amostra, troca-a ou tira o itálico dos títulos.

## Guardar e confirmar

Escreve `marca.json`, e depois:

```bash
PY SK/scripts/marca.py
```

- `A MARCA PRECISA DE AJUSTES`: explica-lhe o problema numa frase, ajusta as cores e corre outra vez. Um contraste baixo quer dizer que o texto não se ia ler, por isso muda a cor em vez de ignorar.
- `MARCA OK`: olha para a amostra e mostra-lha. Ela tem de ver as três amostras (escura, destaque e papel) e dizer se se revê nelas. Confirma os acentos: uma letra noutro desenho quer dizer que a fonte não os tem. A pergunta para ela é se gosta das cores e das letras, porque o texto da amostra é só de exemplo. Se vires um defeito de posição, resolve-o tu e não lho atribuas à fonte.

Só avança para o carrossel depois de ela aprovar.
