"""Cria a pasta de um carrossel novo, com a marca da aluna.
Uso: python novo.py nome-do-carrossel [--dest PASTA] [--exemplo]
Por defeito, cria em ~/Carrosseis. --exemplo traz um carrossel completo, sem fotos, para ver o motor a funcionar."""
import argparse
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, str(Path(__file__).resolve().parent))
from marca_lib import MARCA, PRONTO, SK, carregar_marca, criar_pasta, validar  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument('nome')
ap.add_argument('--dest', default=str(Path.home() / 'Carrosseis'))
ap.add_argument('--exemplo', action='store_true')
a = ap.parse_args()

if not PRONTO.exists():
    sys.exit('O computador ainda não está preparado. Corre primeiro verificar.py.')
if not MARCA.exists() and not a.exemplo:
    sys.exit('Ainda não há marca guardada. Faz primeiro o passo da marca (references/marca.md).')
marca = carregar_marca()
erros = validar(marca)
if erros:
    sys.exit('A marca precisa de ajustes: ' + ' '.join(erros))

nome = re.sub(r'[<>:"/\\|?*]', '-', a.nome).strip()
pasta = Path(a.dest).expanduser().resolve() / nome
if pasta.exists():
    sys.exit(f'Já existe: {pasta}. Escolhe outro nome, não escrevo por cima.')
pasta.parent.mkdir(parents=True, exist_ok=True)
criar_pasta(pasta, marca, SK / 'assets' / 'exemplo' / 'motion.js' if a.exemplo else None)
print(f'Pronto: {pasta}')
print('slides.js traz o exemplo completo.' if a.exemplo else 'slides.js é um ponto de partida. Substitui-o pelo carrossel novo.')
