# Quando algo corre mal

Resolve o que conseguires sem a incomodar. Explica-lhe o problema numa frase, sem o erro em bruto, e diz-lhe o que vais fazer. Só lhe peças uma ação se tiver mesmo de ser ela.

Se ela disser só "não funciona", descobre onde parou: há `pronto.json` e `marca.json` em `~/.carrossel-animado`? Há vídeos em `entrega/` e frames em `frames/` na pasta do carrossel? Continua a partir daí, sem refazer o que está feito.

## A preparar o computador

| O que aparece | O que quer dizer | O que fazer |
|---|---|---|
| Comando `python` não encontrado, ou mensagem da Microsoft Store | Falta o Python | Windows: `winget install --id Python.Python.3.12 -e --accept-source-agreements --accept-package-agreements`. Mac: `brew install python`. Depois, ela fecha e volta a abrir a app. |
| `winget` não encontrado | Windows antigo, sem o instalador | Pede-lhe que instale "Instalador de Aplicações" (App Installer) na Microsoft Store e volta a tentar. |
| `brew` não encontrado | Mac sem o Homebrew | Manda-a a brew.sh. Tem de ser ela a colar o comando na app Terminal, porque pede a password do computador. |
| `FALTA INSTALAR` outra vez, depois de instalar | A app ainda não vê o que foi instalado | Ela fecha a app por completo e volta a abri-la. |
| Erro de `pip`, ou `não consegui instalar numpy e pillow` | Python sem permissões, ou sem internet | Confirma a internet. Depois tenta `PY -m pip install numpy pillow`. |
| `não consegui descarregar o navegador` ou `o motor` | Internet, ou rede que bloqueia | Tenta outra rede. Numa rede de empresa, pode estar bloqueado. |
| Antivírus a bloquear `chrome-headless-shell` | O navegador do motor parece suspeito ao antivírus | Vem do Playwright, da Microsoft. Pede-lhe para o autorizar, e confirma com ela antes. |

## A criar o carrossel

| O que aparece | O que quer dizer | O que fazer |
|---|---|---|
| `Fontes que não carregaram` | Caminho da pasta demasiado longo, ou ficheiro de fonte estragado | Cria o carrossel em `~/Carrosseis`. Se continuar, troca a fonte em `marca.json`. |
| `Não encontrei a fonte` | Nome errado no Google Fonts | Confirma o nome em fonts.google.com, ou pede o ficheiro. |
| `imagens que não carregaram` | Falta uma foto, ou `foto.py` não correu | Corre `foto.py` para esse número, ou corrige `slides.js`. |
| `O recorte falhou` | Sem internet na primeira vez, ou foto difícil | Confirma a internet e repete. Se falhar sempre, usa `--sem-recorte`, sem palavra atrás da cabeça nesse slide. |
| `foto de iPhone (HEIC)` | O computador não a consegue abrir | No telemóvel, pede-lhe para a enviar como JPG, ou no computador para a exportar. |
| `texto a sair do slide` | A fonte dela é mais larga | Encolhe esse texto, ou parte-o em mais linhas. |
| Pouco espaço em disco | Um carrossel de 8 slides ocupa cerca de 5 GB até acabar | `PY limpar.py` nos carrosséis já aprovados. |

## A gerar os vídeos

| O que aparece | O que quer dizer | O que fazer |
|---|---|---|
| Para a meio, ou o computador adormeceu | Foi interrompido | `node render.mjs --slide N` nos slides que faltam. Os outros continuam feitos. Pede-lhe que ligue o computador à corrente. |
| `Faltam frames dos slides` | A geração não acabou | O mesmo: gera esses slides outra vez. |
| Muito lento | Computador fraco, ou muitos programas abertos | Avisa-a e deixa correr. Fechar outros programas ajuda. |
| Erro em `frame 0` | O início do vídeo não bate certo com o desenho | Vê a tabela de armadilhas em `references/motor.md`. |
| Erro em `loop` | O fim do vídeo não encaixa no início | Tudo o que mexe tem de dar voltas inteiras e acabar parado. |
| `texto nos cantos` | O contador do Instagram tapa esse texto | Afasta o texto dos cantos à direita. |

## Nos vídeos

| O que aparece | O que fazer |
|---|---|
| O `vista.html` não mostra os vídeos | Abre-o com duplo clique a partir da pasta do carrossel. Os vídeos têm de ficar em `entrega/`. |
| O Instagram corta os lados | Num carrossel, todos os vídeos têm de ter o mesmo formato. Confirma no Instagram que escolheu o formato 4:5. |
| O vídeo passa mal para o telemóvel | Enviar por email ou WhatsApp reduz a qualidade. Usa AirDrop, um cabo, Google Drive ou iCloud. |

Se nada disto resolver, resume o que aconteceu em duas frases para ela poder pedir ajuda, sem caminhos pessoais nem dados da conta.
