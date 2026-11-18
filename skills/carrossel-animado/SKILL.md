---
name: carrossel-animado
description: "Cria carrosséis de Instagram animados com a marca de quem a usa: cada slide é um vídeo MP4 em loop de 1080x1350, sem áudio, feito em código, sem editor de vídeo e sem créditos. Prepara o computador na primeira vez, guarda a marca (cores, fontes, @ e voz) e depois pede o tema, as imagens e o tipo de animação. Trabalha em dois modos: revista (a pessoa em grande, letra editorial, palavras atrás da cabeça) ou motion (a animação é o conteúdo, com ou sem fotos). Entrega os vídeos, a legenda e uma vista para rever. USAR SEMPRE que pedirem um carrossel interativo, animado, com movimento, em motion, em vídeo ou que mexe, ou disserem 'anima este carrossel', 'carrossel em MP4', 'carrossel estilo revista', 'slides em vídeo para o Instagram', ou quando algo correr mal a meio de um destes carrosséis."
---

# Carrossel animado

Um carrossel é uma experiência construída slide a slide, onde a estratégia, o texto, a tipografia, a imagem e o movimento trabalham juntos. A animação serve a mensagem. Se um slide só fica bonito, falhou.

## Como falar com a aluna

Quem usa esta skill não é técnica. Fala em português simples, no idioma da marca dela (`pt-PT` ou `pt-BR`), com uma pergunta de cada vez.

- Diz "os vídeos", "gerar" e "a pasta". Evita "render", "script", "frames", "terminal" e "npm".
- Antes de um passo demorado, diz quanto tempo vai levar.
- Nunca lhe mostres um erro em bruto. Lê `references/socorro.md`, resolve o que conseguires e explica o resto numa frase.
- Se a app lhe pedir autorização para correr um comando, explica uma vez que é normal e o que esse comando faz.
- Nunca escrevas passwords por ela nem lhe peças para as colar aqui.
- Para perguntar, usa `AskUserQuestion`. Se não existir, pergunta em texto, com as opções numeradas.
- Para lhe mostrar uma imagem ou `vista.html`, abre-os no computador dela: `start "" "caminho"` no Windows, `open "caminho"` no Mac. Diz-lhe também onde está o ficheiro.

**Nunca há música nem efeitos sonoros.** Os vídeos saem sem áudio, porque a música escolhe-se diretamente no Instagram. Não escrevas "com som" nem "liga o som" nos slides nem na legenda.

`SK` é a pasta desta skill, indicada como "Base directory" quando a skill arranca. `PY` é o comando do Python: `python` no Windows, `python3` no Mac.

## Passo 1: preparar o computador (só na primeira vez)

Precisa de correr no computador dela: separador Code da app Claude no computador. Se não conseguires correr comandos, diz-lhe para abrir esse separador e voltar a pedir.

Vê se o Python existe, com `python --version` ou `python3 --version`. No Windows, uma mensagem a falar da Microsoft Store quer dizer que não está instalado. Se faltar, instala-o com o comando de `references/socorro.md`, pede-lhe para fechar e voltar a abrir a app, e recomeça.

```bash
PY SK/scripts/verificar.py
```

Corre em segundo plano na primeira vez, porque descarrega cerca de 300 MB e demora alguns minutos.

- `JÁ ESTÁ PRONTO` ou `TUDO PRONTO`: avança e guarda a estimativa de tempo que ele indica.
- `FALTA INSTALAR`: mostra os comandos a seguir. Corre-os com a autorização dela, pede-lhe para fechar e voltar a abrir a app, e corre outra vez. No Mac, se não houver Homebrew, manda-a a brew.sh, porque esse passo pede a password do computador e tem de ser ela a fazê-lo.

## Passo 2: a marca (só na primeira vez)

Se não existir `~/.carrossel-animado/marca.json`, lê `references/marca.md` e faz as perguntas que lá estão. Só avança quando ela aprovar a amostra.

Se ela pedir para mudar a marca mais tarde, edita esse ficheiro e corre outra vez `PY SK/scripts/marca.py`. Em cada carrossel, lê `marca.json`, porque tem o público, a voz e o idioma.

