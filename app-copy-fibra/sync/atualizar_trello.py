import json, re, sys, os, datetime
sys.path.insert(0, '/home/user/T-nia-Silveira/app-copy-fibra/sync')
from secoes import parse
V = {'d2026-10-12':22,'d2026-10-13':30,'d2026-10-14':10,'d2026-10-15':19,'d2026-10-16':13,'d2026-10-17':11,'d2026-10-19':20,'d2026-10-20':4,'d2026-10-21':8,'d2026-10-22':11,'d2026-10-23':40,'d2026-11-02':4,'d2026-11-25':4}
VC = {'p2026-10-12':3,'p2026-10-13':1,'p2026-10-14':1,'p2026-10-15':2,'p2026-10-16':3,'p2026-10-17':3}
L3 = '../live3'
NOW = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.000Z')
d = json.load(open('board.json'))
cards = {o['id']: o for o in json.load(open('conteudos.json'))}
feed = json.load(open('feedcopy.json'))
cl = {}
for c in d['checklists']: cl.setdefault(c['idCard'], []).append(c)
raw = {c['id']: c for c in d['cards']}
def stories_txt(cid):
    out = []
    for ch in sorted(cl.get(cid, []), key=lambda c: c['pos']):
        cur = []; nome = ch['name'].strip()
        if not re.search(r'(?i)stories', nome): cur.append(nome.upper())
        for it in [i['name'].strip() for i in sorted(ch['checkItems'], key=lambda i: i['pos'])]:
            m = re.fullmatch(r'\*\*(.+?)\*\*:?', it)
            if m:
                if cur: out.append('\n'.join(cur))
                cur = [m.group(1).strip().upper()]
            elif it: cur.append('- ' + it)
        if cur: out.append('\n'.join(cur))
    return '\n\n'.join(out)
def fixcopy(t, fmt):
    t = re.sub(r'(?m)^\*\*((?:Slide|Cena)\s*\d+)\s*:?\*\*\s*:?\s*$', r'## \1', t)
    if t and not t.lstrip().startswith('## '):
        t = ('## Roteiro\n' if fmt == 'Reels' else '## Copy\n') + t
    return t.strip()
wk_re = re.compile(r'(\d+)\s+(?:de|se)\s+(\w+)\s+a\s+(\d+)\s+de\s+(\w+)', re.I)
day_re = re.compile(r'^(segunda|terça|terca|quarta|quinta|sexta|sábado|sabado|domingo)\b', re.I)
lw = {}
for o in cards.values():
    if o['semana']: lw[raw[o['id']]['idList']] = o['semana']
notas = {}
for c in sorted(d['cards'], key=lambda c: c['pos']):
    if c['closed'] or c['idList'] not in lw: continue
    n = c['name'].strip()
    if wk_re.search(n) or day_re.match(n) or n in ('.', ''): continue
    if lw[c['idList']] < '2026-10-12': continue
    notas.setdefault(lw[c['idList']], []).append(n + (('\n' + c['desc'].strip()) if c['desc'].strip() else ''))
writes = []; rel = []
for cid, o in sorted(cards.items(), key=lambda x: x[1]['data'] or ''):
    if not o['data'] or o['data'] < '2026-10-12': continue
    k = 'd' + o['data']; f = f'{L3}/plano/{k}.json'
    if not os.path.exists(f): continue
    L = json.load(open(f)); upd = {}; what = []
    if o['cartao'] and L.get('cartao') != o['cartao']: upd.update(cartao=o['cartao'], secoes=parse(o['cartao'])); what.append('cartão')
    st = stories_txt(cid)
    if st and st != (L.get('stories') or ''): upd['stories'] = st; what.append('checklist stories')
    if o['inspiracao'] and o['inspiracao'] != L.get('inspiracao'): upd['inspiracao'] = o['inspiracao']
    if L.get('titulo') != o['titulo']: upd['titulo'] = o['titulo']
    if o['formato'] in ('Reels','Carrossel','Só stories','Live') and L.get('formato') != o['formato'] and not L.get('formato'): upd['formato'] = o['formato']
    upd.update(trello=o['trello'], trelloId=cid)
    have = {re.sub(r'\W+', '', c.get('texto') or '')[:80] for c in (L.get('comentarios') or [])}
    novos = [{'autor': 'Sarah' if re.search(r'sarah', c['quem'], re.I) else 'Tânia', 'texto': c['texto'], 'data': c['data'] + 'T12:00:00.000Z', 'alvo': 'feed', 'origem': 'trello', 'aplicado': True}
             for c in o['comentarios'] if re.sub(r'\W+', '', c['texto'])[:80] not in have]
    if novos: upd['comentarios'] = (L.get('comentarios') or []) + novos; what.append(f'{len(novos)} coment.')
    aprovado = any(re.search(r'(?i)aprovad', c['texto']) and re.search(r'(?i)sarah', c['quem']) for c in o['comentarios'])
    fc = fixcopy(feed.get(o['data'], ''), L.get('formato') or o['formato'])
    if o['data'] <= '2026-11-21' and fc and fc.strip() != (L.get('copy') or '').strip():
        vs = L.get('versoes') or []
        if L.get('copy'): vs = (vs + [{'em': NOW, 'copy': L['copy'], **({'feito': L['copyRev']['em'], 'como': L['copyRev'].get('como', '')} if L.get('copyRev') else {})}])[-12:]
        upd.update(copy=fc, versoes=vs, copyRev={'em': NOW, 'como': 'copy final do Trello'}); what.append('COPY FEED')
    if aprovado and L.get('estado') in ('Por fazer', 'Rascunho', 'Para a Sarah'): upd['estado'] = 'Aprovado'; what.append('aprovado')
    elif L.get('estado') == 'Por fazer' and (upd.get('copy') or L.get('copy')): upd['estado'] = 'Para a Sarah'
    nota = '\n\n'.join(notas.get(o['semana'], []))
    if nota and nota != L.get('semanaNota'): upd['semanaNota'] = nota
    if len(upd) > 2:
        upd['atualizado'] = NOW
        writes.append({'op': 'update', 'collection': 'plano', 'doc_id': k, 'data': upd, 'if_version': V.get(k, 2)})
        rel.append(f"{o['data']} {o['titulo'][:40]} :: {', '.join(what)}")
    # conteúdos
    cf = f'{L3}/conteudos/p{o["data"]}.json'
    if os.path.exists(cf) and 'copy' in upd:
        C = json.load(open(cf))
        cvs = (C.get('versoes') or []) + ([{'em': NOW, 'copy': C['copy']}] if C.get('copy') else [])
        writes.append({'op': 'update', 'collection': 'conteudos', 'doc_id': 'p' + o['data'], 'data': {'copy': upd['copy'], 'versoes': cvs[-12:], 'copyRev': upd['copyRev'], 'cartao': o['cartao'], 'secoes': parse(o['cartao']), 'atualizado': NOW}, 'if_version': VC['p' + o['data']]})
print('\n'.join(rel)); print(len(writes), 'writes')
os.makedirs('up', exist_ok=True); ents = []
for w in writes:
    p = os.path.abspath(f"up/{w['collection']}_{w['doc_id']}.json"); json.dump(w['data'], open(p, 'w'), ensure_ascii=False)
    ents.append({'op': 'update', 'collection': w['collection'], 'doc_id': w['doc_id'], 'file_path': p, 'if_version': w['if_version']})
json.dump(ents, open('batch.json', 'w'), ensure_ascii=False)
