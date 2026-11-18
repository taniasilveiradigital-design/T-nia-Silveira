# O motor

Na pasta do carrossel, `index.html` carrega `marca.css` e `marca.js` (a marca dela, gerados), `engine.js` (não se mexe) e `slides.js` (o carrossel). Os exemplos estão em `assets/exemplo/`: `motion.js` e `revista.js`.

## Forma de um slide

```js
const SEAM = [760, 1040];     // altura da luz em cada costura: SEAM[0] entre os slides 1 e 2

const SLIDES = {
  1: () => {
    // Constrói aqui o DOM, uma vez.
    return {
      theme: 'destaque',      // opcional: 'destaque' ou 'papel'. Por defeito, escuro.
      seek(t) { /* desenha o frame do segundo t */ },
    };
  },
};
arrancar(SLIDES, { seam: SEAM });   // última linha. Sem seam, não há luz.
```

O loop dura `T` = 8 segundos, em todos os slides.

## Peças de engine.js

| Peça | Para quê |
|---|---|
| `el(classe, css, html, pai, tag)` | Cria um elemento. O pai é `content`, por defeito. |
| `cena(n, { x, y, w })` | Foto `fotos/fN.jpg`, camada `tras` e recorte `fotos/fN.png`, sempre alinhados. Devolve `{ c, tras }`. Por defeito `x: -70, y: -205, w: 1220`. Uma foto que não seja 9:16 é cortada dos lados, sem deformar: acerta o tamanho com `w`. |
| `zoom(s.c, t)` | Zoom lento e periódico da cena. Usa em `seek`. |
| `scrim(de, ate, forte)` | Escurece de baixo para cima, para o texto se ler sobre a foto. |
| `handle()` | Põe o @ da marca em baixo, à esquerda. |
| `COR` | As cores da marca: `COR.escuro`, `destaque`, `claro`, `creme`, `papel`, `marcador`, `destaquePapel` (destaque legível sobre papel), `escuro2`, `sobreDestaque`. |
| `tela(pai)` | Canvas a toda a área, para motion. Devolve o contexto 2D. Limpa-o em cada `seek`. |
| `recorte(n, { x, y, w, pai })` | Só a pessoa, sem a foto de fundo, com a mesma cor de `cena`. |
| `mod(x, m)`, `ressalto(x)`, `semente(n)` | Resto sempre positivo, chegada com ressalto, e números aleatórios sempre iguais. |
| `placa(x, y, html, opções)` | Placa em perspetiva. |
| `wave(t, k, fase)` | Onda com `k` voltas em 8 s. Com `k` inteiro, o fim encaixa no início. |
| `salto(t, instante, d)` | Opacidade que passa por 0 no instante de um salto. |
| `clamp`, `outCubic`, `inOut`, `inCubic`, `px` | Ajudas. |

Fontes, sempre com estes nomes, seja qual for a fonte da marca: `Titulo`, `Texto` (400, 500, 600) e `Etiqueta` (500). Um nome errado cai noutra fonte sem dar erro. Em canvas, escreve por exemplo `g.font = 'italic 96px Titulo'` e as cores com `COR`. Nunca escrevas à mão as cores da marca (só o preto de uma sombra): nas CSS usa `var(--destaque)`, `var(--ac)`, ou `rgba(var(--escuro-rgb),.5)`.

Cada fonte tem larguras diferentes. Os tamanhos dos exemplos são um ponto de partida, por isso confere na folha e nos avisos de `render.mjs`.

Classes de `index.html`: `.abs`, `.titulo`, `.texto`, `.etiqueta`, `.ac` (cor de destaque do tema), `.marcador` (fundo de marcador), `.cartao`, `.etq`, `.rot`, `.linha`, `.num`, `.vidro`, `.caixa`, `.tira`, `.furos`, `.cel`, `.caret`, `.seta`.

| Classe | Para quê |
|---|---|
| `.seta` | "Desliza" com seta. Põe a seta num `<b>`, que é o que se anima. Fica à direita do @, por isso mantém-na curta. |
| `.marcador` | Fundo de marcador. Usa-a num `<span>`. |
| `.caixa` | Caixa de comentário, 952 x 116 px, com `top` à tua escolha. Põe o texto e o coração lá dentro. |
| `.vidro` | Painel escuro translúcido, para texto sobre foto. |
| `.etq`, `.rot` | Etiqueta em forma de cápsula, e rótulo no canto de um cartão. |
| `.linha`, `.num` | Uma linha de lista com número redondo. |
| `.tira`, `.furos`, `.cel` | Película fotográfica. |

