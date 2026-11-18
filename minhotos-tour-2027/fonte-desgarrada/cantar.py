# Gera vozes.wav: voz pt-PT (Piper) afinada à melodia do vira com WORLD
import numpy as np, soundfile as sf, pyworld as pw, subprocess, os, warnings
warnings.filterwarnings('ignore')
D = os.path.dirname(os.path.abspath(__file__))
VOZ = os.path.join(D, '..', 'vozes', 'pt_PT-tugão-medium.onnx')
PIPER = os.path.join(D, '..', 'voz-venv', 'bin', 'piper')
FS = 22050; E = 1 / 6; FP = 5.0

NOTE = {'C': 0, 'C#': 1, 'D': 2, 'D#': 3, 'E': 4, 'F': 5, 'F#': 6, 'G': 7, 'G#': 8, 'A': 9, 'A#': 10, 'B': 11}
def hz(n): return 440 * 2 ** ((NOTE[n[:-1]] + 12 * (int(n[-1]) + 1) - 69) / 12)
VERSO = [[('B4', 2), ('D5', 1), ('B4', 1), ('G4', 2)], [('A4', 2), ('C5', 1), ('A4', 1), ('F#4', 2)],
         [('A4', 1), ('B4', 1), ('C5', 2), ('B4', 1), ('A4', 1)], [('B4', 4), ('G4', 2)],
         [('B4', 2), ('D5', 1), ('B4', 1), ('D5', 2)], [('E5', 2), ('D5', 1), ('C5', 1), ('E5', 2)],
         [('D5', 1), ('C5', 1), ('B4', 2), ('A4', 2)], [('G4', 6)]]
REFRAO = [[('D5', 1), ('D5', 1), ('B4', 1), ('B4', 1), ('G4', 2)], [('B4', 1), ('C5', 1), ('D5', 4)],
          [('C5', 1), ('C5', 1), ('A4', 1), ('A4', 1), ('F#4', 2)], [('A4', 1), ('B4', 1), ('C5', 4)],
          [('C5', 1), ('B4', 1), ('A4', 2), ('D5', 2)], [('C5', 1), ('B4', 1), ('A4', 2), ('F#4', 2)],
          [('G4', 1), ('A4', 1), ('B4', 2), ('A4', 2)], [('G4', 6)]]
# texto para a voz (escrita fonética onde ajuda)
LETRA = {
 'ele1': ['Já fiz dezoito menina', 'já posso entrar no baile', 'quem quiser que me acompanhe', 'quem não quiser que se cale'],
 'ela1': ['Dezoito anos rapaz', 'não te ponhas com vaidade', 'que eu já danço a desgarrada', 'desde antes da maioridade'],
 'ele2': ['Ó menina não me tentes', 'que eu sou diabo do Minho', 'trago os cornos trago o rabo', 'e a festa pelo caminho'],
 'ela2': ['Se és diabo eu sou diaba', 'e de nós dois a pior', 'tu tens cornos de enfeite', 'eu tenho o rabo maior'],
 'refrao1': ['Viramos? Viramos sim', 'dezoito anos a virar', 'túr dezoito mais na estrada', 'ninguém fica sem dançar'],
 'refrao2': ['Viramos? Viramos sim', 'põe o lenço aperta o laço', 'que em vinte e sete os diabos', 'vão virar de braço em braço'],
}
PLANO = [('ele1', 8, VERSO, ['ele']), ('ela1', 16, VERSO, ['ela']), ('ele2', 24, VERSO, ['ele']),
         ('ela2', 32, VERSO, ['ela']), ('refrao1', 40, REFRAO, ['ele', 'ela']), ('refrao2', 48, REFRAO, ['ele', 'ela'])]

def tts(text, speed=1.0):
    out = os.path.join(D, '_tmp.wav')
    subprocess.run([PIPER, '-m', VOZ, '-f', out, '--length-scale', str(speed)], input=text.encode(), check=True, capture_output=True)
    x, fs = sf.read(out); assert fs == FS
    e = np.convolve(np.abs(x), np.ones(400) / 400, 'same'); idx = np.where(e > .02 * e.max())[0]
    return x[max(0, idx[0] - 200): idx[-1] + 200]

def melody_f0(bars, n, dur, voice):
    times = np.arange(n) * FP / 1000
    sched = []; t = 0
    for bar in bars:
        for note, d in bar: sched.append((t, t + d * E, hz(note))); t += d * E
    f = np.zeros(n)
    for a, z, h in sched:
        m = (times >= a * dur / (len(bars))) & (times < z * dur / (len(bars)))  # escala os 2 compassos para 'dur'
        f[m] = h
    f[f == 0] = sched[-1][2]
    if voice == 'ele': f = f / 2
    # vibrato e portamento
    f = f * 2 ** (.35 / 12 * np.sin(2 * np.pi * 5.6 * times) * np.clip((times % 1) * 2, 0, 1))
    k = 7; f = np.convolve(np.pad(f, (k, k), 'edge'), np.ones(2 * k + 1) / (2 * k + 1), 'valid')
    return f

def sing(text, bars, voice, dur=1.92):
    x = tts(text, 1.0).astype(np.float64)
    f0, t = pw.harvest(x, FS, frame_period=FP, f0_floor=60, f0_ceil=500)
    sp = pw.cheaptrick(x, f0, t, FS); ap = pw.d4c(x, f0, t, FS)
    n = int(dur * 1000 / FP)
    src = np.linspace(0, len(f0) - 1, n)
    i0 = np.floor(src).astype(int); i1 = np.minimum(i0 + 1, len(f0) - 1); w = (src - i0)[:, None]
    sp2 = sp[i0] * (1 - w) + sp[i1] * w; ap2 = ap[i0] * (1 - w) + ap[i1] * w
    voiced = (f0[np.round(src).astype(int)] > 0)
    # suaviza a máscara para não cortar sílabas
    voiced = np.convolve(voiced.astype(float), np.ones(5) / 5, 'same') > .3
    f2 = melody_f0(bars, n, dur, voice) * voiced
    if voice == 'ela':  # desloca formantes para cima
        a = 1.17; bins = sp2.shape[1]; srcb = np.clip(np.arange(bins) / a, 0, bins - 1)
        b0 = np.floor(srcb).astype(int); b1 = np.minimum(b0 + 1, bins - 1); wb = srcb - b0
        sp2 = sp2[:, b0] * (1 - wb) + sp2[:, b1] * wb
        ap2 = ap2[:, b0] * (1 - wb) + ap2[:, b1] * wb
    y = pw.synthesize(np.ascontiguousarray(f2), np.ascontiguousarray(sp2), np.ascontiguousarray(ap2), FS, FP)
    return y / (np.max(np.abs(y)) + 1e-9)

TOTAL = 61.0
track = {'ele': np.zeros(int(TOTAL * FS)), 'ela': np.zeros(int(TOTAL * FS))}
for nome, start, mel, vozes in PLANO:
    for i, line in enumerate(LETRA[nome]):
        bars = mel[2 * i: 2 * i + 2]
        for v in vozes:
            y = sing(line, bars, v) * (.75 if len(vozes) > 1 else 1)
            a = int((start + 2 * i + .02) * FS); track[v][a:a + len(y)] += y[:len(track[v]) - a]
        print(nome, i, flush=True)
sf.write(os.path.join(D, 'voz_ele.wav'), track['ele'] * .8, FS)
sf.write(os.path.join(D, 'voz_ela.wav'), track['ela'] * .8, FS)
os.remove(os.path.join(D, '_tmp.wav'))
