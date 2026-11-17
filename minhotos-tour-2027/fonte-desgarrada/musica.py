# Vira original em Sol maior, 3/4, 1 compasso = 1 s. Gera musica.wav e estrutura.json
import numpy as np, json, wave
SR = 44100
BAR = 1.0
E = BAR / 6  # colcheia

NOTE = {'C': 0, 'C#': 1, 'D': 2, 'D#': 3, 'E': 4, 'F': 5, 'F#': 6, 'G': 7, 'G#': 8, 'A': 9, 'A#': 10, 'B': 11}
def hz(n):
    name, octv = n[:-1], int(n[-1])
    return 440 * 2 ** ((NOTE[name] + 12 * (octv + 1) - 69) / 12)

CH = {'G': ['G', 'B', 'D'], 'D': ['D', 'F#', 'A'], 'C': ['C', 'E', 'G'], 'D7': ['D', 'F#', 'C']}
BASS = {'G': ('G2', 'D2'), 'D': ('D2', 'A2'), 'C': ('C3', 'G2'), 'D7': ('D2', 'A2')}

VERSO = (['G', 'D', 'D', 'G', 'G', 'C', 'D7', 'G'], [
    [('B4', 2), ('D5', 1), ('B4', 1), ('G4', 2)],
    [('A4', 2), ('C5', 1), ('A4', 1), ('F#4', 2)],
    [('A4', 1), ('B4', 1), ('C5', 2), ('B4', 1), ('A4', 1)],
    [('B4', 4), ('G4', 2)],
    [('B4', 2), ('D5', 1), ('B4', 1), ('D5', 2)],
    [('E5', 2), ('D5', 1), ('C5', 1), ('E5', 2)],
    [('D5', 1), ('C5', 1), ('B4', 2), ('A4', 2)],
    [('G4', 6)]])
REFRAO = (['G', 'G', 'D', 'D', 'D7', 'D7', 'G', 'G'], [
    [('D5', 1), ('D5', 1), ('B4', 1), ('B4', 1), ('G4', 2)],
    [('B4', 1), ('C5', 1), ('D5', 4)],
    [('C5', 1), ('C5', 1), ('A4', 1), ('A4', 1), ('F#4', 2)],
    [('A4', 1), ('B4', 1), ('C5', 4)],
    [('C5', 1), ('B4', 1), ('A4', 2), ('D5', 2)],
    [('C5', 1), ('B4', 1), ('A4', 2), ('F#4', 2)],
    [('G4', 1), ('A4', 1), ('B4', 2), ('A4', 2)],
    [('G4', 6)]])
FIM = (['G', 'D7', 'G', 'G'], [[('D5', 1), ('B4', 1), ('G4', 4)], [('A4', 1), ('C5', 1), ('F#4', 4)], [('G4', 2), ('G4', 1), ('G4', 3)], [('G5', 6)]])

# secções: (nome, bloco, voz da melodia)  ele = concertina, ela = cavaquinho oitava acima, ambos = os dois
PLANO = [('intro', REFRAO, 'ambos'), ('ele1', VERSO, 'ele'), ('ela1', VERSO, 'ela'), ('ele2', VERSO, 'ele'),
         ('ela2', VERSO, 'ela'), ('refrao1', REFRAO, 'ambos'), ('refrao2', REFRAO, 'ambos'), ('fim', FIM, 'ambos')]

total_bars = sum(len(b[0]) for _, b, _ in PLANO)
N = int((total_bars * BAR + 2.5) * SR)
mel, ac, cav, bass, drum = (np.zeros(N) for _ in range(5))
t_all = np.arange(N) / SR

def env(n, a=.012, r=.05):
    e = np.ones(n); ai = max(1, int(a * SR)); ri = max(1, int(r * SR))
    e[:ai] = np.linspace(0, 1, ai); e[-ri:] *= np.linspace(1, 0, ri); return e

def reed(f, dur, bright=1.0):
    n = int(dur * SR); t = np.arange(n) / SR; out = np.zeros(n)
    for det in (-.0032, 0, .0036):          # 3 palhetas desafinadas = musette
        ff = f * (1 + det)
        for k in range(1, 14):
            if ff * k > 9000: break
            out += np.sin(2 * np.pi * ff * k * t + k * det * 50) * (1 / k ** (1.15 / bright)) * (1.15 if k % 2 else .8)
    return out * env(n) * (1 + .04 * np.sin(2 * np.pi * 5.5 * t))