**Limites do render.** Texto abaixo de 28 px dá aviso. Texto com a direita além dos 940 px e com o topo acima dos 120 px ou o fundo abaixo dos 1240 px falha em `entregar.py`, porque a interface do Instagram o tapa. A linha conta inteira, mesmo com letras mais pequenas, por isso títulos largos devem começar abaixo dos 120 px. Texto fora do slide dá aviso, exceto em `s.tras`.

## A luz das costuras

Em `arrancar(SLIDES, { seam })`, cada número é a altura da luz numa costura. Fica por cima da foto e por baixo do texto. Escolhe alturas onde o fundo está vazio, e varia de costura para costura. Usa `null` para deixar uma costura sem luz, e tira-a se parecer uma mancha sobre `papel`. Confirma sempre em `static/_costuras.png`.

## Palavra atrás da cabeça

```js
const s = cena(1, { y: -140 });
const g = el('abs titulo', { left: '30px', top: '56px', fontSize: '296px', fontStyle: 'italic', whiteSpace: 'nowrap' }, 'Palavra', s.tras);
scrim(24, 46);
// em seek: zoom(s.c, t); g.style.transform = `translateX(${14 * wave(t, 1)}px)`;
```

O texto em `s.tras` fica entre a foto e o recorte. Se a cabeça tapa demasiado, desce a pessoa com `y` ou encolhe a palavra. Texto normal vai em `content`, depois do `scrim`.

Mexe a palavra, mas nunca a foto em relação ao recorte, senão aparece a pessoa em duplicado. Sobre a própria foto, os defeitos do recorte não se veem. Fora da foto, sobre cor lisa, veem-se: confirma e apaga restos pintando o alfa de `fotos/fN.png` com um polígono.

## Motion

```js
3: () => {
  const g = tela();
  return {
    seek(t) {
      g.clearRect(0, 0, 1080, 1350);
      const p = inOut(clamp((t - 2) / 2));    // anda de 0 a 1 entre as 2 s e as 4 s
      // desenha aqui, só com t e p
    },
  };
},
```

Põe o texto com `el`, depois de `tela()`, mesmo em motion. As verificações de 28 px e de cantos só veem texto em `el`: o que escreves no canvas tens de conferir à mão.

O frame 0 continua a ter de ser um desenho acabado. Uma cena que se constrói tem de estar completa em `t = 0` e no fim, e desfaz-se e refaz-se pelo meio, com o padrão abaixo.

**Um elemento que passa de um slide para o outro.** Desenha-o em coordenadas contínuas, como se os slides fossem uma só tira: `xGlobal = x + (id - 1) * 1080`. Mantém a mesma altura em todos e não uses `seam`. Cada vídeo arranca sozinho no Instagram, por isso só nos momentos parados é que bate certo: põe os elementos parados e cortados na costura em `t = 0` e no fim.

**Velocidade.** Cada frame é um instante, sem desfoque. Acima de cerca de 80 px por frame, o olho perde o objeto: desenha um rasto de cópias apagadas ou abranda. Raios de roda a girar depressa parecem andar ao contrário.

**Uma coisa que se estraga ou desfaz.** O frame 0 é a capa e o vídeo volta sempre ao início, por isso não pode acabar de outra forma. Mostra na capa o estado final, já desfeito, que é o que dá tensão ao título. A meio, passa pela opacidade 0, recomeça do estado inteiro e deixa-o desfazer-se à frente de quem vê, até voltar à capa. Evita desfazer o movimento ao contrário, porque parece um filme a andar para trás.

**Etiquetas diferentes num ciclo.** Se os objetos têm conteúdo diferente, o avanço total em 8 s tem de ser múltiplo do número de objetos, senão o loop salta.

## Tempos de render

Um frame pode demorar de 0,1 a 2 s, consoante o slide, por causa do grão e das misturas de cor. Conta com vários minutos por slide, e corre sempre em segundo plano. O render mostra o progresso a cada 60 frames.

Cada correção depois do render custa minutos, por isso vê tudo antes: `node render.mjs --at 0,0.5,1,1.5,2,2.5,3,3.5,4,4.5,5,5.5,6,6.5,7,7.5` e `python folha.py` dão uma folha legível por slide, em `static/_em_s01.png` e seguintes, em segundos. Com `--slide N`, só desse slide. Até 8 tempos, fica tudo em `static/_em.png`.