## Passo 3: o que este carrossel vai ser

Estas respostas decidem o carrossel inteiro. Usa `AskUserQuestion` e pergunta só o que ela ainda não disse:

1. **O tema.** De que fala e qual é a ideia que tem de ficar.
2. **As imagens.** Tem fotos para usar? Pede os ficheiros ou a pasta, ou aceita que não há imagens. Pode também indicar um vídeo e o segundo que quer usar. Usa só imagens que ela indique, e diz-lhe que têm de ser dela ou ter autorização.
3. **O tipo de animação:**
   - **Revista:** como a capa de uma revista, com a foto dela a ocupar o slide inteiro, letras grandes e quase tudo parado. Precisa de fotos.
   - **Motion:** como um pequeno desenho animado, em que a animação conta a ideia. Pode não ter fotos.
   - E se tem uma referência, um estilo ou uma ideia para algum slide. Se der imagens de referência, olha para elas antes de desenhar.
4. **O objetivo.** O que quer que o público faça no fim, e o que tem para oferecer a quem comentar. Pergunta se essa oferta já existe e como a vai enviar.

Não vás buscar imagens às pastas dela sem perguntar. Se não tiver nenhuma, sugere motion sem foto ou um frame de um vídeo dela.

Há duas paragens para ela aprovar: o texto (Fase B) e os slides parados (Fase D). Mudar o texto ou o desenho custa segundos. Depois de gerar, custa minutos. Só saltas as paragens se ela o pedir, e nesse caso diz no fim o que assumiste.

Agora cria a pasta do carrossel, porque tudo o que se segue fica lá. Fica em `~/Carrosseis`, fora do OneDrive e do iCloud, porque os ficheiros temporários ocupam vários GB. Diz-lhe onde fica.

```bash
PY SK/scripts/novo.py nome-do-carrossel
```

Os exemplos da skill estão em português de Portugal. Em `pt-BR`, adapta-os ("Desliza", "envio-te") à forma como ela escreve, e pergunta se tiveres dúvidas.

## Fase A: conceito

Define antes de qualquer slide:
- O público e a ideia que deve ficar na memória.
- O que torna este ângulo diferente do que qualquer conta do nicho dela diria.
- O objetivo e a única ação que queremos do público.

Não inventes dados, estudos, experiências dela nem resultados. Uma pergunta não afirma nada, e uma estatística inventada destrói a confiança. Se o argumento precisar de uma história ou de um número, pergunta-lhe. Números verificáveis do próprio carrossel são bons ("240 fotos, só neste slide").

## Fase B: narrativa

Referência de 8 slides. Ajusta ao tema, sem acrescentar slides só para chegar ao número. Se ela pedir menos, funde funções e mantém sempre Parar, Revelação e Agir. Com 5 slides: Parar / Promessa e identificação / Revelação / Demonstração, guardar e aplicação / Agir. Com 3 slides: Parar / Revelação / Agir.

| Slide | Função | O que tem de fazer |
|---|---|---|
| 1 | Parar | Título de 3 a 8 palavras que cria tensão. Não explica tudo. |
| 2 | Confirmar a promessa | Mostra que a capa tem fundamento. Funciona também como ponto de entrada, porque o Instagram volta a mostrá-lo. |
| 3 | Identificação | Uma situação concreta que o público reconhece. |
| 4 | Revelação | A ideia central, a perspetiva que muda a forma de ver o tema. |
| 5 | Demonstração | Antes e depois, comparação, exemplo real. O formato segue a mensagem. |
| 6 | Guardar | Um método, checklist ou modelo que vale sozinho fora do carrossel. |
| 7 | Aplicação | Uma tarefa concreta para fazer já. |
| 8 | Agir | Uma só chamada para ação, de preferência "Comenta X e envio-te Y". |

Cada slide tem de fazer sentido se alguém lhe tirar uma captura de ecrã e o enviar a outra pessoa.

