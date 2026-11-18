"""Folhas de revisão.
python folha.py                 frames 0 (static/_folha.png) e costuras coladas (static/_costuras.png)
Depois de node render.mjs --at, também cria static/_em.png, uma linha por slide.
python folha.py --slide 3       um frame a cada 0,5 s desse slide (static/_tempos3.png). Precisa do render feito."""
import sys
sys.stdout.reconfigure(encoding='utf-8')
import glob
from pathlib import Path
from PIL import Image

if '--slide' in sys.argv:
    s = int(sys.argv[sys.argv.index('--slide') + 1])
    frames = sorted(Path(f'frames/s{s:02d}').glob('*.png'))[::15]
    W, H = 270, 338
    per = 8
    rows = (len(frames) + per - 1) // per
    sheet = Image.new('RGB', (W * per, H * rows), (90, 90, 90))
    for i, f in enumerate(frames):
        sheet.paste(Image.open(f).convert('RGB').resize((W, H), Image.LANCZOS), ((i % per) * W, (i // per) * H))
    sheet.save(f'static/_tempos{s}.png')
    print(f'static/_tempos{s}.png: {len(frames)} frames, um a cada 0,5 s')
    sys.exit()

fs = sorted(glob.glob('static/s[0-9]*.png'))
W, H = 400, 500
per = len(fs) if len(fs) <= 4 else (len(fs) + 1) // 2
linhas_f = (len(fs) + per - 1) // per
sheet = Image.new('RGB', (W * per, H * linhas_f + 12 * (linhas_f - 1)), (90, 90, 90))
for i, f in enumerate(fs):
    sheet.paste(Image.open(f).convert('RGB').resize((W, H), Image.LANCZOS), ((i % per) * W, (i // per) * (H + 12)))
sheet.save('static/_folha.png')

# Cada par mostra o fim de um slide colado ao início do seguinte, com um espaço entre pares.
CW, CH = 200, 500
pares = len(fs) - 1
cost = Image.new('RGB', (max(1, pares) * (CW * 2 + 16), CH), (90, 90, 90))
for i in range(pares):
    a = Image.open(fs[i]).convert('RGB').crop((1080 - 432, 0, 1080, 1350)).resize((CW, CH), Image.LANCZOS)
    b = Image.open(fs[i + 1]).convert('RGB').crop((0, 0, 432, 1350)).resize((CW, CH), Image.LANCZOS)
    cost.paste(a, (i * (CW * 2 + 16), 0))
    cost.paste(b, (i * (CW * 2 + 16) + CW, 0))
cost.save('static/_costuras.png')
print(f'static/_folha.png e static/_costuras.png: {len(fs)} slides')

em = sorted(glob.glob('static/em/s*.png'))
if em:
    linhas = sorted({Path(f).name.split('_')[0] for f in em})
    colunas = sorted({Path(f).stem.split('_')[1] for f in em}, key=float)
    W, H = 300, 375
    if len(colunas) <= 8:
        sheet = Image.new('RGB', (W * len(colunas), H * len(linhas)), (90, 90, 90))
        for f in em:
            a, b = Path(f).stem.split('_')
            sheet.paste(Image.open(f).convert('RGB').resize((W, H), Image.LANCZOS), (colunas.index(b) * W, linhas.index(a) * H))
        sheet.save('static/_em.png')
        print(f'static/_em.png: {len(linhas)} slides nos segundos {", ".join(colunas)}')
    else:
        # Muitos tempos numa só linha ficam ilegíveis: uma folha por slide, com 8 por linha.
        for g in glob.glob('static/_em_s*.png'):
            Path(g).unlink()
        rows = (len(colunas) + 7) // 8
        for linha in linhas:
            sheet = Image.new('RGB', (W * 8, H * rows), (90, 90, 90))
            for f in em:
                a, b = Path(f).stem.split('_')
                if a == linha:
                    i = colunas.index(b)
                    sheet.paste(Image.open(f).convert('RGB').resize((W, H), Image.LANCZOS), ((i % 8) * W, (i // 8) * H))
            sheet.save(f'static/_em_{linha}.png')
        print(f'static/_em_s01.png e seguintes: uma folha por slide, nos segundos {", ".join(colunas)}')
