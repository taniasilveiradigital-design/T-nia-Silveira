import json,sys,re,datetime,os
d=json.load(open(sys.argv[1]))
lists={l['id']:l for l in d['lists']}
cm={}
for a in d['actions']:
    if a['type']=='commentCard':
        cm.setdefault(a['data']['card']['id'],[]).append({'data':a['date'][:10],'quem':a['memberCreator']['fullName'],'texto':a['data']['text']})
cl={}
for c in d['checklists']: cl.setdefault(c['idCard'],[]).append(c)
MES={'janeiro':1,'fevereiro':2,'março':3,'abril':4,'maio':5,'junho':6,'julho':7,'agosto':8,'setembro':9,'outubro':10,'novembro':11,'dezembro':12}
DIA={'segunda':0,'terça':1,'terca':1,'quarta':2,'quinta':3,'sexta':4,'sábado':5,'sabado':5}
SKIP={'Seu plano de ação','Seus materiais','Já Postados','Estratégias','Conteúdos','segunda semana','quarta semana','quinta seman','.'}
cards=sorted([c for c in d['cards'] if not lists[c['idList']]['closed'] and lists[c['idList']]['name'] not in SKIP],key=lambda c:(lists[c['idList']]['pos'],c['pos']))
out=[];week=None;wk_re=re.compile(r'(\d+)\s+(?:de|se)\s+(\w+)\s+a\s+(\d+)\s+de\s+(\w+)',re.I)
def mkdate(day,mon): return datetime.date(2026,MES[mon.lower()],int(day))
links=lambda s,pat: list(dict.fromkeys(re.findall(pat,s)))
# semana de cada lista: 1º cabeçalho aberto; senão 1º arquivado; novembro sem cabeçalho = semanas seguidas desde 2 nov
lw={}
for c in cards:
    m=wk_re.search(c['name'])
    if m:
        try: w=mkdate(m.group(1),m.group(2)); w=w-datetime.timedelta(days=w.weekday())
        except Exception: continue
        k=c['idList']; cur=lw.get(k)
        if cur is None or (cur[1] and not c['closed']): lw[k]=(w,c['closed'])
nov=sorted([l['id'] for l in sorted(d['lists'],key=lambda l:l['pos']) if l['name']=='novembro' and not l['closed']],key=lambda k: k!='6a9f9acdbbde1d4d20b4dd97')
for i,k in enumerate(nov):
    if k not in lw: lw[k]=(datetime.date(2026,11,2)+datetime.timedelta(days=7*i),False)
for c in cards:
    n=c['name'].strip(); L=lists[c['idList']]['name']
    if c['closed'] or wk_re.search(n): continue
    week=lw.get(c['idList'],(None,))[0]
    dm=re.match(r'^(segunda|terça|terca|quarta|quinta|sexta|sábado|sabado)\s*:?\s*(.*)$',n,re.I)
    if not dm and not n.lower().startswith('conversa'): continue
    desc=c['desc'] or ''
    if dm:
        dia=DIA[dm.group(1).lower()]; titulo=dm.group(2).strip()
    else:
        dia=None; titulo=n
    if not titulo and not desc: continue
    data=(week+datetime.timedelta(days=dia)).isoformat() if (week and dia is not None) else None
    if not dm:  # "Conversa Tramada" cards in same week
        m2=re.match(r'^(segunda|terça|quarta|quinta|sexta|sábado)',n,re.I)
    low=(titulo+' '+desc[:300]).lower()
    insp=links(desc,r'https?://(?:www\.)?(?:instagram\.com|vm\.tiktok\.com|www\.tiktok\.com|tiktok\.com)[^\s)"\]]+')
    canva=links(desc+' '+' '.join(x['texto'] for x in cm.get(c['id'],[])),r'https://canva\.link/[a-z0-9]+')
    if 'conversa tramada' in low: fmt='Live'
    elif 'pausa' in low[:120]: fmt='Só stories'
    elif re.search(r'\*?\*?(slide|ponto)\s*\d',desc,re.I): fmt='Carrossel'
    elif re.search(r'\bcena\s*\d',desc,re.I): fmt='Reels'
    elif any('/reel/' in u or 'tiktok' in u for u in insp): fmt='Reels'
    elif any('/p/' in u for u in insp): fmt='Carrossel'
    elif re.search(r'pega no (teu )?ca[fg]',desc,re.I): fmt='Reels'
    else: fmt='Por definir'
    # copy final
    copy=''
    idx=[mm.start() for mm in re.finditer(r'(?i)(\*\*|_|#+ )*\*?\*?(novo\s+copp?y|copp?y\s+retificado|copp?y)\s*:?\**_*',desc)]
    pos_ret=[mm.start() for mm in re.finditer(r'(?i)(novo copp?y|copp?y retificado)',desc)]
    start = pos_ret[-1] if pos_ret else (idx[0] if idx else None)
    if start is None and fmt=='Carrossel':
        mm=re.search(r'(?i)\*?\*?slide\s*1',desc); start=mm.start() if mm else None
    if start is not None:
        seg=desc[start:]
        seg=re.sub(r'(?i)^[\s\*_#]*(novo\s+copp?y|copp?y\s+retificado|copp?y)\s*:?[\*_\s]*','',seg)
        stop=re.search(r'(?im)^\s*\**_*(template|tamplate|templete|capa reels|capa|inspira[çc][ãa]o|o que precisa|possíveis ideias|analise desse|como fazer|reels)\b.*$',seg)
        if stop: seg=seg[:stop.start()]
        copy=re.sub(r'!\[[^\]]*\]\([^)]*\)','[imagem]',seg).strip().strip('-').strip()
    if fmt=='Por definir' and copy and not re.search(r'(?i)slide',copy): fmt='Reels'
    if fmt=='Por definir' and re.search(r'(?i)guarda este v[ií]deo|v[ií]deo',desc[:2000]): fmt='Reels'
    stories=[]
    for ch in cl.get(c['id'],[]):
        for it in sorted(ch['checkItems'],key=lambda i:i['pos']):
            stories.append(it['name'])
    def field(name):
        mm=re.search(r'(?is)\*\*'+name+r'\*\*\s*\n(.*?)(?:\n---|\Z)',desc)
        return mm.group(1).strip() if mm else ''
    tema=field('Tema') or titulo
    estado='Publicado' if (data and data<='2026-10-10') else ('Planeado' if data else 'Sem data')
    if fmt=='Só stories': estado = 'Publicado' if (data and data<'2026-10-10') else estado
    out.append(dict(id=c['id'],data=data,dia=['Segunda','Terça','Quarta','Quinta','Sexta','Sábado','Domingo'][dia] if dia is not None else '',
        semana=week.isoformat() if week else None,titulo=titulo or n,tema=tema[:500],formato=fmt,estado=estado,
        objetivo=(field('Feed') or field('Objetivo'))[:3000],estrategia=field('Estratégia')[:3000],
        copy=copy[:40000],cartao=desc[:60000],stories=stories,inspiracao=insp,canva=canva,
        comentarios=cm.get(c['id'],[]),trello=c['shortUrl'],lista=L,origem='trello'))
json.dump(out,open('conteudos.json','w'),ensure_ascii=False,indent=0)
from collections import Counter
print(len(out),Counter(o['formato'] for o in out),Counter(o['estado'] for o in out))
print(sum(1 for o in out if o['copy']), 'com copy')
for o in out: print(o['data'],o['dia'][:3],o['formato'][:9].ljust(9),len(o['copy']),o['titulo'][:60])