Se o CTA promete enviar algo, Y tem de existir antes de publicar. Se ela já o tiver, guarda o link em `recurso.txt`. Se não tiver, oferece-te para escrever um rascunho e marca-o no topo como `RASCUNHO, a rever`. É conteúdo profissional dela, por isso diz-lhe claramente que tem de o rever, sobretudo em áreas como saúde, finanças ou direito. Na legenda, não digas que está pronto antes de ela o rever. `entregar.py` copia `recurso.txt` para a entrega. Como chega a quem comenta é decisão dela: diz-lhe que está por tratar, se ainda não souber.

Escreve o texto de cada slide na voz de `marca.json` e **mostra-lho para aprovar antes de desenhar**. Segue as regras de `references/legenda.md`.

## Fase C: direção de arte

**O que torna isto básico, e por isso evita:** fundo escuro plano, texto empilhado à esquerda em todos os slides, linhas finas decorativas, quadrados e bolas genéricos, tudo do mesmo tamanho, e nenhuma imagem ou ideia visual forte.

**Comum aos dois modos**
- Títulos com contraste forte de escala: enormes, apertados, com uma segunda linha em itálico na cor de destaque. As fontes e as cores vêm da marca dela.
- Alterna momentos para dar ritmo: um poster (`theme: 'destaque'`), papel (`theme: 'papel'`, muito bom para o slide de guardar), cartões, placas em perspetiva. Dois slides seguidos com a mesma estrutura são sinal de alerta.
- O `handle()` fica no mesmo sítio em todos, e todos os slides duram o mesmo, 8 segundos. A seta de deslizar (`.seta`) vai só na capa.
- Uma cara nunca fica tapada, em nenhum modo. O texto e os objetos ficam fora da boca e dos olhos.
- Nada de texto abaixo de 28 px, porque o Instagram vê-se no telemóvel. O render avisa.
- Por defeito, uma luz atravessa as costuras entre slides (`seam` em `arrancar`), à mesma altura dos dois lados, para dar vontade de deslizar. Confere-a em `static/_costuras.png`. Em motion, pode ser um elemento que passa de um slide para o outro, com a receita de `references/motor.md`.

**Modo revista**
- A foto ocupa o slide inteiro e a pessoa é o centro.
- A assinatura é uma palavra gigante atrás da cabeça, entre a foto e o recorte. A cabeça pode tapar um pouco, mas a palavra tem de se ler.
- O texto começa abaixo do queixo. Ajusta o enquadramento em `cena(n, { x, y, w })`.
- Escolhe expressões que digam alguma coisa e evita a boca a meio de uma palavra. Uma foto por slide, sem repetir, por isso pede-lhe uma por slide. Se tiver poucas, intercala com slides sem foto.
- Nunca uses um vídeo de alguém a falar como fundo: sem som, parece um erro.
- Quase estático: zoom lento, a palavra a deslizar, um gesto por slide.

**Modo motion**
- O movimento é a ideia, por isso cada slide é uma cena com um tema próprio: o que ela pediu, ou a tradução visual da ideia desse slide. Uma metáfora a acontecer é melhor do que formas a passar.
- Desenha em `tela()` ou com elementos SVG.
- Fotos, se as houver, entram como recortes dentro da cena, com `recorte(n, { x, y, w })`.
- Pode haver mais movimento do que na revista, mas o olhar segue uma coisa de cada vez. Se tudo compete, nada se lê.

**O movimento, em ambos**
- **O texto lê-se.** Fica trancado na revista. Em motion pode entrar ou formar-se, mas tem de estar completo e parado pelo menos metade do loop.
- **Um gesto principal por slide.** Se tudo se mexe por igual, nota-se que foi automático.
- **O que salta passa pela opacidade 0.** Um número ou um anel a mudar de repente parece um erro.
- **Suavidade e peso.** Nada se move de forma linear. O que cai estica e achata no impacto.
- **Ritmo.** Os gestos começam em tempos certos, a cada 0,5 s, e tudo o que se repete dá voltas inteiras no loop. Não prometas que acerta na música que ela vai escolher.

Escreve `STORYBOARD.md` com uma linha por slide: função, composição, imagem e gesto com os tempos.

## Fase D: produção

