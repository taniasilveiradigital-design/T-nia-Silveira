"""Prepara o computador para fazer carrosséis, e confirma que tudo funciona com um teste real.
Uso: python verificar.py [--forcar]
Termina com código 0 se está tudo pronto, e 2 se falta instalar alguma coisa à mão."""
import json
import os
import platform
import re
import shutil
import subprocess
import sys
import time
from datetime import date
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, str(Path(__file__).resolve().parent))
from marca_lib import CASA, PRONTO, PW, SK  # noqa: E402

VERSAO = 1
MAC = platform.system() == 'Darwin'
GB_PRECISOS = 8

if PRONTO.exists() and '--forcar' not in sys.argv:
    p = json.loads(PRONTO.read_text(encoding='utf-8'))
    if p.get('versao') == VERSAO and (CASA / 'motor' / 'node_modules' / 'playwright-core').exists():
        print(f"JÁ ESTÁ PRONTO. Um carrossel de 8 slides demora cerca de {p['minutos_8_slides']} minutos a gerar, ou mais com fotos.")
        sys.exit(0)

faltam = []
if sys.version_info < (3, 9):
    faltam.append('python')
node = shutil.which('node')
if not node:
    faltam.append('node')
else:
    v = subprocess.run(['node', '--version'], capture_output=True, text=True).stdout
    if int(re.match(r'v(\d+)', v)[1]) < 20:
        faltam.append('node')
if not shutil.which('npm') and 'node' not in faltam:
    faltam.append('node')
if not shutil.which('ffmpeg') or not shutil.which('ffprobe'):
    faltam.append('ffmpeg')
elif 'libx264' not in subprocess.run(['ffmpeg', '-hide_banner', '-encoders'], capture_output=True, text=True, errors='replace').stdout:
    faltam.append('ffmpeg')

if faltam:
    print('FALTA INSTALAR: ' + ', '.join(faltam))
    if MAC:
        print('Mac, com o Homebrew (brew.sh):')
        pacote = {'python': 'python', 'node': 'node', 'ffmpeg': 'ffmpeg'}
        print('  brew install ' + ' '.join(pacote[f] for f in faltam))
    else:
        print('Windows:')
        pacote = {'python': 'Python.Python.3.12', 'node': 'OpenJS.NodeJS.LTS', 'ffmpeg': 'Gyan.FFmpeg'}
        for f in faltam:
            print(f'  winget install --id {pacote[f]} -e --accept-source-agreements --accept-package-agreements')
    print('Depois de instalar, fecha a app por completo, volta a abri-la e corre isto outra vez.')
    sys.exit(2)
print('OK: Python, Node e ffmpeg')

livre = shutil.disk_usage(Path.home()).free / 1024 ** 3
if livre < GB_PRECISOS:
    print(f'AVISO: só tens {livre:.0f} GB livres. Enquanto se gera, um carrossel de 8 slides ocupa cerca de 5 GB.')

try:
    import numpy, PIL  # noqa: F401,E401
except ImportError:
    print('A instalar as bibliotecas de imagem do Python...')
    r = subprocess.run([sys.executable, '-m', 'pip', 'install', '--user', '--quiet', 'numpy', 'pillow'], capture_output=True, text=True)
    if r.returncode:
        sys.exit(f'ERRO: não consegui instalar numpy e pillow.\n{r.stderr[-600:]}')
    # Acabadas de instalar, não estão ainda no caminho de procura desta execução.
    import importlib
    import site
    importlib.invalidate_caches()
    sys.path.insert(0, site.getusersitepackages())
print('OK: bibliotecas de imagem')

motor = CASA / 'motor'
motor.mkdir(parents=True, exist_ok=True)
amb = dict(os.environ, PLAYWRIGHT_BROWSERS_PATH=str(CASA / 'browser'))
if not (motor / 'node_modules' / 'playwright-core').exists():
    print('A instalar o motor...')
    r = subprocess.run(f'npm init -y && npm i playwright-core@{PW}', shell=True, cwd=motor, capture_output=True, text=True, errors='replace')
    if r.returncode:
        sys.exit(f'ERRO: não consegui instalar o motor. Confirma a ligação à internet.\n{r.stderr[-600:]}')
browsers = CASA / 'browser'
if not browsers.exists() or not list(browsers.glob('chromium_headless_shell-*')):
    print('A descarregar o navegador que grava os frames, cerca de 100 MB...')
    r = subprocess.run('npx playwright-core install chromium-headless-shell', shell=True, cwd=motor, env=amb, capture_output=True, text=True, errors='replace')
    if r.returncode:
        sys.exit(f'ERRO: não consegui descarregar o navegador. Confirma a ligação à internet.\n{r.stderr[-600:]}')
print('OK: motor e navegador')

# Teste real: cria um carrossel de exemplo e mede quanto demora um frame neste computador.
from marca_lib import carregar_marca, criar_pasta  # noqa: E402

teste = CASA / 'teste'
shutil.rmtree(teste, ignore_errors=True)
criar_pasta(teste, carregar_marca(), SK / 'assets' / 'exemplo' / 'motion.js')


def correr(*args):
    t0 = time.time()
    r = subprocess.run(['node', 'render.mjs', *args], cwd=teste, capture_output=True, text=True, errors='replace')
    if r.returncode:
        sys.exit(f'ERRO: o teste falhou.\n{r.stdout[-400:]}\n{r.stderr[-800:]}')
    return time.time() - t0


# Mede todos os slides em paralelo, como na geração real. Medido num só, dava estimativas muito abaixo do real.
base = correr('--static')
TEMPOS = ','.join(str(x / 4) for x in range(24))
total = correr('--at', TEMPOS)
por_frame = max(0.2, (total - base) / (6 * 24))
minutos = max(5, round(por_frame * 2 * 240 * 8 / 60))  # Medido contra gerações reais: demoram cerca do dobro.
if not list(teste.glob('static/em/*.png')):
    sys.exit('ERRO: o teste correu mas não criou imagens.')
shutil.rmtree(teste, ignore_errors=True)
PRONTO.write_text(json.dumps({'versao': VERSAO, 'testado': str(date.today()), 'segundos_por_frame': round(por_frame, 3), 'minutos_8_slides': minutos}), encoding='utf-8')
print(f'TUDO PRONTO. Neste computador, um carrossel de 8 slides demora cerca de {minutos} minutos a gerar, ou mais com fotos.')