def pluck(f, dur):
    n = int(dur * SR); t = np.arange(n) / SR; out = np.zeros(n)
    for k in range(1, 10):
        out += np.sin(2 * np.pi * f * k * t) * np.exp(-t * (6 + k * 3)) / k
    return out * env(n, .002, .02)

def add(buf, start, sig, g=1.0):
    i = int(start * SR); j = min(N, i + len(sig)); buf[i:j] += sig[:j - i] * g

estrutura = []; pos = 0.0
for nome, (chords, melody), voz in PLANO:
    estrutura.append({'nome': nome, 'inicio': pos, 'compassos': len(chords), 'voz': voz})
    for b, (ch, notes) in enumerate(zip(chords, melody)):
        t0 = pos + b * BAR
        # melodia
        tt = t0
        for nt, d in notes:
            dur = d * E
            if voz in ('ele', 'ambos'):
                add(mel, tt, reed(hz(nt), dur * .96), .22)
            if voz in ('ela', 'ambos'):
                f = hz(nt) * 2
                # cavaquinho: palhetada em colcheias (rasgado/tremolo)
                k = 0
                while k * E < dur - 1e-6:
                    add(cav, tt + k * E, pluck(f, min(E * 1.6, dur - k * E + .05)), .20 if voz == 'ela' else .11)
                    k += 1
            tt += dur
        # mão esquerda: baixo no 1º tempo, acorde no 2º e 3º
        bnote = BASS[ch][b % 2]
        add(bass, t0, reed(hz(bnote), 2 * E * .9, .6), .30)
        for beat in (1, 2):
            for nn in CH[ch]:
                add(ac, t0 + beat * 2 * E, reed(hz(nn + '3') if nn in ('C', 'D') else hz(nn + '3'), 2 * E * .55, .8), .06)
        # bombo no 1, ferrinhos em todas as colcheias com acento nos tempos
        n = int(.25 * SR); tk = np.arange(n) / SR
        kick = np.sin(2 * np.pi * (50 * tk + 70 / 18 * (1 - np.exp(-18 * tk)))) * np.exp(-tk * 14)
        add(drum, t0, kick, .9 if b % 2 == 0 else .6)
        for e8 in range(6):
            n2 = int(.12 * SR); tf = np.arange(n2) / SR
            tri = (np.sin(2 * np.pi * 4180 * tf) + .7 * np.sin(2 * np.pi * 5530 * tf) + .5 * np.sin(2 * np.pi * 6890 * tf)) * np.exp(-tf * (30 if e8 % 2 else 14))
            add(drum, t0 + e8 * E, tri, (.10 if e8 % 2 == 0 else .05) * (1.4 if e8 == 0 else 1))
    pos += len(chords) * BAR

mix = mel + cav + ac + bass + drum
# reverb simples (convolução com ruído decrescente)
irn = int(1.6 * SR); rng = np.random.default_rng(3)
ir = rng.standard_normal(irn) * np.exp(-np.arange(irn) / SR * 4.2); ir[0] = 0
L = 1 << int(np.ceil(np.log2(N + irn)))
wet = np.fft.irfft(np.fft.rfft(mix, L) * np.fft.rfft(ir, L), L)[:N]
wet /= np.max(np.abs(wet)) + 1e-9
out = mix / (np.max(np.abs(mix)) + 1e-9) + .18 * wet
out = np.tanh(out * 1.3)
out /= np.max(np.abs(out)); out *= .89
fade = int(1.5 * SR); out[-fade:] *= np.linspace(1, 0, fade)
# estéreo ligeiro: cavaquinho à direita, concertina à esquerda
l = out + .15 * (mel - cav) / (np.max(np.abs(mel - cav)) + 1e-9) * .3
r = out - .15 * (mel - cav) / (np.max(np.abs(mel - cav)) + 1e-9) * .3
st = np.stack([l, r], 1); st /= np.max(np.abs(st)); st *= .9
with wave.open('musica.wav', 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((st * 32767).astype('<i2').tobytes())
json.dump({'bar': BAR, 'secoes': estrutura, 'total': pos}, open('estrutura.json', 'w'), indent=1)
print('ok', pos, 's')