Antes de escrever código, lê `references/motor.md`. Para veres como se constrói cada gesto, lê `assets/exemplo/motion.js`, que corre sem fotos, e em modo revista `assets/exemplo/revista.js`. Não repitas as composições sem razão.

Dentro da pasta do carrossel, trabalha nesta ordem:

1. **Imagens.** Para cada imagem: `PY foto.py N "caminho"`, ou `PY foto.py N "video.MOV" --t 28` para um frame de vídeo. Cria `fotos/fN.jpg` e o recorte `fotos/fN.png`. Na primeira vez descarrega cerca de 170 MB e pode demorar alguns minutos. As fotos deitadas perdem muito dos lados.
2. **Desenho.** Escreve `slides.js`, depois `node render.mjs --at 0,2.25,4,7.9` e `PY folha.py`. Olha mesmo para `static/_folha.png`, `static/_costuras.png` e `static/_em.png`, que mostra cada slide a meio do movimento, e repete até estar bem. Uma verificação sem erros não mostra como o slide fica. É aqui que se apanha quase tudo.
3. **Aprovação.** Mostra-lhe `static/_folha.png` e `static/_em.png`, para ela ver o movimento em momentos diferentes, e explica numa frase o que mexe em cada slide. Avança quando ela aprovar.
4. **Gerar os vídeos.** `node render.mjs`, em segundo plano e só depois de `foto.py` acabar. Diz-lhe a estimativa do `verificar.py`, proporcional ao número de slides, que pode chegar ao dobro com muitas fotos, que o computador tem de ficar ligado à corrente e sem adormecer, e que pode continuar a usá-lo mais lento. Para refazer um slide: `node render.mjs --slide N`, depois `PY entregar.py --slide N`.
5. **Legenda.** Escreve `legenda.txt` com as regras de `references/legenda.md`.
6. **Entrega e auditoria técnica.** `PY entregar.py`, que demora cerca de 30 segundos por slide. Cria `entrega/01.mp4`, `02.mp4`... e `vista.html`.

## Fase E: auditoria

**Técnica.** `entregar.py` verifica o primeiro frame, a emenda do loop, o formato (1080x1350, 30 fps, número de frames), a duração, a ausência de áudio, texto nos cantos e a junção do loop no próprio vídeo, e diz o que falhou. Avisa também de frames isolados, que tens de abrir e ver. Se houver falhas, descobre a causa antes de mexer na tolerância.

**Visual, feita por ti.** O OK técnico não vê o design. Corre `PY folha.py --slide N` em cada slide, para veres um frame a cada 0,5 s, e procura:
- Texto a tapar a boca ou os olhos, ou a cabeça a tapar demasiado a palavra.
- Palavras sozinhas numa linha: acerta a quebra com `<br>`.
- Palavras partidas no hífen ("envio-te"): envolve-as em `<span style="white-space:nowrap">`.
- Recortes fora da própria foto: restos de fundo e cortes direitos na margem da imagem.
- Espaço morto: um terço do slide vazio sem intenção.
- Texto legível no tamanho de telemóvel. O texto desenhado em `tela()` não passa nas verificações automáticas, por isso confere-o à mão.

**Editorial.** Passa a lista de `references/legenda.md`. A capa desperta interesse? O que vem a seguir confirma a promessa? Alguma afirmação não tem base?

Corrige antes de apresentar.

## Fase F: entrega

Mostra-lhe a folha de contactos, indica-lhe `vista.html` e `entrega/`, e diz com clareza:
- O que assumiste (ângulo, a promessa do CTA) e onde falta a voz ou uma história dela.
- O que não consegues verificar: não vês o vídeo a tocar nem no telemóvel, só imagens e medições. Pede-lhe para ver no telemóvel antes de publicar.
- Nada é publicado. Para subir: passar os vídeos para o telemóvel, criar um post, escolher os vídeos por ordem e acrescentar a música no Instagram.

Depois de ela aprovar os vídeos, oferece-te para libertar espaço com `PY limpar.py`, que apaga os ficheiros temporários e mantém os vídeos, a legenda e o código. Se ela quiser mudar um slide mais tarde, basta gerá-lo outra vez.