## A regra do seek(t)

`seek(t)` só pode depender de `t`. O render pede os frames fora de ordem, por isso estado guardado entre chamadas parte o vídeo. Sem temporizadores, sem `requestAnimationFrame` e sem `Math.random()`. Para valores aleatórios, usa uma sequência com semente fixa.

**O frame 0 é a capa do slide.** Tem de ser o desenho acabado, porque é o que se vê antes de o vídeo arrancar e o que fica se o Instagram não o reproduzir. Por isso o gesto segue este padrão:

```js
// Parado até 1,5 s, desaparece até 1,75 s, atua a partir das 2,0 s, e acaba parado.
if (t < 1.5) rest(); else if (t < 1.75) fadeOut(); else if (t < 2) hidden(); else perform(t - 2);
```

O último frame tem de encaixar no primeiro: o que mexe sempre dá voltas inteiras, e o que atua acaba parado.

**O que salta passa pela opacidade 0.** Usa `el.style.opacity = salto(t, instante)` à volta do salto, ou `0.8 * Math.sin(Math.PI * progresso)` num elemento que aparece e desaparece.

## Micro-movimentos

Além do gesto do slide, só os detalhes se mexem, e ligeiramente: zoom da foto, uma palavra a deslizar, um cursor a piscar, uma seta a ir e voltar, uma placa a flutuar, um anel a pulsar.

## Placas em perspetiva

Boas para mostrar camadas, etapas ou ferramentas empilhadas. Cada placa é um quadrado de 300 px inclinado, com duas faces laterais em SVG, e ocupa 450 px de largura.

```js
// Cria de baixo para cima, 160 px entre placas: a última criada fica por cima.
const c = placa(540, 800, '<div style="margin:78px 0 0 78px;font:400 48px Titulo">Vídeo</div>');
const b = placa(540, 640, '<div style="margin:78px 0 0 78px;font:400 48px Titulo">Página</div>');
```

A placa de cima tapa cerca de 113 x 113 px do canto superior esquerdo da de baixo, por isso põe o conteúdo fora dessa zona. Para flutuar: `b.style.transform = 'translateY(' + 6 * wave(t, 1) + 'px)'`.

## Armadilhas já encontradas

| Sintoma | Causa | Solução |
|---|---|---|
| Títulos em Times | O nome da fonte está errado | Usa a família `Titulo`. Se a fonte não carregar, `render.mjs` para com erro. |
| Frame 0 diferente em SVG ou elemento com escala | Com diferença acima de 8 em 255 ou em muitos píxeis, é um erro real: o `seek(0)` não desenha o mesmo do início | Confirma que `seek(0)` repõe tudo. Usa `will-change:transform` e deixa sempre `scale(s)` em vez de `none`. |
| Algarismos desalinhados | Tabela de algarismos errada | `font-variant-numeric: lining-nums tabular-nums`. |
| Janela que muda de tamanho com texto a escrever-se | O texto ainda não escrito não ocupa espaço | Mantém o resto em `visibility:hidden` (ver slide 5 de `motion.js`). |
| ✓, ✕ ou → noutro desenho | As fontes só têm o alfabeto latino, e estes símbolos vêm de uma fonte do sistema, que muda entre Windows e Mac | Desenha-os em SVG. |
| Aviso de texto a sair do slide | A fonte da marca é mais larga do que a do exemplo | Encolhe o texto ou parte-o em mais linhas. |
| `junção` baixa em dB num slide agitado | Muito movimento dá poucos dB, mesmo sem salto | Só é erro se for bem pior do que `seguidos`. |
| `seguidos 99` | Slide parado no fim do loop, dois frames idênticos | É normal. |
| Aviso de texto nos cantos com o texto longe do canto | O teste usa a caixa da linha, maior do que as letras | Encolhe o texto ou muda-o de sítio. `entregar.py` trata-o como falha. |
| Aviso de frames isolados | Um frame sozinho diferente dos vizinhos | Abre esse frame e os vizinhos. Com ressaltos e saltos de propósito, é um falso alarme frequente. Se parecer um erro de desenho, corrige-o. Durante movimento rápido contínuo, este aviso não apanha nada: revê esses trechos a olho. |
