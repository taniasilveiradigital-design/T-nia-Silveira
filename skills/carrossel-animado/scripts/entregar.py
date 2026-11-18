"""Une os frames num MP4 sem áudio por slide e faz a auditoria técnica: frame 0, loop, cantos, formato, duração."""
import sys
sys.stdout.reconfigure(encoding='utf-8')
import json
import shutil
import subprocess
from pathlib import Path

import numpy as np
from PIL import Image, ImageChops

out = Path('entrega')
out.mkdir(exist_ok=True)
if not Path('duracoes.json').exists():
    sys.exit('Ainda não há nada gerado. Corre primeiro node render.mjs.')
cues = json.loads(Path('duracoes.json').read_text(encoding='utf-8'))
ok = True
em_falta = [k for k in cues if len(list(Path(f'frames/s{int(k):02d}').glob('*.png'))) != round(cues[k]['dur'] * 30)]
if em_falta:
    sys.exit(f"Faltam frames dos slides {', '.join(sorted(em_falta, key=int))}. O render não acabou: corre node render.mjs outra vez.")

# python entregar.py --slide 3 refaz só esse vídeo.
alvo = sys.argv[sys.argv.index('--slide') + 1] if '--slide' in sys.argv else None
for key in sorted(cues, key=int):
    if alvo and key != str(int(alvo)):
        continue
    s = int(key)
    tag = f's{s:02d}'
    mp4 = out / f'{s:02d}.mp4'
    subprocess.run(['ffmpeg', '-y', '-hide_banner', '-loglevel', 'error', '-framerate', '30', '-i', f'frames/{tag}/%03d.png',
                    '-vf', 'scale=out_color_matrix=bt709:out_range=tv,format=yuv420p', '-c:v', 'libx264', '-crf', '15', '-preset', 'medium',
                    '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-movflags', '+faststart',
                    '-an', '-t', str(cues[key]['dur']), str(mp4)], check=True)

    frames = sorted(Path(f'frames/{tag}').glob('*.png'))
    first = Image.open(frames[0]).convert('RGB')
    static = Image.open(f'static/{tag}.png').convert('RGB')
    # Tolerância só para arredondamento do navegador ao rasterizar: invisível a olho.
    diff = np.asarray(ImageChops.difference(first, static)).max(axis=2)
    same = int((diff > 0).sum()) <= 15000 and int(diff.max()) <= 8
    drift = f'{int((diff > 0).sum())}px/{int(diff.max())}'
    a = np.asarray(first, dtype=np.int16)
    last = np.asarray(Image.open(frames[-1]).convert('RGB'), dtype=np.int16)
    # A referência não pode usar o último frame: se ele estiver errado, a referência sobe com ele e o erro passa.
    prev = np.asarray(Image.open(frames[-2]).convert('RGB'), dtype=np.int16)
    prev2 = np.asarray(Image.open(frames[-3]).convert('RGB'), dtype=np.int16)
    seam = np.abs(last - a).mean()
    normal = np.abs(prev - prev2).mean()
    cantos = cues[key].get('cantos', [])
    # Um frame diferente dos dois vizinhos, que são iguais entre si, é quase sempre um erro.
    # Movimento muito rápido também o pode dar, por isso é aviso e não falha: vai olhar para esses frames.
    pequenos = [np.asarray(Image.open(f).convert('L').resize((270, 338)), dtype=np.int16) for f in frames]
    isolados = []
    for i in range(len(pequenos)):
        ant, cur, seg = pequenos[i - 1], pequenos[i], pequenos[(i + 1) % len(pequenos)]
        if int(((np.abs(cur - ant) > 25) & (np.abs(cur - seg) > 25) & (np.abs(ant - seg) < 10)).sum()) > 30:
            isolados.append(i)
    # Vários seguidos são movimento rápido. O erro é o frame sozinho, sem vizinhos marcados.
    marcados = set(isolados)
    n_f = len(pequenos)
    isolados = [i for i in isolados if (i - 1) % n_f not in marcados and (i + 1) % n_f not in marcados]
    if isolados:
        print(f"AVISO {s:02d}: frames isolados, confere: {', '.join(f'{i} ({i / 30:.2f} s)' for i in isolados[:12])}")
    probe = json.loads(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'stream=codec_type,width,height,r_frame_rate,pix_fmt,nb_frames:format=duration', '-of', 'json', str(mp4)], capture_output=True, text=True).stdout)
    v = next(x for x in probe['streams'] if x['codec_type'] == 'video')
    seam_ok = seam <= normal * 1.6 + 0.05
    dur_real = float(probe['format']['duration'])
    falhas = []
    if not same: falhas.append('frame 0')
    if not seam_ok: falhas.append('loop')
    if (v['width'], v['height'], v['pix_fmt']) != (1080, 1350, 'yuv420p'): falhas.append('formato')
    n_frames = round(cues[key]['dur'] * 30)
    if v['r_frame_rate'] != '30/1' or abs(dur_real - cues[key]['dur']) > 0.1 or int(v['nb_frames']) != n_frames: falhas.append('duração')
    # A prova final é no MP4 entregue: último contra primeiro, comparado com dois seguidos. Mais dB é mais parecido.
    tmp = out / '_tmp'
    tmp.mkdir(exist_ok=True)
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', str(mp4), '-vf', f"select='eq(n,0)+eq(n,{n_frames - 2})+eq(n,{n_frames - 1})'", '-fps_mode', 'passthrough', str(tmp / 'f%d.png')], check=True)
    f1, f2, f3 = (np.asarray(Image.open(tmp / f'f{i}.png').convert('RGB'), dtype=np.float64) for i in (1, 2, 3))
    psnr = lambda x, y: 99.0 if not np.any(x - y) else 10 * np.log10(255 ** 2 / np.mean((x - y) ** 2))
    db_juncao, db_seguidos = psnr(f3, f1), psnr(f3, f2)
    shutil.rmtree(tmp)
    if db_juncao < 30 and db_juncao < db_seguidos - 3: falhas.append('junção no MP4')
    if any(x['codec_type'] == 'audio' for x in probe['streams']): falhas.append('tem áudio')
    if cantos: falhas.append('texto nos cantos')
    good = not falhas
    ok = ok and good
    print(f"{s:02d}: {'OK ' if good else 'ERRO'} frame0={'igual' if same else 'DIFERENTE'} ({drift}) | emenda {seam:.3f} (normal {normal:.3f}) | "
          f"{v['width']}x{v['height']} {v['r_frame_rate']} {dur_real:.2f}s | junção {db_juncao:.1f} dB (seguidos {db_seguidos:.1f}) | cantos {len(cantos)}" + (f" | FALHA: {', '.join(falhas)}" if falhas else ''))

n = len(cues)
vista = Path('vista-modelo.html').read_text(encoding='utf-8').replace('__TOTAL__', str(n))
Path('vista.html').write_text(vista, encoding='utf-8')
for extra in ('legenda.txt', 'recurso.txt'):
    if Path(extra).exists():
        (out / extra).write_text(Path(extra).read_text(encoding='utf-8'), encoding='utf-8')
print('TUDO OK' if ok else 'HÁ ERROS')
