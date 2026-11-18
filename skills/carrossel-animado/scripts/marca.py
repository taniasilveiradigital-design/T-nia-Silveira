"""Confirma a marca guardada em ~/.carrossel-animado/marca.json e cria uma amostra para a aluna aprovar.
Uso: python marca.py
Sem problemas, cria amostra/static/_folha.png dentro dessa pasta e diz o caminho."""
import json
import shutil
import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, str(Path(__file__).resolve().parent))
from marca_lib import CASA, MARCA, SK, criar_pasta, validar  # noqa: E402

if not MARCA.exists():
    sys.exit(f'Ainda não há marca guardada em {MARCA}. Vê references/marca.md.')
try:
    marca = json.loads(MARCA.read_text(encoding='utf-8'))
except json.JSONDecodeError as e:
    sys.exit(f'O ficheiro da marca tem um erro de escrita: {e}')
erros = validar(marca)
if erros:
    print('A MARCA PRECISA DE AJUSTES:')
    for e in erros:
        print(f'- {e}')
    sys.exit(2)

pasta = CASA / 'amostra'
shutil.rmtree(pasta, ignore_errors=True)
criar_pasta(pasta, marca, SK / 'assets' / 'template' / 'amostra.js')
r = subprocess.run(['node', 'render.mjs', '--static'], cwd=pasta, capture_output=True, text=True, errors='replace')
if r.returncode:
    sys.exit(f'A amostra falhou.\n{r.stdout[-400:]}\n{r.stderr[-800:]}')
subprocess.run([sys.executable, 'folha.py'], cwd=pasta, check=True, capture_output=True)
if r.stdout.strip():
    print(r.stdout.strip())
print(f'MARCA OK. Amostra: {pasta / "static" / "_folha.png"}')
