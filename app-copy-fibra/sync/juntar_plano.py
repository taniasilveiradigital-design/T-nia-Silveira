import json, sys, re, os, datetime
sys.path.insert(0, '..')
from secoes import parse
SP = '..'
d = json.load(open('board.json'))
cards = {o['id']: o for o in json.load(open('conteudos.json'))}
seed = json.load(open('../plano.json'))
V = {'d2026-10-12': 20, 'd2026-10-13': 29, 'd2026-10-14': 7, 'd2026-10-15': 15, 'd2026-10-16': 7, 'd2026-10-17': 4, 'd2026-10-19': 17}
raw = {c['id']: c for c in d['cards']}
lists = {l['id']: l for l in d['lists']}
cl = {}
for c in d['checklists']: cl.setdefault(c['idCard'], []).append(c)
def stories_txt(cid):
    out = []
    for ch in sorted(cl.get(cid, []), key=lambda c: c['pos']):
        items = [i['name'].strip() for i in sorted(ch['checkItems'], key=lambda i: i['pos'])]
        cur = []
        nome = ch['name'].strip()
        if not re.search(r'(?i)o que fazer nos stories|stories', nome): cur.append(nome.upper())
        for it in items:
            m = re.fullmatch(r'\*\*(.+?)\*\*:?', it)
            if m:
                if cur: out.append('\n'.join(cur))
                cur = [m.group(1).strip().upper()]
            else: cur.append('- ' + it)
        if cur: out.append('\n'.join(cur))
    return '\n\n'.join(out)
# notas de semana: cartões da lista que não são dia nem cabeçalho
wk_re = re.compile(r'(\d+)\s+(?:de|se)\s+(\w+)\s+a\s+(\d+)\s+de\s+(\w+)', re.I)
day_re = re.compile(r'^(segunda|terça|terca|quarta|quinta|sexta|sábado|sabado)\b', re.I)
notas = {}  # semana -> text
by_list_week = {}
for o in cards.values():
    if o['semana']: by_list_week[raw[o['id']]['idList']] = o['semana']
for c in sorted(d['cards'], key=lambda c: c['pos']):
    if c['closed'] or c['idList'] not in by_list_week: continue
    n = c['name'].strip()
    if wk_re.search(n) or day_re.match(n) or n in ('.', ''): continue
    w = by_list_week[c['idList']]
    if w < '2026-10-12': continue
    txt = n + (('\n' + c['desc'].strip()) if c['desc'].strip() else '')
    notas.setdefault(w, []).append(txt)
writes = []; rel = []
FMT_OK = {'Reels', 'Carrossel', 'Fotos', 'Só stories', 'Estático', 'Live'}
for cid, o in cards.items():
    if not o['data'] or o['data'] < '2026-10-12': continue
    k = 'd' + o['data']
    L = json.load(open(f'{SP}/live/plano/{k}.json'))
    S = seed.get(k, {})
    upd = {}; what = []
    st = stories_txt(cid)
    secs = parse(o['cartao'])
    fresh = V.get(k, 1) == 1
    replaced = L.get('trelloId') and L['trelloId'] != cid
    if fresh or (replaced and not L.get('copy')) or not L.get('trelloId'):
        if L.get('cartao') != o['cartao']: upd.update(cartao=o['cartao'], secoes=secs); what.append('cartão')
        if (L.get('stories') or '') != st: upd['stories'] = st; what.append('stories')
        if L.get('titulo') != o['titulo']: upd['titulo'] = o['titulo']
        if not L.get('formato') and o['formato'] in FMT_OK: upd['formato'] = o['formato']
        if L.get('inspiracao') != o['inspiracao']: upd['inspiracao'] = o['inspiracao']
        upd.update(trello=o['trello'], trelloId=cid)
    else:
        if o['cartao'] != L.get('cartao'):
            if L.get('cartao') == S.get('cartao'): upd.update(cartao=o['cartao'], secoes=secs); what.append('cartão')
            else: upd['cartaoTrello'] = o['cartao']; what.append('cartão novo no Trello (o teu ficou)')
        if st and st != (L.get('stories') or ''):
            if (L.get('stories') or '') in ('', S.get('stories', '')): upd['stories'] = st; what.append('stories')
            else: upd['storiesTrello'] = st; what.append('stories novos no Trello (os teus ficaram)')
        ni = [u for u in o['inspiracao'] if u not in (L.get('inspiracao') or [])]
        if ni: upd['inspiracao'] = (L.get('inspiracao') or []) + ni; what.append('inspiração')
        if replaced: what.append('ATENÇÃO: cartão do Trello trocado, já tinhas copy')
    # comentários do Trello
    have = {re.sub(r'\W+', '', (c.get('texto') or ''))[:80] for c in (L.get('comentarios') or [])}
    novos = []
    for c in o['comentarios']:
        key = re.sub(r'\W+', '', c['texto'])[:80]
        if key in have: continue
        autor = 'Sarah' if re.search(r'sarah', c['quem'], re.I) else 'Tânia'
        novos.append({'autor': autor, 'texto': c['texto'], 'data': c['data'] + 'T12:00:00.000Z', 'alvo': 'feed', 'origem': 'trello'})
    if novos:
        upd['comentarios'] = (L.get('comentarios') or []) + novos; what.append(f'{len(novos)} comentário(s)')
    nota = '\n\n'.join(notas.get(o['semana'], []))
    if nota and nota != L.get('semanaNota'): upd['semanaNota'] = nota
    if upd:
        upd['atualizado'] = datetime.datetime.utcnow().isoformat() + 'Z'
        writes.append({'op': 'update', 'collection': 'plano', 'doc_id': k, 'data': upd, 'if_version': V.get(k, 1)})
        rel.append((o['data'], o['titulo'][:50], ', '.join(what) or 'nota da semana'))
# dias sem cartão mas com nota de semana
for fn in os.listdir(f'{SP}/live/plano'):
    k = fn[:-5]; L = json.load(open(f'{SP}/live/plano/{fn}'))
    if any(w['doc_id'] == k for w in writes): continue
    nota = '\n\n'.join(notas.get(L.get('semana'), []))
    if nota and nota != L.get('semanaNota'):
        writes.append({'op': 'update', 'collection': 'plano', 'doc_id': k, 'data': {'semanaNota': nota}, 'if_version': V.get(k, 1)})
for r in sorted(rel): print(*r, sep=' | ')
print(len(writes), 'writes')
for i in range(0, len(writes), 50):
    json.dump(writes[i:i+50], open(f'm{i//50}.json', 'w'), ensure_ascii=False)
for w, t in sorted(notas.items()): print('NOTA', w, '::', ' || '.join(x[:150].replace(chr(10), ' ') for x in t))
