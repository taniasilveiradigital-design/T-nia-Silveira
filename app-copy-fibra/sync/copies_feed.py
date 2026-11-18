import json, re, sys
sys.path.insert(0, '/home/user/T-nia-Silveira/app-copy-fibra/sync')
from secoes import parse
cs = {o['data']: o for o in json.load(open('conteudos.json')) if o['data'] and '2026-10-12' <= o['data'] <= '2026-11-21'}
def norm(t):
    t = re.sub(r'(?m)^#{2,}\s*\n+\s*(Slide|Cena|Ponto)', r'## \1', t)
    t = re.sub(r'(?m)^#{1,6}\s*', '## ', t)
    t = re.sub(r'(?m)^\*\*(Slide\s*\d+|Cena\s*\d+)\*\*\s*$', r'## \1', t)
    t = re.sub(r'(?m)^(Slide\s*\d+)\s*:?\s*$', r'## \1', t)
    t = re.sub(r'!\[[^\]]*\]\([^)]*\)', '', t)
    return re.sub(r'\n{3,}', '\n\n', t).strip()
out = {}
for k, o in sorted(cs.items()):
    secs = parse(o['cartao'])
    cand = [s for s in secs if s['titulo'] == 'Copy retificado'] or [s for s in secs if s['titulo'] == 'Copy']
    txt = cand[-1]['texto'] if cand else ''
    if len(o['copy']) > len(txt) and not any(s['titulo'] == 'Copy retificado' for s in secs): txt = o['copy']
    txt = norm(txt)
    out[k] = txt
    print(k, o['formato'][:9], len(txt), repr(txt[:90]))
json.dump(out, open('feedcopy.json', 'w'), ensure_ascii=False)
