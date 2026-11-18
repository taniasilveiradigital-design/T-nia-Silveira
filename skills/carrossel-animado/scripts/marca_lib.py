"""O que verificar.py, marca.py e novo.py partilham: onde vivem as coisas, as cores e as fontes da marca, e a criação de uma pasta de carrossel."""
import colorsys
import json
import os
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile
from pathlib import Path

SK = Path(__file__).resolve().parent.parent
# No Windows, a app pode guardar as skills em pastas com caminhos acima de 260 caracteres, e aí o Python não abre os ficheiros.
if os.name == 'nt' and not str(SK).startswith(chr(92) * 2):
    SK = Path(chr(92) * 2 + '?' + chr(92) + str(SK))
CASA = Path(os.environ.get('CARROSSEL_CASA') or Path.home() / '.carrossel-animado')
MARCA = CASA / 'marca.json'
PRONTO = CASA / 'pronto.json'
PW = '1.64.1'
COPIADOS = ('render.mjs', 'entregar.py', 'folha.py', 'foto.py', 'limpar.py')
FORMATO = {'.woff2': 'woff2', '.woff': 'woff', '.ttf': 'truetype', '.otf': 'opentype'}
PAPEIS = {
    'titulo': ('Titulo', [(400, 'normal'), (400, 'italic')]),
    'texto': ('Texto', [(400, 'normal'), (500, 'normal'), (600, 'normal')]),
    'etiqueta': ('Etiqueta', [(500, 'normal')]),
}


def rgb(h):
    return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))


def lum(h):
    f = lambda v: v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = (f(v / 255) for v in rgb(h))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contraste(a, b):
    x, y = sorted((lum(a), lum(b)), reverse=True)
    return (x + 0.05) / (y + 0.05)


def misturar(a, b, k):
    return '#' + ''.join(f'{round(x + (y - x) * k):02x}' for x, y in zip(rgb(a), rgb(b)))


def derivar(c):
    """Acrescenta às seis cores da marca as que o motor calcula: letra sobre o destaque, destaque legível sobre o papel."""
    d = dict(c)
    dp = c['destaque']
    for _ in range(20):
        if contraste(dp, c['papel']) >= 3:
            break
        dp = misturar(dp, c['escuro'], 0.12)
    d['destaquePapel'] = dp
    escuro_ganha = contraste(c['escuro'], c['destaque']) >= contraste(c['creme'], c['destaque'])
    d['sobreDestaque'] = c['escuro'] if escuro_ganha else c['creme']
    d['acDestaque'] = c['creme'] if escuro_ganha else c['escuro']
    d['escuro2'] = misturar(c['escuro'], c['destaque'], 0.18)
    return d


def validar(m):
    """Devolve a lista de problemas, em palavras simples. Lista vazia quer dizer que a marca serve."""
    erros = []
    if not re.fullmatch(r'@[A-Za-z0-9._]{1,30}', m.get('handle', '')):
        erros.append('O @ tem de começar por @ e só pode ter letras, números, pontos e traços baixos.')
    if m.get('idioma') not in ('pt-PT', 'pt-BR'):
        erros.append('O idioma tem de ser pt-PT ou pt-BR.')
    c = m.get('cores', {})
    for k in ('escuro', 'destaque', 'claro', 'creme', 'papel', 'marcador'):
        if not re.fullmatch(r'#[0-9a-fA-F]{6}', c.get(k, '')):
            erros.append(f'A cor "{k}" tem de estar no formato #RRGGBB.')
    if erros:
        return erros
    for f in ('titulo', 'texto', 'etiqueta'):
        if not m.get('fontes', {}).get(f):
            erros.append(f'Falta a fonte de "{f}".')
    d = derivar(c)
    testes = [
        ('creme', 'escuro', 7, 'O texto claro não se lê sobre a cor escura.'),
        ('escuro', 'papel', 7, 'O texto escuro não se lê sobre a cor de papel.'),
        ('claro', 'escuro', 3, 'A cor clara de destaque não se vê sobre a cor escura.'),
        ('escuro', 'marcador', 7, 'O texto não se lê sobre o marcador.'),
    ]
    for a, b, minimo, msg in testes:
        v = contraste(c[a], c[b])
        if v < minimo:
            erros.append(f'{msg} ({a} sobre {b}: contraste {v:.1f}, mínimo {minimo}.)')
    if contraste(d['sobreDestaque'], c['destaque']) < 3:
        erros.append('Nenhuma letra se lê bem sobre a cor de destaque. Escolhe um destaque mais forte ou mais claro.')
    return erros


def carregar_marca():
    p = MARCA if MARCA.exists() else SK / 'assets' / 'marca-modelo.json'
    return json.loads(p.read_text(encoding='utf-8'))


def _mais_perto(disponiveis, peso):
    return min(disponiveis, key=lambda w: abs(w - peso)) if disponiveis else None


