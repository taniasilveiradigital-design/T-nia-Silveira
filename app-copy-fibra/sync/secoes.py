import re
HEAD = [
 ('Feed', r'feed'), ('Objetivo', r'objetivo'), ('Estratégia', r'estrat[ée]gia'), ('Tema', r'tema|inspira[çc][ãa]o de tema'),
 ('Gancho', r'gancho|ideia de in[ií]cio'), ('Como fazer', r'como fazer|como criar|como trazer|direcionamento|o que trazer|o que fazer|o que precisa ser abordado|possíveis ideias|poss[ií]veis ideias|sugest[ãa]o de pilares[^\n]*|trazer os pontos'),
 ('Copy retificado', r'copp?y retificado|novo copp?y|copp?y atualizado'), ('Copy', r'copp?y'),
 ('Template', r'template|tamplate|templete|template capa|capa reels|capa|atualizado'), ('Inspiração', r'inspira[çc][ãa]o(,)?( de formato| de conte[úu]do)?|an[aá]lise desse v[ií]deo|reels'),
 ('Observações', r'observa[çc][õo]es'), ('Prints', r'prints'), ('Título no vídeo', r't[ií]tulo no v[ií]deo'),
]
HRE = re.compile(r'^\s*(?:#+\s*)?[\*_]*\s*(' + '|'.join(p for _, p in HEAD) + r')\s*[\*_]*\s*:?\s*[\*_]*\s*:?\s*$', re.I)
def label(h):
    for name, p in HEAD:
        if re.fullmatch(p, h.strip(), re.I): return name
    return h
def parse(desc):
    lines = desc.split('\n'); out = []; cur = None; buf = []
    def flush():
        txt = '\n'.join(buf).strip().strip('-').strip()
        txt = re.sub(r'\n{3,}', '\n\n', txt)
        if cur or txt:
            if txt or cur: out.append({'titulo': cur or 'Introdução', 'texto': txt})
    for ln in lines:
        m = HRE.match(ln)
        if m:
            flush(); cur = label(m.group(1)); buf = []
        elif ln.strip() in ('---', '‌'): buf.append('')
        else: buf.append(ln)
    flush()
    # se não houver Copy mas houver slides/cenas/pontos dentro de outra secção, separa
    if not any(s['titulo'].startswith('Copy') for s in out):
        for i, s in enumerate(out):
            mm = re.search(r'(?im)^\s*[\*_>]*\s*(slide|cena|ponto)\s*1\b', s['texto'])
            if mm:
                antes, depois = s['texto'][:mm.start()].strip(), s['texto'][mm.start():].strip()
                novo = [{'titulo': s['titulo'], 'texto': antes}] if antes else []
                novo.append({'titulo': 'Copy', 'texto': depois})
                out[i:i+1] = novo; break
    # "Template"/"Capa"/"Inspiração" seguidos apenas de link: manter
    return [s for s in out if s['texto'] or s['titulo'] not in ('Introdução',)]
