"""Apaga os frames, que ocupam gigas, depois de os vídeos estarem feitos. Corre dentro da pasta do carrossel.
Os vídeos, a legenda e o código ficam. Para mudar um slide depois, é só voltar a gerá-lo."""
import json
import shutil
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')
if not Path('duracoes.json').exists():
    sys.exit('Corre isto dentro da pasta do carrossel, depois de o gerar.')
n = len(json.loads(Path('duracoes.json').read_text(encoding='utf-8')))
videos = [f'{i:02d}.mp4' for i in range(1, n + 1)]
em_falta = [v for v in videos if not (Path('entrega') / v).exists()]
if em_falta:
    sys.exit(f'Não apago nada: faltam vídeos em entrega/: {", ".join(em_falta)}. Os frames ainda fazem falta.')
total = 0
for d in (Path('frames'), Path('static') / 'em'):
    if d.exists():
        total += sum(f.stat().st_size for f in d.rglob('*') if f.is_file())
        shutil.rmtree(d)
print(f'Libertei {total / 1024 ** 3:.1f} GB. Os {n} vídeos continuam em entrega/.')