def _fontsource(slug):
    """Traz uma família do Google Fonts (pacote @fontsource). Fica guardada, para não voltar a descarregar."""
    cache = CASA / 'fontes' / slug
    if cache.exists() and list(cache.glob('*.woff2')):
        return cache
    with tempfile.TemporaryDirectory() as tmp:
        r = subprocess.run(f'npm pack @fontsource/{slug} --silent', shell=True, cwd=tmp, capture_output=True, text=True)
        tgz = list(Path(tmp).glob('*.tgz'))
        if r.returncode or not tgz:
            sys.exit(f'Não encontrei a fonte "{slug}" no Google Fonts. Confirma o nome em fonts.google.com, ou indica o ficheiro da fonte.')
        cache.mkdir(parents=True, exist_ok=True)
        with tarfile.open(tgz[0]) as t:
            for mem in t.getmembers():
                m = re.fullmatch(rf'package/files/{re.escape(slug)}-latin-(\d+)-(normal|italic)\.woff2', mem.name)
                if m:
                    (cache / f'latin-{m[1]}-{m[2]}.woff2').write_bytes(t.extractfile(mem).read())
    if not list(cache.glob('*.woff2')):
        shutil.rmtree(cache)
        sys.exit(f'A fonte "{slug}" não tem letras latinas. Escolhe outra.')
    return cache


def preparar_fontes(marca, destino):
    """Copia as fontes da marca para destino/ e devolve as regras @font-face."""
    destino.mkdir(parents=True, exist_ok=True)
    regras = []
    for papel, (familia, pedidas) in PAPEIS.items():
        origem = str(marca['fontes'][papel])
        ficheiro = Path(origem).expanduser()
        if ficheiro.is_file():
            if ficheiro.suffix.lower() not in FORMATO:
                sys.exit(f'A fonte {ficheiro.name} tem de ser .ttf, .otf, .woff ou .woff2.')
            nome = f'{papel}{ficheiro.suffix.lower()}'
            shutil.copy(ficheiro, destino / nome)
            regras.append(f"@font-face{{font-family:{familia};font-weight:100 900;src:url(fonts/{nome}) format('{FORMATO[ficheiro.suffix.lower()]}')}}")
            continue
        slug = re.sub(r'[^a-z0-9]+', '-', origem.lower()).strip('-')
        locais = list((SK / 'assets' / 'fonts').glob(f'{slug}-latin-*.woff2'))
        if locais:
            achar = {tuple(f.stem.split('-')[-2:]): f for f in locais}
        else:
            achar = {tuple(f.stem.split('-')[-2:]): f for f in _fontsource(slug).glob('*.woff2')}
        for peso, estilo in pedidas:
            pesos = [int(w) for w, s in achar if s == estilo]
            perto = _mais_perto(pesos, peso)
            if perto is None:
                continue  # Sem itálico próprio, o navegador inclina a letra normal.
            f = achar[(str(perto), estilo)]
            nome = f'{papel}-{peso}-{estilo}.woff2'
            shutil.copy(f, destino / nome)
            regras.append(f"@font-face{{font-family:{familia};font-weight:{peso};font-style:{estilo};src:url(fonts/{nome}) format('woff2')}}")
    return regras


def escrever_marca(pasta, marca):
    d = derivar(marca['cores'])
    regras = preparar_fontes(marca, pasta / 'fonts')
    h = colorsys.rgb_to_hsv(*[v / 255 for v in rgb(d['destaque'])])[0] * 360
    sepia = 0.1 if h < 70 or h >= 330 else 0  # Num destaque frio, um tom quente na foto ficaria errado.
    r = lambda k: ','.join(str(v) for v in rgb(d[k]))
    var = {
        'escuro': d['escuro'], 'escuro2': d['escuro2'], 'destaque': d['destaque'], 'claro': d['claro'], 'creme': d['creme'], 'papel': d['papel'],
        'marcador': d['marcador'], 'destaque-papel': d['destaquePapel'], 'sobre-destaque': d['sobreDestaque'], 'ac-destaque': d['acDestaque'],
        'escuro-rgb': r('escuro'), 'destaque-rgb': r('destaque'), 'claro-rgb': r('claro'), 'creme-rgb': r('creme'),
        'foto': f'contrast(1.08) saturate(1.1) sepia({sepia}) brightness(.98)',
    }
    css = '\n'.join(regras) + '\n:root{' + ';'.join(f'--{k}:{v}' for k, v in var.items()) + '}\n'
    (pasta / 'marca.css').write_text(css, encoding='utf-8')
    (pasta / 'marca.js').write_text('window.MARCA = ' + json.dumps({'handle': marca['handle'], 'idioma': marca.get('idioma', 'pt-PT'), 'cores': d}, ensure_ascii=False) + ';\n', encoding='utf-8')


def criar_pasta(pasta, marca, slides=None):
    """Cria uma pasta de carrossel. slides: ficheiro de assets a usar como slides.js."""
    pasta = Path(pasta)
    # O Chrome não abre ficheiros com caminho acima de 260 caracteres no Windows, e as fontes falham em silêncio.
    if len(str(pasta)) > 200:
        sys.exit(f'O caminho da pasta é demasiado longo ({len(str(pasta))} caracteres). Usa uma pasta mais curta.')
    shutil.copytree(SK / 'assets' / 'template', pasta, ignore=shutil.ignore_patterns('amostra.js'))
    for f in COPIADOS:
        shutil.copy(SK / 'scripts' / f, pasta / f)
    if slides:
        shutil.copy(slides, pasta / 'slides.js')
    (pasta / 'fotos').mkdir()
    escrever_marca(pasta, marca)
    # Grão de película, igual em todos os carrosséis.
    import numpy as np
    from PIL import Image
    Image.fromarray(np.random.default_rng(3).normal(128, 46, (1350, 1080)).clip(0, 255).astype('uint8'), 'L').save(pasta / 'fotos' / 'grao.png')
