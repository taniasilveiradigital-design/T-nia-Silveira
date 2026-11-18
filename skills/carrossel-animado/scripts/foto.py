"""Prepara uma imagem para um slide: fotos/fN.jpg e o recorte fotos/fN.png, com a pessoa sem fundo.
Corre dentro da pasta do carrossel.

python foto.py 1 "caminho/foto.jpg"
python foto.py 2 "caminho/video.MOV" --t 28      usa o frame do segundo 28
python foto.py 3 "caminho/foto.jpg" --sem-recorte

O recorte corre no computador. Da primeira vez, descarrega um modelo de cerca de 170 MB."""
import argparse
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageOps

sys.stdout.reconfigure(encoding='utf-8')
ap = argparse.ArgumentParser()
ap.add_argument('n', type=int)
ap.add_argument('origem')
ap.add_argument('--t', type=float, default=None)
ap.add_argument('--sem-recorte', action='store_true')
a = ap.parse_args()

orig = Path(a.origem).expanduser()
if not orig.exists():
    sys.exit(f'Não encontro: {orig}')
Path('fotos').mkdir(exist_ok=True)
jpg = Path('fotos') / f'f{a.n}.jpg'
VIDEO = {'.mov', '.mp4', '.m4v', '.webm', '.mkv'}
sufixo = orig.suffix.lower()

if sufixo in VIDEO:
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-ss', str(a.t or 0), '-i', str(orig), '-frames:v', '1', '-q:v', '2', str(jpg)], check=True)
elif sufixo in {'.heic', '.heif'}:
    # As fotos de iPhone: o Python não as abre, mas o ffmpeg recente sim.
    r = subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', str(orig), '-frames:v', '1', '-q:v', '2', str(jpg)], capture_output=True)
    if r.returncode or not jpg.exists():
        sys.exit('Não consegui abrir esta foto de iPhone (HEIC). Exporta-a como JPG e volta a tentar.')
else:
    try:
        im = ImageOps.exif_transpose(Image.open(orig)).convert('RGB')
    except OSError:
        sys.exit(f'Não consegui abrir {orig.name}. Exporta a imagem como JPG ou PNG e volta a tentar.')
    # Mantém o detalhe: 1600 px de largura chegam para um slide de 1080 com folga para o zoom.
    if im.width > 1600:
        im = im.resize((1600, round(im.height * 1600 / im.width)), Image.LANCZOS)
    im.save(jpg, quality=93)

im = Image.open(jpg)
print(f'{jpg}: {im.width}x{im.height}.')
if im.width < 1080:
    print('AVISO: menos de 1080 px de largura. Vai ficar mole no slide.')
if im.width >= im.height:
    print('AVISO: foto deitada. Numa cena de slide inteiro perde muito dos lados, por isso vê como fica ou pede uma vertical.')
if not a.sem_recorte:
    png = jpg.with_suffix('.png')
    r = subprocess.run(f'npx -y hyperframes@0.8.200 remove-background "{jpg}" -o "{png}"', shell=True, capture_output=True, text=True, encoding='utf-8', errors='replace')
    if r.returncode or not png.exists():
        sys.exit(f'O recorte falhou. Confirma a ligação à internet e volta a tentar.\n{r.stdout[-800:]}\n{r.stderr[-800:]}')
    print(f'{png}: recorte feito. Vê-o sobre fundo liso antes de o usar fora da própria foto.')
