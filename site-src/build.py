#!/usr/bin/env python3
"""Gera o site taniasilveira.pt em ../site. Correr: python3 site-src/build.py"""
import json, os, html, datetime

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "site")
SITE = "https://taniasilveira.pt"
HOJE = "2026-11-20"

# ---------- dados que a Tânia pode mudar num só sítio ----------
ANOS = "10"  # anos de experiência no têxtil
LINKS = {
    "diagnostico": "https://sessaodiagnostico.base44.app/",
    "fibra": "https://metodofibra.base44.app/",
    "tafeta": "https://calendar.app.google/B5q9q8hBqUVsdThx7",
    "lista_revenda": "https://checkout.salespark.io/11FRP51MWJH0IFW/",
    "lista_zero": "https://checkout.salespark.io/1577ZC1MWEXNZ71/",
    "lista_combo": "https://checkout.salespark.io/11FRP51MWJH6557/?offer=mwjh6564",
    "instagram": "https://www.instagram.com/taniasilveira.pt/",
    "linkedin": "https://www.linkedin.com/in/t%C3%A2nia-silveira-229848295",
}
# Mensagens reais de clientes (WhatsApp), com nomes ocultados.
# Formato: ("frase da cliente", "quem", "contexto"). Lista vazia = secção escondida.
FEEDBACKS = [
    ("Tânia, o teu Método FIBRA ficou-me na cabeça: estrutura, margem e estratégia.", "Cliente", "Depois de conhecer o método"),
    ("Quero ter o compromisso de, de 15 em 15 dias, reunir contigo.", "Cliente", "A decisão de entrar em acompanhamento"),
    ("Já temos data para gravação na RTP.", "Cliente em acompanhamento", "Marca a caminho da televisão"),
    ("Já recebi o email da inscrição. Fomos selecionados. Aquela feira que supostamente tinha as inscrições fechadas: afinal fomos aceites.", "Cliente do Método FIBRA", "Seleção para uma feira"),
    ("Ontem também me candidatei ao mercado e recebi o email agora. Fomos aceites. Para dia 30 e 31 de maio.", "Cliente em acompanhamento", "Candidatura aceite"),
    ("Adorei todos, mas o primeiro está espetacular. Encheu o coração.", "Cliente", "Revisão do logótipo da marca"),
]

# Casos reais, do arquivo "Histórias de Clientes" da Tânia
CASOS = [
    ("Rebranding", "ROMEO: rebranding em cinco dias",
     "A fundadora entrou para mudar a imagem. Em cinco dias o posicionamento ficou ajustado, a identidade clara e uma peça foi pensada de raiz.",
     "Não foi velocidade. Foi clareza."),
    ("Marca do zero", "LEFKOT: da ideia à primeira coleção",
     "A LEFKOT queria criar uma marca e não sabia por onde começar. Acompanhei o pensamento inicial, a estrutura e as decisões até à primeira coleção. Hoje caminha sozinha.",
     "Não dei ideias soltas. Dei método."),
    ("Revenda", "Do medo à revenda",
     "Chegou insegura, sem saber se o negócio tinha pernas. Com estrutura e direção, organizou o processo e hoje revende com confiança.",
     "O crescimento foi interno antes de ser externo."),
    ("Viabilidade", "O pedido certo atrás do pedido errado",
     "Muitos seguidores e investimento forte em comunicação. Parecia um problema de vendas. A pergunta real era se as peças podiam ser produzidas em Portugal.",
     "Alcance nunca substitui estrutura."),
]

CLIENTES = ["Nicau Couture", "ROMEO", "DOMPURE", "Hosmos.co", "LEFKOT", "Traços D'Amor"]
OG = SITE + "/assets/img/og.jpg"
FOTO = SITE + "/assets/img/tania-silveira-fita-metrica.jpg"

e = html.escape

def casos_html():
    return '<div class="cases">' + "".join(
        f'<article class="case rise"><span class="tag">{e(t)}</span><h3>{e(h)}</h3><p>{e(d)}</p><p class="lesson">{e(l)}</p></article>'
        for t, h, d, l in CASOS) + '</div>'

def feedbacks_html():
    if not FEEDBACKS:
        return ""
    cards = "".join(f'<figure class="fb rise"><blockquote>“{e(q)}”</blockquote><figcaption><b>{e(n)}</b>{e(m)}</figcaption></figure>' for q, n, m in FEEDBACKS)
    return f'''<section class="alt"><div class="wrap"><div class="head"><span class="eyebrow">Mensagens reais de clientes</span><h2>O que chega <em>ao meu WhatsApp.</em></h2><p class="lead">Feiras, mercados, televisão. Resultados contados pelas próprias clientes. Os nomes ficam de fora, por respeito.</p></div><div class="fbs">{cards}</div></div></section>'''

def pic(name, alt, h=1650, lazy=True, sizes="(max-width:860px) 90vw, 40vw"):
    return (f'<picture><source type="image/webp" srcset="/assets/img/{name}-600.webp 600w, /assets/img/{name}-1100.webp 1100w" sizes="{sizes}">'
            f'<img src="/assets/img/{name}.jpg" width="1100" height="{h}" alt="{alt}"' + (' loading="lazy"' if lazy else ' fetchpriority="high"') + '></picture>')
PAGES = []  # (path, prioridade)

PERSON = {
    "@type": "Person", "@id": SITE + "/#tania",
    "name": "Tânia Silveira",
    "jobTitle": "Estrategista de marcas de moda e negócios têxteis",
    "description": f"Estrategista de produto e estrutura para marcas de moda, com {ANOS} anos de experiência na indústria têxtil: chão de fábrica, produção, planeamento, produto e gestão comercial.",
    "image": FOTO, "url": SITE + "/sobre/",
    "homeLocation": {"@type": "Place", "name": "Guimarães, Portugal"},
    "birthPlace": {"@type": "Place", "name": "Chaves, Portugal"},
    "knowsAbout": ["estratégia de marcas de moda", "indústria têxtil", "desenvolvimento de produto de moda",
                   "margem e preço de coleção", "estrutura de coleção", "fornecedores têxteis em Portugal",
                   "produção de vestuário", "posicionamento de marca de moda"],
    "knowsLanguage": ["pt-PT"],
    "sameAs": [LINKS["instagram"], LINKS["linkedin"]],
    "worksFor": {"@id": SITE + "/#negocio"},
}
BUSINESS = {
    "@type": "ProfessionalService", "@id": SITE + "/#negocio",
    "name": "Tânia Silveira — Estratégia para marcas de moda",
    "url": SITE + "/", "image": FOTO, "logo": SITE + "/assets/img/icon-512.png",
    "description": "Estratégia, estrutura de produto e margem para marcas de moda e negócios têxteis em Portugal. Diagnóstico Alinhavar, Método FIBRA e Consultoria Tafetá 360.",
    "founder": {"@id": SITE + "/#tania"},
    "address": {"@type": "PostalAddress", "addressLocality": "Guimarães", "addressRegion": "Braga", "addressCountry": "PT"},
    "areaServed": [{"@type": "Country", "name": "Portugal"}, {"@type": "Place", "name": "Online"}],
    "availableLanguage": "pt-PT",
    "sameAs": [LINKS["instagram"], LINKS["linkedin"]],
}

# ---------- moldura ----------
class _Thread:
    n = 0
    def __format__(self, spec):
        _Thread.n += 1
        i = f"sw{_Thread.n}"
        d = "M0 12 C 150 2, 300 22, 450 12 S 750 2, 900 12 S 1100 22, 1200 12"
        return (f'<svg class="thread sew" viewBox="0 0 1200 24" preserveAspectRatio="none" aria-hidden="true">'
                f'<defs><mask id="{i}" maskUnits="userSpaceOnUse" x="0" y="0" width="1200" height="24"><path class="reveal" d="{d}" pathLength="1" fill="none" stroke="#fff" stroke-width="6"/></mask></defs>'
                f'<path d="{d}" fill="none" stroke="currentColor" stroke-width="1.5" stroke-dasharray="7 6" mask="url(#{i})"/></svg>')
THREAD = _Thread()

NAV = [("/metodo-fibra/", "Método FIBRA"), ("/servicos/", "Serviços"), ("/empresas/", "Empresas"), ("/ferramentas/", "Ferramentas"), ("/guias/", "Guias"), ("/sobre/", "Sobre")]

def head(path, title, desc, schema, kind="website", noindex=False):
    url = SITE + path
    graph = {"@context": "https://schema.org", "@graph": schema}
    return f"""<!doctype html>
<html lang="pt-PT">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{url}">
{'<meta name="robots" content="noindex">' if noindex else '<meta name="robots" content="index, follow, max-image-preview:large">'}
<meta name="author" content="Tânia Silveira">
<meta property="og:type" content="{kind}">
<meta property="og:locale" content="pt_PT">
<meta property="og:site_name" content="Tânia Silveira">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{OG}">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#faf6f1">
<link rel="icon" href="/assets/img/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/assets/img/icon-180.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;1,400;1,500&family=Raleway:wght@400;500;600&family=Dr+Sugiyama&display=swap">
<link rel="stylesheet" href="/assets/site.css">
<script type="application/ld+json">{json.dumps(graph, ensure_ascii=False)}</script>
</head>
<body>
<a class="skip" href="#conteudo">Saltar para o conteúdo</a>
<header class="mast"><div class="wrap">
<a class="brand" href="/" aria-label="Tânia Silveira, página inicial">Tânia Silveira<small>Estratégia para marcas de moda</small></a>
<button class="burger" id="burger" aria-label="Abrir menu" aria-expanded="false" aria-controls="nav"><span></span><span></span><span></span></button>
<nav class="nav" id="nav" aria-label="Principal">
{''.join(f'<a href="{h}"{" aria-current=page" if path.startswith(h) else ""}>{t}</a>' for h, t in NAV)}
<a class="btn" href="/diagnostico-alinhavar/">Pedir diagnóstico</a>
</nav></div><div id="sew-progress" aria-hidden="true"></div></header>
<main id="conteudo">
"""

FOOT = f"""</main>
<footer class="foot"><div class="wrap">
<div class="grid">
<div><a class="brand" href="/">Tânia Silveira<small>Estratégia para marcas de moda</small></a>
<p style="margin-top:22px;max-width:320px">Estrutura, margem e estratégia para marcas de moda crescerem com previsibilidade. Guimarães, Portugal. Trabalho com marcas de todo o país, presencial e online.</p></div>
<div><h4>Serviços</h4><ul>
<li><a href="/diagnostico-alinhavar/">Diagnóstico Alinhavar</a></li>
<li><a href="/metodo-fibra/">Método FIBRA</a></li>
<li><a href="/consultoria-tafeta-360/">Consultoria Tafetá 360</a></li>
<li><a href="/lista-estrategica-de-fornecedores/">Lista de Fornecedores</a></li>
<li><a href="/empresas/">Para empresas</a></li></ul></div>
<div><h4>Conhecer</h4><ul>
<li><a href="/sobre/">Sobre a Tânia</a></li>
<li><a href="/ferramentas/">Ferramentas</a></li>
<li><a href="/guias/">Guias</a></li>
<li><a href="/perguntas-frequentes/">Perguntas frequentes</a></li>
<li><a href="/contacto/">Contacto</a></li></ul></div>
<div><h4>Seguir</h4><ul>
<li><a href="{LINKS['instagram']}" rel="me noopener" target="_blank">Instagram</a></li>
<li><a href="{LINKS['linkedin']}" rel="me noopener" target="_blank">LinkedIn</a></li></ul></div>
</div>
<div class="base"><span>© 2026 Tânia Silveira · Estratégia Têxtil</span><span><a href="/politica-de-privacidade/">Política de privacidade</a></span></div>
</div></footer>
<script src="/assets/site.js" defer></script>
<script src="/assets/ferramentas.js" defer></script>
</body></html>
"""

def crumbs(items):
    """items: [(nome, path)] — devolve html + schema."""
    allitems = [("Início", "/")] + items
    h = '<nav class="crumbs" aria-label="Caminho">' + " / ".join(
        f'<a href="{p}">{e(n)}</a>' if i < len(allitems) - 1 else f"<span>{e(n)}</span>"
        for i, (n, p) in enumerate(allitems)) + "</nav>"
    s = {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + p} for i, (n, p) in enumerate(allitems)]}
    return h, s

def faq_block(qs):
    h = '<div class="faq">' + "".join(
        f"<details><summary>{e(q)}</summary><div><p>{a}</p></div></details>" for q, a in qs) + "</div>"
    import re
    s = {"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"<[^>]+>", "", a)}} for q, a in qs]}
    return h, s

def service_schema(path, name, desc, extra=None):
    s = {"@type": "Service", "@id": SITE + path + "#servico", "name": name, "description": desc,
         "provider": {"@id": SITE + "/#tania"}, "areaServed": "PT", "url": SITE + path,
         "serviceType": "Consultoria estratégica para marcas de moda"}
    if extra: s.update(extra)
    return s

def write(path, content, prio="0.8"):
    d = os.path.join(ROOT, path.strip("/"))
    os.makedirs(d, exist_ok=True)
    fn = os.path.join(d, "index.html") if path.endswith("/") else os.path.join(ROOT, path.strip("/"))
    content = content.replace('class="steps"', 'class="steps sew"')
    with open(fn, "w", encoding="utf-8") as f:
        f.write(content)
    if prio: PAGES.append((path, prio))

def final_cta(titulo="Antes de mudar tudo, <em>percebe o que está errado.</em>",
              texto="O Diagnóstico Alinhavar identifica onde está o problema real da tua marca e o que tens de fazer primeiro."):
    return f"""<section class="dark final"><div class="wrap">
<span class="eyebrow">Próximo passo</span>
<h2>{titulo}</h2>
<p class="lead">{texto}</p>
<div class="btns"><a class="btn light" href="/diagnostico-alinhavar/">Pedir o Diagnóstico Alinhavar</a></div>
</div></section>"""

# =====================================================================
# HOME
# =====================================================================
home_faq = [
    ("O que faz uma estrategista de marcas de moda?",
     "Organiza as decisões que estão por trás da marca: que produto fazer, a que preço, com que margem, para quem e com que fornecedores. Não faço conteúdo nem design. Faço a estrutura que permite à marca crescer sem depender de improviso."),
    ("Por onde começo se não sei o que está a travar a minha marca?",
     "Pelo <a href=\"/diagnostico-alinhavar/\">Diagnóstico Alinhavar</a>. É uma sessão de 30 minutos para identificar o gargalo real: produto, margem, posicionamento ou decisão. A partir daí, sabes se precisas de acompanhamento ou só de afinar."),
    ("Qual a diferença entre o Método FIBRA e a Consultoria Tafetá 360?",
     "O <a href=\"/metodo-fibra/\">Método FIBRA</a> é acompanhamento 1:1 durante 6 meses, para estruturar o negócio por inteiro. A <a href=\"/consultoria-tafeta-360/\">Tafetá 360</a> é uma intervenção pontual: 2 horas de diagnóstico profundo e 1 hora de seguimento ao fim de um mês, para marcas que já funcionam e precisam de afinar."),
    ("Trabalhas só com marcas do Norte de Portugal?",
     "Não. Estou em Guimarães, no centro da indústria têxtil portuguesa, mas trabalho com marcas de todo o país. As sessões são online ou presenciais."),
]
faq_h, faq_s = home_faq_block = faq_block(home_faq)

home = head("/", "Tânia Silveira · Estratégia para marcas de moda e negócios têxteis",
            f"Estrategista de marcas de moda em Portugal. {ANOS} anos de chão de fábrica a pôr estrutura, margem e direção em marcas de moda. Método FIBRA, Consultoria Tafetá 360 e Diagnóstico Alinhavar.",
            [BUSINESS, PERSON, {"@type": "WebSite", "@id": SITE + "/#site", "url": SITE + "/", "name": "Tânia Silveira",
                                "inLanguage": "pt-PT", "publisher": {"@id": SITE + "/#tania"}}, faq_s])
home += f"""
<section class="hero"><div class="wrap">
<div>
<span class="eyebrow">Estratégia para marcas de moda &amp; negócios têxteis</span>
<h1>Não és ignorada por falta de qualidade. <em>És ignorada por falta de posicionamento.</em></h1>
<p class="lead">Sou a Tânia Silveira. Há {ANOS} anos no têxtil, do chão de fábrica ao produto. Ponho estrutura, margem e direção em marcas de moda que trabalham muito e crescem pouco.</p>
<div class="btns"><a class="btn" href="/diagnostico-alinhavar/">Pedir o diagnóstico</a><a class="btn ghost" href="/autodiagnostico/">Fazer o autodiagnóstico</a></div>
<div class="proof"><span>{ANOS} anos na indústria têxtil</span><span>Produção, produto e planeamento</span><span>Guimarães · Portugal</span></div>
</div>
<figure class="portrait">
{pic("tania-silveira-fita-metrica", "Tânia Silveira, estrategista têxtil, com uma fita métrica ao pescoço em frente a um cabide de roupa", lazy=False)}
<figcaption><b>Tânia Silveira</b>Estrategista têxtil</figcaption>
</figure>
</div></section>
{THREAD}
<section><div class="wrap">
<div class="head"><span class="eyebrow">Em que fase está a tua marca?</span>
<h2>O problema muda de forma. <em>A raiz é a mesma.</em></h2>
<p class="lead">Falta de estrutura, clareza e direção. Escolhe onde estás e eu digo-te por onde começar. Ou <a class="link" href="/autodiagnostico/">faz o autodiagnóstico em 2 minutos</a>.</p></div>
<div class="paths">
<a class="path rise" href="/lista-estrategica-de-fornecedores/"><span class="n">01</span><h3>Tenho a ideia, falta o caminho.</h3><p>Queres criar a marca ou começar a vender e não sabes por onde pegar: fornecedores, quantidades, preço. Começa com base, não com pressa.</p><span class="go">Começar certo →</span></a>
<a class="path rise" href="/diagnostico-alinhavar/"><span class="n">02</span><h3>Já vendo, mas fica pouco.</h3><p>Trabalhas o dia inteiro, dependes de descontos e no fim do mês a conta não fecha. O problema está na margem ou no produto. Vamos encontrá-lo.</p><span class="go">Encontrar o gargalo →</span></a>
<a class="path rise" href="/metodo-fibra/"><span class="n">03</span><h3>Cresci e virei o gargalo.</h3><p>A marca vende, mas depende de ti para tudo. Cresceu e ficou pesada. Precisas de estrutura para escalar sem perder o controlo.</p><span class="go">Estruturar para escalar →</span></a>
</div></div></section>

<section class="alt"><div class="wrap split">
<div><span class="eyebrow">Faz a conta agora</span>
<h2>Quanto ganhas, <em>de verdade</em>, em cada peça?</h2>
<p class="lead">Mete o custo e o preço de uma peça tua. A conta faz-se à tua frente, sem IVA, que o IVA não é teu.</p>
<p><a class="link" href="/calculadora-de-margem/">Fazer a conta completa, com portes, taxas e devoluções →</a></p></div>
<form class="mini" id="mini-calc" onsubmit="return false" aria-label="Calculadora rápida de margem">
<div class="mini-in">
<label for="m-custo">Custo da peça<input id="m-custo" type="number" inputmode="decimal" min="0" step="0.5" value="22"><span>€</span></label>
<label for="m-pvp">Preço de venda com IVA<input id="m-pvp" type="number" inputmode="decimal" min="0" step="1" value="69"><span>€</span></label>
<label for="m-desc" class="range">Desconto médio <output id="m-desc-v">10%</output><input id="m-desc" type="range" min="0" max="60" step="5" value="10"></label>
</div>
<div class="mini-out" aria-live="polite">
<div class="dial"><svg viewBox="0 0 120 120" aria-hidden="true"><circle cx="60" cy="60" r="52" class="track"/><circle cx="60" cy="60" r="52" class="val" pathLength="1"/></svg><b id="m-pct">0%</b></div>
<p class="m-sub">margem bruta</p>
<p id="m-eur" class="m-eur"></p>
<div id="m-verdict" class="verdict"></div>
</div>
</form>
</div></section>

<section class="dark"><div class="wrap">
<div class="head"><span class="eyebrow">Como penso</span>
<h2>Eu não dou dicas. <em>Desenho a estrutura.</em></h2>
<p class="lead">Enquanto estás presa no operacional, as decisões estratégicas ficam sempre para depois. É aí que as marcas param.</p></div>
<div class="pillars">
<div><b>Estrutura antes do crescimento</b><p>Crescer em cima de improviso é só multiplicar o problema.</p></div>
<div><b>Produto antes da comunicação</b><p>Nenhum post salva uma coleção mal pensada.</p></div>
<div><b>Clareza antes da execução</b><p>Primeiro sabes o que decidir. Depois fazes.</p></div>
<div><b>Decisão antes da ação</b><p>Cada peça, cada preço, cada fornecedor com critério.</p></div>
</div></div></section>

<section><div class="wrap">
<div class="head"><span class="eyebrow">Serviços</span>
<h2>Um ponto de entrada <em>para cada fase.</em></h2>
<p class="lead">Escolhe por onde entras. Eu faço o resto: estrutura, critério e decisão.</p></div>
<div class="services">
<div class="svc"><span class="tag">Análise · 30 min</span><h3>Diagnóstico Alinhavar</h3>
<p>Identifica o bloqueio que trava a marca: produto, margem, posicionamento ou decisão.</p>
<ul><li>Leitura do estado atual da marca</li><li>O gargalo real, nomeado</li><li>O que decidir primeiro</li></ul>
<a class="btn ghost" href="/diagnostico-alinhavar/">Saber mais</a></div>
<div class="svc main"><span class="badge">Programa principal</span><span class="tag">Acompanhamento · 6 meses</span><h3>Método FIBRA</h3>
<p>Estrutura estratégica 1:1 para marcas que querem crescer com direção e consistência.</p>
<ul><li>Coleção e lógica de produto</li><li>Preço e margem</li><li>Posicionamento e comunicação</li><li>Mentalidade de decisão</li></ul>
<a class="btn light" href="/metodo-fibra/">Conhecer o FIBRA</a></div>
<div class="svc"><span class="tag">Consultoria · 2h + 1h</span><h3>Consultoria Tafetá 360</h3>
<p>Intervenção para marcas com base criada que precisam de afinar produto, margem e estratégia comercial.</p>
<ul><li>Sessão estratégica de 2 horas</li><li>Plano de correção</li><li>Seguimento de 1 hora ao fim de um mês</li></ul>
<a class="btn ghost" href="/consultoria-tafeta-360/">Saber mais</a></div>
</div>
<p style="margin-top:28px;color:var(--muted)">Precisas só da informação certa? A <a class="link" href="/lista-estrategica-de-fornecedores/">Lista Estratégica de Fornecedores</a> reúne contactos do setor têxtil para revenda e produção própria.</p>
</div></section>

<section style="padding-top:0"><div class="wrap split" style="border-top:1.5px dashed var(--beige);padding-top:clamp(48px,6vw,80px)">
<div><span class="eyebrow">Para empresas</span><h2>Fábricas, confeções e marcas com equipa. <em>Começa por uma consultoria.</em></h2></div>
<div><p class="lead">Olho para a empresa por dentro, com a experiência de quem trabalhou do lado da produção. A partir daí, apresento um plano à medida.</p>
<a class="btn" href="/empresas/">Ver o trabalho com empresas</a></div>
</div></section>

<section class="alt"><div class="wrap split">
<figure class="portrait" style="max-width:440px">
{pic("tania-silveira-amostras-tecido", "Tânia Silveira a analisar amostras de tecido e esboços de coleção", sizes="(max-width:860px) 90vw, 36vw")}
</figure>
<div><span class="eyebrow">Quem está do outro lado</span>
<h2>Do chão de fábrica <em>à tua marca.</em></h2>
<p>Comecei na indústria têxtil, entre produção, planeamento, produto e fornecedores. Vi de perto como uma peça nasce, quanto custa de facto e onde as marcas perdem dinheiro sem dar por isso.</p>
<p>Hoje uso essa experiência para pôr critério onde existe improviso. Não sou consultora de teoria. Sei o que acontece numa confeção quando a ficha técnica vem mal feita.</p>
<p class="sig">Tânia Silveira</p>
<a class="link" href="/sobre/">Conhecer a minha história →</a></div>
</div></section>

<section><div class="wrap">
<div class="head"><span class="eyebrow">Casos reais</span><h2>Bastidores, <em>não promessas.</em></h2>
<p class="lead">Histórias de marcas que acompanhei. O produto raramente é o problema. As decisões são.</p></div>
{casos_html()}
<div style="text-align:center;margin-top:clamp(48px,6vw,80px)"><span class="eyebrow">Marcas com quem já trabalhei</span>
<div class="clients" style="margin-top:20px">{''.join(f'<span>{e(c)}</span>' for c in CLIENTES)}</div></div>
</div></section>
{feedbacks_html()}
{THREAD}
<section><div class="wrap">
<div class="head"><span class="eyebrow">Guias</span><h2>Respostas de quem <em>já esteve na fábrica.</em></h2></div>
<div class="cards" id="home-guias">__GUIAS__</div>
</div></section>

<section class="alt"><div class="wrap narrow">
<div class="head"><span class="eyebrow">Perguntas frequentes</span><h2>Antes de <em>avançares.</em></h2></div>
{faq_h}
<p style="margin-top:26px"><a class="link" href="/perguntas-frequentes/">Ver todas as perguntas →</a></p>
</div></section>
{final_cta()}
""" + FOOT

# =====================================================================
# GUIAS (conteúdo para Google e para IA)
# =====================================================================
GUIAS = []

def guia(slug, titulo, h1, desc, tag, resumo, corpo, faqs, tempo):
    path = f"/guias/{slug}/"
    GUIAS.append((path, titulo, desc, tag))
    c_h, c_s = crumbs([("Guias", "/guias/"), (titulo, path)])
    f_h, f_s = faq_block(faqs)
    art = {"@type": "Article", "@id": SITE + path + "#artigo", "headline": titulo, "description": desc,
           "author": {"@id": SITE + "/#tania"}, "publisher": {"@id": SITE + "/#tania"},
           "datePublished": HOJE, "dateModified": HOJE, "inLanguage": "pt-PT",
           "image": OG, "mainEntityOfPage": SITE + path}
    p = head(path, f"{titulo} · Tânia Silveira", desc, [art, c_s, f_s, PERSON], kind="article")
    p += f"""<article>
<header class="page-head"><div class="wrap prose">
{c_h}
<span class="eyebrow">{e(tag)}</span>
<h1 style="font-size:clamp(40px,5.4vw,68px)">{h1}</h1>
<div class="byline"><img src="/assets/img/tania-silveira-avatar.webp" alt="" width="46" height="46"><span>Por <a href="/sobre/">Tânia Silveira</a>, estrategista têxtil · {tempo} min de leitura · Atualizado a 20 nov 2026</span></div>
</div></header>
<div class="wrap prose" style="padding-bottom:80px">
<div class="tldr"><strong>Resposta curta</strong>{resumo}</div>
{corpo}
<h2>Perguntas frequentes</h2>
{f_h}
<div class="aside-cta"><h3>Queres que olhe para os números da tua marca?</h3>
<p>No Diagnóstico Alinhavar identifico onde a tua marca está a perder margem e o que tens de decidir primeiro.</p>
<a class="btn light" href="/diagnostico-alinhavar/">Pedir o diagnóstico</a></div>
</div>
</article>
""" + FOOT
    write(path, p, "0.7")

guia("como-calcular-preco-e-margem-de-uma-peca-de-roupa",
     "Como calcular o preço e a margem de uma peça de roupa",
     "Como calcular o preço e a <em>margem</em> de uma peça de roupa",
     "Passo a passo para calcular o custo real, o preço de venda e a margem de uma peça de roupa, com IVA e revenda. Escrito por quem trabalhou em produção têxtil.",
     "Preço e margem",
     "<p>Soma o custo real da peça (tecido, confeção, aviamentos, etiquetas, embalagem, transporte e quebras). Define a margem de que o negócio precisa para pagar tudo o resto. Só depois calculas o preço, e só no fim acrescentas o IVA. Se o preço que sai não é aceite pela tua cliente, o problema está no produto ou no posicionamento, não na conta.</p>",
     """
<p>A maior parte das marcas que me chegam calcula o preço ao contrário. Olha para a concorrência, escolhe um número que parece bem e espera que sobre alguma coisa. Não sobra. Sobra trabalho.</p>
<h2>1. Calcula o custo real, não o custo da fatura</h2>
<p>O custo de uma peça não é o preço que a confeção te cobra. É tudo o que tens de pagar para a peça existir e chegar à cliente:</p>
<ul>
<li><b>Matéria-prima:</b> tecido ou malha consumida por peça, incluindo o desperdício do corte.</li>
<li><b>Confeção:</b> corte, costura, acabamento, passar a ferro.</li>
<li><b>Aviamentos:</b> botões, fechos, linhas, entretelas, elásticos.</li>
<li><b>Identificação:</b> etiqueta de marca, etiqueta de composição, tag de preço.</li>
<li><b>Estampados ou bordados</b>, quando existem.</li>
<li><b>Embalagem e transporte</b> até ti e até à cliente.</li>
<li><b>Amostras e protótipos</b>, divididos pelas peças da produção.</li>
<li><b>Quebras:</b> peças com defeito, sobras, saldos.</li>
</ul>
<div class="formula">Custo real por peça = matéria-prima + confeção + aviamentos + identificação + embalagem + transporte + (amostras ÷ n.º de peças) + margem de quebra</div>
<h2>2. Decide a margem antes de decidir o preço</h2>
<p>A margem não é o que sobra. É o que o negócio precisa para pagar o que não aparece na peça: fotografias, site, publicidade, comissões de pagamento, o teu salário e o investimento na próxima coleção.</p>
<div class="formula">Margem bruta (%) = (preço de venda sem IVA − custo real) ÷ preço de venda sem IVA × 100</div>
<p>É comum o setor trabalhar com multiplicadores sobre o custo. Mas o multiplicador certo para a tua marca depende da tua estrutura de custos fixos, do canal onde vendes e de quanto queres investir em crescimento. Copiar o multiplicador de outra marca é copiar a estrutura de custos dela, que não é a tua.</p>
<h2>3. Calcula o preço de venda</h2>
<div class="formula">Preço sem IVA = custo real ÷ (1 − margem pretendida)<br>Preço ao público = preço sem IVA × 1,23  (IVA de 23% em Portugal continental)</div>
<h3>Exemplo com números redondos</h3>
<table><tr><th>Passo</th><th>Valor</th></tr>
<tr><td>Custo real da peça</td><td>20,00 €</td></tr>
<tr><td>Margem bruta pretendida</td><td>65%</td></tr>
<tr><td>Preço sem IVA: 20 ÷ (1 − 0,65)</td><td>57,14 €</td></tr>
<tr><td>Preço ao público com IVA (× 1,23)</td><td>70,29 €</td></tr></table>
<p>Os valores são um exemplo para mostrar a conta. A margem certa para a tua marca sai da tua estrutura.</p>
<p><a class="btn" href="/calculadora-de-margem/">Fazer a conta com os teus números</a></p>
<h2>4. Se vendes também a lojas, faz a conta duas vezes</h2>
<p>Uma loja multimarca compra-te a preço de revenda e aplica a margem dela. Se o teu preço ao público só funciona na tua loja online, não tens espaço para revenda. Define primeiro o preço ao público, depois o preço de revenda, e confirma que ainda tens margem nos dois.</p>
<h2>5. Os erros que mais vejo</h2>
<ul>
<li>Esquecer as amostras e os protótipos no custo.</li>
<li>Calcular a margem sobre o preço com IVA. O IVA não é teu.</li>
<li>Baixar o preço para vender e compensar com volume que não existe.</li>
<li>Dar descontos todos os meses. A cliente aprende a esperar por eles.</li>
<li>Ter peças na coleção que nunca deram margem e ninguém tirou.</li>
</ul>
<p>Se a conta não fecha, não baixes o preço. Revê o produto: o tecido, o número de operações de costura, a quantidade da encomenda. É aí que se ganha margem.</p>
""",
     [("Que margem deve ter uma marca de roupa?",
       "Não existe um número único. A margem certa é a que paga a estrutura da tua marca (marketing, site, comissões, salário, próxima coleção) e ainda deixa lucro. Calcula primeiro os teus custos fixos e só depois define a margem."),
      ("O preço de uma peça de roupa calcula-se com ou sem IVA?",
       "Calcula-se sem IVA. A margem é sempre calculada sobre o preço sem IVA, porque o IVA é entregue ao Estado. Em Portugal continental, o IVA normal é de 23%, que acrescentas no fim."),
      ("Como baixar o custo de produção sem perder qualidade?",
       "Revê o produto antes de mudar de fornecedor: o consumo de tecido no corte, o número de operações de costura, os aviamentos e a quantidade encomendada. Pequenas mudanças técnicas costumam ter mais impacto do que trocar de confeção.")],
     7)

guia("como-escolher-fornecedor-textil-em-portugal",
     "Como escolher um fornecedor têxtil em Portugal",
     "Como escolher um <em>fornecedor têxtil</em> em Portugal",
     "Critérios para escolher confeções, fornecedores de tecido e malha em Portugal: quantidades mínimas, amostras, prazos, ficha técnica e certificações.",
     "Fornecedores e produção",
     "<p>Antes de contactar fornecedores, define o produto, as quantidades e o preço-alvo. Depois avalia cada um pela quantidade mínima, pelo prazo, pela qualidade das amostras, pela comunicação e pelas condições de pagamento. O fornecedor certo é o que encaixa na fase da tua marca, não o maior nem o mais barato.</p>",
     """
<p>Portugal tem uma das indústrias têxteis mais completas da Europa, concentrada sobretudo no Norte: Guimarães, Famalicão, Barcelos, Braga, Porto. Ter fornecedores perto não é o problema. O problema é chegar a eles sem saber o que pedir.</p>
<h2>1. Prepara-te antes do primeiro contacto</h2>
<p>Um fornecedor responde melhor a quem sabe o que quer. Leva:</p>
<ul>
<li><b>O produto definido:</b> tipo de peça, tecido ou malha pretendida, composição.</li>
<li><b>Uma ficha técnica</b>, mesmo simples: medidas, desenho, pormenores de costura.</li>
<li><b>Quantidades por modelo e por tamanho.</b></li>
<li><b>Preço-alvo</b> por peça, calculado a partir da margem que precisas.</li>
<li><b>O prazo</b> em que precisas das peças.</li>
</ul>
<h2>2. Os critérios que importam</h2>
<table><tr><th>Critério</th><th>O que perguntar</th></tr>
<tr><td>Quantidade mínima</td><td>Qual o mínimo por modelo e por cor?</td></tr>
<tr><td>Amostras</td><td>Fazem protótipo? Quanto custa? Quanto tempo demora?</td></tr>
<tr><td>Prazo de produção</td><td>Quanto tempo desde a aprovação da amostra até à entrega?</td></tr>
<tr><td>Especialidade</td><td>Trabalham malha ou tecido? Que tipo de peça fazem melhor?</td></tr>
<tr><td>Comunicação</td><td>Quem é a pessoa de contacto? Responde com clareza?</td></tr>
<tr><td>Pagamento</td><td>Pedem sinal? Qual o prazo do restante?</td></tr>
<tr><td>Certificações</td><td>Têm certificação como OEKO-TEX ou GOTS, se for importante para a tua marca?</td></tr></table>
<h2>3. Revenda ou produção própria</h2>
<p>São dois negócios diferentes. Na revenda compras peças prontas e o teu trabalho é escolher, comunicar e vender. Na produção própria crias o produto e precisas de vários fornecedores: tecido, confeção, estampado, etiquetas. Escolhe primeiro o modelo, depois o fornecedor. <a class="link" href="/guias/revenda-ou-marca-propria/">Lê o guia sobre revenda e marca própria.</a></p>
<h2>4. Sinais de alerta</h2>
<ul>
<li>Aceita tudo sem fazer perguntas sobre o produto.</li>
<li>Não faz amostra antes da produção.</li>
<li>Os prazos mudam a cada conversa.</li>
<li>Não há nada por escrito: preço, quantidades, prazo.</li>
</ul>
<h2>5. Começa pequeno e testa</h2>
<p>Faz primeiro uma amostra e uma produção curta. Avalia a qualidade, o cumprimento do prazo e a forma como os problemas são resolvidos. É assim que se constrói uma relação de produção que dura.</p>
<div class="aside-cta" style="background:var(--paper2);color:var(--ink)"><h3 style="color:var(--brown)">Precisas de contactos para começar?</h3>
<p>A <a class="link" href="/lista-estrategica-de-fornecedores/">Lista Estratégica de Fornecedores</a> reúne contactos do setor têxtil para revenda e para criar produto próprio, organizados por categoria.</p></div>
""",
     [("Qual a quantidade mínima para produzir roupa em Portugal?",
       "Depende do fornecedor e do tipo de peça. Cada confeção e cada fornecedor de tecido tem os seus mínimos por modelo e por cor. Pergunta sempre o mínimo por modelo, por cor e por tamanho antes de avançar."),
      ("Onde ficam as fábricas têxteis em Portugal?",
       "A maior parte da indústria têxtil e de vestuário está no Norte do país, em concelhos como Guimarães, Vila Nova de Famalicão, Barcelos, Braga, Santo Tirso e Porto."),
      ("O que é uma ficha técnica de roupa?",
       "É o documento que descreve a peça para a produção: desenho técnico, medidas por tamanho, materiais, aviamentos, tipo de costura e acabamentos. Sem ficha técnica, cada fornecedor interpreta a peça à sua maneira.")],
     6)

guia("revenda-ou-marca-propria",
     "Revenda ou marca própria: por onde começar uma marca de roupa",
     "Revenda ou <em>marca própria</em>: por onde começar?",
     "Diferenças entre revenda de roupa e produção própria: investimento, risco, margem e controlo. Como decidir qual o modelo certo para começar a tua marca de moda.",
     "Começar uma marca",
     "<p>A revenda pede menos investimento inicial e menos conhecimento técnico, mas dá menos controlo sobre o produto e menos diferenciação. A marca própria exige mais investimento, mais tempo e conhecimento de produção, mas dá-te um produto que é só teu. Escolhe pelo que tens hoje: capital, tempo, conhecimento e a cliente que queres servir.</p>",
     """
<h2>As diferenças, lado a lado</h2>
<table><tr><th></th><th>Revenda</th><th>Marca própria</th></tr>
<tr><td>Investimento inicial</td><td>Menor</td><td>Maior (amostras, mínimos, desenvolvimento)</td></tr>
<tr><td>Tempo até vender</td><td>Curto</td><td>Mais longo</td></tr>
<tr><td>Controlo do produto</td><td>Baixo</td><td>Total</td></tr>
<tr><td>Diferenciação</td><td>Difícil: outras lojas vendem o mesmo</td><td>Alta</td></tr>
<tr><td>Conhecimento técnico</td><td>Pouco</td><td>Produto, fornecedores, produção</td></tr>
<tr><td>Principal risco</td><td>Competir só por preço</td><td>Stock parado e erros de produção</td></tr></table>
<h2>Quando faz sentido começar pela revenda</h2>
<ul><li>Queres testar o mercado com pouco capital.</li><li>A tua força é escolher, comunicar e vender.</li><li>Ainda não sabes que produto a tua cliente quer.</li></ul>
<h2>Quando faz sentido criar produto próprio</h2>
<ul><li>Tens uma ideia de produto que não existe no mercado.</li><li>Tens capital para amostras e para os mínimos de produção.</li><li>Queres construir uma marca que se distingue pelo produto.</li></ul>
<h2>O erro mais comum</h2>
<p>Querer as duas coisas ao mesmo tempo sem estrutura para nenhuma. Muitas marcas começam na revenda, percebem o que vende e só depois criam produto próprio. É um caminho válido, desde que a passagem seja uma decisão e não um impulso.</p>
<p>Qualquer que seja o modelo, a pergunta é a mesma: quem é a tua cliente e porque é que compra a ti e não a outra marca?</p>
""",
     [("É melhor começar uma loja de roupa com revenda ou com marca própria?",
       "Depende do capital, do tempo e do conhecimento técnico que tens. A revenda é mais rápida e pede menos investimento. A marca própria dá mais controlo e diferenciação, mas exige conhecimento de produção e mais capital para amostras e quantidades mínimas."),
      ("Posso passar da revenda para a marca própria?",
       "Sim. Muitas marcas usam a revenda para perceber o que a cliente compra e só depois desenvolvem produto próprio. O importante é tomar essa decisão com números: margem, rotação de stock e procura real.")],
     5)

# Guias hub
cards = "".join(f'<a class="card" href="{p}"><span class="tag">{e(tag)}</span><h3>{e(t)}</h3><p>{e(d)}</p><span class="go">Ler o guia →</span></a>' for p, t, d, tag in GUIAS)
home = home.replace("__GUIAS__", cards)
write("/", home, "1.0")

c_h, c_s = crumbs([("Guias", "/guias/")])
p = head("/guias/", "Guias para marcas de moda · Tânia Silveira",
         "Guias práticos sobre preço, margem, fornecedores têxteis e estrutura para marcas de moda, escritos por uma estrategista com experiência de chão de fábrica.",
         [c_s, {"@type": "CollectionPage", "name": "Guias para marcas de moda", "url": SITE + "/guias/", "author": {"@id": SITE + "/#tania"},
                "hasPart": [{"@id": SITE + g[0] + "#artigo"} for g in GUIAS]}])
p += f"""<section class="page-head"><div class="wrap">{c_h}
<span class="eyebrow">Guias</span><h1>Respostas de quem <em>já esteve na fábrica.</em></h1>
<p class="lead">Preço, margem, fornecedores, coleção. O que precisas de saber para decidir com critério, sem teoria.</p></div></section>
<section style="padding-top:0"><div class="wrap"><div class="cards">{cards}</div></div></section>
{final_cta()}""" + FOOT
write("/guias/", p, "0.8")

# =====================================================================
# SERVIÇOS
# =====================================================================
def service_page(path, nome, titulo_seo, desc, eyebrow, h1, lead, resumo, cta_label, cta_href, blocos, faqs, extra_schema=None, crumb=None):
    c_h, c_s = crumbs([("Serviços", "/servicos/"), (nome, path)] if crumb is None else crumb)
    f_h, f_s = faq_block(faqs)
    sc = [service_schema(path, nome, desc, extra_schema), c_s, f_s, PERSON]
    p = head(path, titulo_seo, desc, sc)
    p += f"""<section class="page-head"><div class="wrap">{c_h}
<span class="eyebrow">{eyebrow}</span><h1>{h1}</h1>
<p class="lead">{lead}</p>
<div class="btns" style="margin-top:30px"><a class="btn" href="{cta_href}"{' target="_blank" rel="noopener"' if cta_href.startswith('http') else ''}>{cta_label}</a></div>
</div></section>
<div class="wrap narrow"><div class="tldr"><strong>Em resumo</strong>{resumo}</div></div>
{blocos}
<section class="alt"><div class="wrap narrow"><div class="head"><span class="eyebrow">Perguntas frequentes</span><h2>O que me <em>perguntam.</em></h2></div>{f_h}</div></section>
<section class="dark final"><div class="wrap"><h2>Bora fazer <em>acontecer?</em></h2>
<div class="btns"><a class="btn light" href="{cta_href}"{' target="_blank" rel="noopener"' if cta_href.startswith('http') else ''}>{cta_label}</a></div></div></section>
""" + FOOT
    write(path, p, "0.9")

# Diagnóstico
service_page("/diagnostico-alinhavar/", "Diagnóstico Alinhavar",
    "Diagnóstico Alinhavar · Diagnóstico estratégico para marcas de moda",
    "Sessão de 30 minutos para identificar o que trava a tua marca de moda: produto, margem, posicionamento ou decisão. Com a estrategista têxtil Tânia Silveira.",
    "Diagnóstico estratégico · 30 minutos",
    "Antes de mudar tudo, <em>percebe o que está errado.</em>",
    "Alinhavar é o ponto de costura provisório que segura a peça antes da costura final. É isso que esta sessão faz: alinha o que está solto antes de investires mais.",
    "<p>O Diagnóstico Alinhavar é uma sessão estratégica de 30 minutos para marcas de moda que já estão a operar e não percebem o que trava o crescimento. Saio da sessão com o gargalo identificado (produto, margem, posicionamento ou decisão) e tu sais com a prioridade clara. A entrada é por candidatura.</p>",
    "Candidatar-me ao diagnóstico", LINKS["diagnostico"],
    f"""<section><div class="wrap split top">
<div><span class="eyebrow">Para quem é</span><h2>Para marcas que trabalham muito <em>e não sabem porque não crescem.</em></h2></div>
<div><ul class="steps">
<li><div><b>Já vendes, mas fica pouco.</b><p>Faturas, mas no fim do mês a margem não aparece.</p></div></li>
<li><div><b>Mudas tudo e nada muda.</b><p>Novo feed, novo logótipo, nova coleção. O problema continua.</p></div></li>
<li><div><b>Vives de descontos.</b><p>Sem promoção, não vendes. Com promoção, não ganhas.</p></div></li>
</ul></div></div></section>
<section class="alt"><div class="wrap split top">
<div><span class="eyebrow">Como funciona</span><h2>Três passos. <em>Sem rodeios.</em></h2></div>
<div><ol class="steps">
<li><div><b>Candidatura</b><p>Respondes a umas perguntas sobre a marca. Eu leio tudo antes da sessão.</p></div></li>
<li><div><b>Sessão de 30 minutos</b><p>Olhamos para produto, margem, posicionamento e decisões. Nomeio o gargalo.</p></div></li>
<li><div><b>Próximo passo</b><p>Sais a saber o que decidir primeiro e se precisas de acompanhamento ou não.</p></div></li>
</ol></div></div></section>
<section><div class="wrap"><div class="versus">
<div><h3>O diagnóstico é</h3><ul><li>Uma leitura estratégica da tua marca</li><li>O problema real, nomeado</li><li>Uma prioridade clara</li></ul></div>
<div><h3>O diagnóstico não é</h3><ul><li>Uma sessão de dicas de Instagram</li><li>Um plano completo de 6 meses</li><li>Uma promessa de resultados</li></ul></div>
</div></div></section>""",
    [("Quanto tempo dura o Diagnóstico Alinhavar?", "30 minutos, online."),
     ("Porque é por candidatura?", "Porque preciso de conhecer a marca antes da sessão. Assim os 30 minutos são usados a decidir, não a apresentar."),
     ("O que acontece depois do diagnóstico?", "Ficas com a prioridade clara. Se fizer sentido, falamos sobre o <a href=\"/metodo-fibra/\">Método FIBRA</a> ou a <a href=\"/consultoria-tafeta-360/\">Consultoria Tafetá 360</a>. Se não fizer, digo-te.")],
    {"offers": {"@type": "Offer", "url": LINKS["diagnostico"], "availability": "https://schema.org/InStock"}})

# FIBRA
service_page("/metodo-fibra/", "Método FIBRA",
    "Método FIBRA · Acompanhamento estratégico de 6 meses para marcas de moda",
    "Método FIBRA: acompanhamento estratégico 1:1 de 6 meses para marcas de moda. Coleção, produto, margem, posicionamento e mentalidade de decisão, com Tânia Silveira.",
    "Programa principal · 6 meses · 1:1",
    "O Método FIBRA não é mentoria de conteúdo. <em>É estrutura de negócio.</em>",
    "Em 6 meses, a tua marca passa a ter direção, margem e decisões com critério. Trabalhamos lado a lado, da coleção à forma como pensas o negócio.",
    "<p>O Método FIBRA é um acompanhamento estratégico individual de 6 meses para marcas de moda que já perceberam o problema e precisam de o resolver com estrutura. Assenta em três pilares: Mentalidade, Produto e Digital. Inclui organização de coleção, lógica de produto, ajuste de margem, direção de posicionamento e desenvolvimento de mentalidade de decisão. A entrada é por candidatura.</p>",
    "Candidatar-me ao Método FIBRA", LINKS["fibra"],
    f"""<section class="dark"><div class="wrap">
<div class="head"><span class="eyebrow">Os três pilares</span><h2>Mentalidade. Produto. <em>Digital.</em></h2>
<p class="lead">Por esta ordem. Porque sem decisão não há produto, e sem produto não há comunicação que resulte.</p></div>
<div class="pillars three">
<div><b>Mentalidade</b><p>Sais do operacional e passas a gerir como CEO. Decides com critério, não por impulso nem por pressão do mês.</p></div>
<div><b>Produto</b><p>Coleção organizada, lógica de produto, preço e margem. Cada peça tem um papel e paga o seu lugar.</p></div>
<div><b>Digital</b><p>Posicionamento e comunicação alinhados com o produto. Falas para a cliente certa, com a mensagem certa.</p></div>
</div></div></section>
<section><div class="wrap split top">
<div><span class="eyebrow">O que trabalhamos</span><h2>Seis meses. <em>A marca inteira.</em></h2>
<p class="lead">Cada marca tem o seu ritmo. Esta é a lógica do percurso.</p>
<figure class="photo">{pic("moodboard-colecao-moda", "Moodboards e esboços de coleção em cima da mesa de trabalho")}</figure></div>
<div><ol class="steps">
<li><div><b>Diagnóstico profundo</b><p>Números, coleção, cliente, operação. Onde está o dinheiro e onde se perde.</p></div></li>
<li><div><b>Organização de coleção</b><p>Que peças ficam, que peças saem, que peças faltam. Lógica de produto.</p></div></li>
<li><div><b>Preço e margem</b><p>Custos reais, preços com critério, margem que sustenta o negócio.</p></div></li>
<li><div><b>Posicionamento</b><p>Quem é a tua cliente, porque compra a ti e como o dizes.</p></div></li>
<li><div><b>Estrutura e decisão</b><p>Rotinas, prioridades e critérios para decidires sem depender de mim.</p></div></li>
</ol></div></div></section>
<section class="alt"><div class="wrap"><div class="versus">
<div><h3>É para ti se</h3><ul><li>A tua marca já existe e já vende</li><li>Sabes que o problema é de estrutura, não de esforço</li><li>Estás disposta a tomar decisões difíceis</li><li>Queres crescer com previsibilidade</li></ul></div>
<div><h3>Não é para ti se</h3><ul><li>Procuras atalhos, hacks ou fórmulas rápidas</li><li>Queres alguém que faça o conteúdo por ti</li><li>Esperas resultados garantidos sem mudar nada</li></ul></div>
</div></div></section>
<section><div class="wrap"><div class="head"><span class="eyebrow">Casos reais</span><h2>O que muda <em>com estrutura.</em></h2></div>{casos_html()}</div></section>
{feedbacks_html()}""",
    [("Quanto tempo dura o Método FIBRA?", "6 meses de acompanhamento estratégico individual."),
     ("O Método FIBRA é online?", "Sim. As sessões são online, para marcas de todo o país. Quando faz sentido, podem ser presenciais."),
     ("Qual a diferença entre o Método FIBRA e uma mentoria de Instagram?", "O FIBRA trabalha o negócio: coleção, produto, preço, margem e decisão. A comunicação entra no fim, alinhada com o produto. Não é uma mentoria de conteúdo."),
     ("Como entro no Método FIBRA?", "Por candidatura. Leio cada candidatura e só aceito marcas onde sei que posso fazer diferença.")],
    {"offers": {"@type": "Offer", "url": LINKS["fibra"], "availability": "https://schema.org/LimitedAvailability"}})

# Tafetá
service_page("/consultoria-tafeta-360/", "Consultoria Tafetá 360",
    "Consultoria Tafetá 360 · Consultoria estratégica para marcas de moda",
    "Consultoria Tafetá 360: sessão estratégica de 2 horas + seguimento de 1 hora ao fim de um mês, para marcas de moda que já vendem e precisam de afinar produto, margem e estratégia comercial.",
    "Consultoria · 2 horas + 1 hora",
    "Para quem já tem a marca a funcionar <em>e quer afinar com precisão.</em>",
    "Uma intervenção estratégica para marcas com base criada. Corrigimos falhas estruturais, afinamos produto e margem e definimos uma direção comercial clara.",
    "<p>A Consultoria Tafetá 360 é uma sessão estratégica de 2 horas, seguida de uma sessão de seguimento de 1 hora ao fim de um mês. É para marcas de moda que já vendem e precisam de impacto sem o compromisso de um acompanhamento de 6 meses. Foco em produto, margem, falhas estruturais e estratégia comercial.</p>",
    "Agendar a Tafetá 360", LINKS["tafeta"],
    """<section><div class="wrap split top">
<div><span class="eyebrow">O que trabalhamos</span><h2>Visão 360. <em>Decisões concretas.</em></h2></div>
<div><ol class="steps">
<li><div><b>Sessão estratégica de 2 horas</b><p>Olhamos para a marca inteira: produto, margem, posicionamento, operação comercial.</p></div></li>
<li><div><b>Plano de correção</b><p>Sais com as falhas identificadas e as decisões que tens de tomar, por ordem.</p></div></li>
<li><div><b>Um mês para aplicar</b><p>Implementas. É aqui que se vê o que funciona.</p></div></li>
<li><div><b>Seguimento de 1 hora</b><p>Revemos o que mudou, ajustamos e definimos o passo seguinte.</p></div></li>
</ol></div></div></section>
<section class="alt"><div class="wrap"><div class="versus">
<div><h3>Tafetá 360</h3><ul><li>Intervenção pontual</li><li>Para marcas que já funcionam</li><li>2 horas + 1 hora de seguimento</li><li>Afinar o que existe</li></ul></div>
<div><h3>Método FIBRA</h3><ul><li>Acompanhamento de 6 meses</li><li>Para marcas que precisam de estrutura</li><li>Trabalho 1:1 contínuo</li><li>Reestruturar o negócio</li></ul></div>
</div><p style="margin-top:22px"><a class="link" href="/metodo-fibra/">Conhecer o Método FIBRA →</a></p></div></section>""",
    [("Quanto tempo dura a Consultoria Tafetá 360?", "Uma sessão de 2 horas e uma sessão de seguimento de 1 hora, um mês depois."),
     ("A Tafetá 360 serve para marcas que estão a começar?", "Não é o ideal. É pensada para marcas com base criada que já vendem. Se estás a começar, o <a href=\"/diagnostico-alinhavar/\">Diagnóstico Alinhavar</a> ou a <a href=\"/lista-estrategica-de-fornecedores/\">Lista de Fornecedores</a> fazem mais sentido.")])

# Serviços (visão geral)
c_h, c_s = crumbs([("Serviços", "/servicos/")])
p = head("/servicos/", "Serviços · Estratégia para marcas de moda · Tânia Silveira",
         "Diagnóstico Alinhavar, Método FIBRA, Consultoria Tafetá 360 e Lista Estratégica de Fornecedores. Escolhe o ponto de entrada certo para a fase da tua marca de moda.",
         [c_s, {"@type": "ItemList", "itemListElement": [
             {"@type": "ListItem", "position": i + 1, "url": SITE + u} for i, u in enumerate(
                 ["/diagnostico-alinhavar/", "/metodo-fibra/", "/consultoria-tafeta-360/", "/lista-estrategica-de-fornecedores/", "/empresas/"])]}])
p += f"""<section class="page-head"><div class="wrap">{c_h}
<span class="eyebrow">Serviços</span><h1>Um ponto de entrada <em>para cada fase.</em></h1>
<p class="lead">Não são serviços soltos. É um caminho: da clareza à estrutura.</p></div></section>
<section style="padding-top:0"><div class="wrap">
<table class="prose" style="max-width:none;width:100%;border-collapse:collapse;background:#fff;font-size:15px">
<tr style="background:var(--paper2)"><th style="padding:14px;border:1px solid var(--line);text-align:left">Serviço</th><th style="padding:14px;border:1px solid var(--line);text-align:left">Para quem</th><th style="padding:14px;border:1px solid var(--line);text-align:left">Formato</th></tr>
<tr><td style="padding:14px;border:1px solid var(--line)"><a class="link" href="/lista-estrategica-de-fornecedores/">Lista de Fornecedores</a></td><td style="padding:14px;border:1px solid var(--line)">Quem está a começar e procura parceiros</td><td style="padding:14px;border:1px solid var(--line)">Acesso digital, 6 meses</td></tr>
<tr><td style="padding:14px;border:1px solid var(--line)"><a class="link" href="/diagnostico-alinhavar/">Diagnóstico Alinhavar</a></td><td style="padding:14px;border:1px solid var(--line)">Marcas a operar que não sabem o que as trava</td><td style="padding:14px;border:1px solid var(--line)">30 minutos, por candidatura</td></tr>
<tr><td style="padding:14px;border:1px solid var(--line)"><a class="link" href="/consultoria-tafeta-360/">Consultoria Tafetá 360</a></td><td style="padding:14px;border:1px solid var(--line)">Marcas que já vendem e precisam de afinar</td><td style="padding:14px;border:1px solid var(--line)">2 horas + 1 hora ao fim de um mês</td></tr>
<tr><td style="padding:14px;border:1px solid var(--line)"><a class="link" href="/metodo-fibra/">Método FIBRA</a></td><td style="padding:14px;border:1px solid var(--line)">Marcas que precisam de estrutura para crescer</td><td style="padding:14px;border:1px solid var(--line)">6 meses, 1:1, por candidatura</td></tr>
<tr><td style="padding:14px;border:1px solid var(--line)"><a class="link" href="/empresas/">Consultoria para empresas</a></td><td style="padding:14px;border:1px solid var(--line)">Fábricas, confeções e marcas com equipa</td><td style="padding:14px;border:1px solid var(--line)">Consultoria inicial + plano à medida</td></tr>
</table>
</div></section>
{final_cta("Não sabes qual é o teu? <em>Começa pelo diagnóstico.</em>", "Em 30 minutos digo-te onde está o problema e qual o caminho certo para a tua marca.")}""" + FOOT
write("/servicos/", p, "0.9")

# Lista de fornecedores (mesmo URL do site atual)
c_h, c_s = crumbs([("Lista de Fornecedores", "/lista-estrategica-de-fornecedores/")])
lista_faq = [("A lista tem atualizações?", "Não. O acesso dura 6 meses e a lista não é atualizada durante esse período."),
             ("A lista substitui um diagnóstico?", "Não. É uma ferramenta de apoio à decisão. As condições, os prazos e a adequação à tua marca têm de ser confirmados diretamente com cada fornecedor."),
             ("O que inclui o Combo Experiência?", "As duas listas, Revenda e Marca do Zero, e uma hora comigo para alinhar o negócio, clarificar a fase em que estás e definir os próximos passos.")]
f_h, f_s = faq_block(lista_faq)
prod = lambda n, d, pr, link: {"@type": "Product", "name": n, "description": d, "brand": {"@type": "Brand", "name": "Tânia Silveira"},
                                "offers": {"@type": "Offer", "price": pr, "priceCurrency": "EUR", "url": link, "availability": "https://schema.org/InStock"}}
p = head("/lista-estrategica-de-fornecedores/", "Lista de Fornecedores Têxteis em Portugal · Revenda e Marca Própria",
         "Contactos de fornecedores têxteis em Portugal para revenda de roupa e para criar marca própria: tecidos, malhas, confeções, estampados, bordados e etiquetas. Desde 49 €.",
         [c_s, f_s, prod("Lista de Fornecedores de Revenda", "Contactos de fornecedores de roupa pronta, organizados por categoria. 6 meses de acesso.", "49.00", LINKS["lista_revenda"]),
          prod("Lista de Fornecedores Marca do Zero", "Tecidos, malhas, confeções, estampados, bordados e etiquetas para criar produto próprio. 6 meses de acesso.", "49.00", LINKS["lista_zero"]),
          prod("Combo Experiência", "Lista de Revenda + Marca do Zero e 1 hora com Tânia Silveira. 6 meses de acesso.", "69.00", LINKS["lista_combo"])])
p += f"""<section class="page-head"><div class="wrap">{c_h}
<span class="eyebrow">Ferramenta estratégica</span><h1>Já tens a ideia. <em>Agora encontra com quem avançar.</em></h1>
<p class="lead">Contactos do setor têxtil para escolheres fornecedores de revenda ou parceiros para criares produto próprio. Organizados por critério de decisão.</p>
<div class="btns" style="margin-top:30px"><a class="btn" href="#precos">Escolher a minha lista</a></div></div></section>
<div class="wrap narrow"><div class="tldr"><strong>Em resumo</strong><p>A Lista Estratégica de Fornecedores reúne contactos de fornecedores têxteis em Portugal, em duas versões: Revenda (roupa pronta) e Marca do Zero (tecidos, malhas, confeções, estampados, bordados e etiquetas). Acesso digital individual de 6 meses, pagamento único, IVA incluído.</p></div></div>
<section style="padding-top:20px"><div class="wrap"><div class="versus">
<div><h3>Esta lista é</h3><ul><li>Uma ferramenta de apoio à decisão</li><li>Um atalho para a informação, não para a estratégia</li><li>Um ponto de partida organizado</li></ul></div>
<div><h3>Esta lista não é</h3><ul><li>Um substituto de diagnóstico</li><li>Um plano de crescimento</li><li>Uma garantia de condições ou prazos</li></ul></div>
</div></div></section>
<section class="alt" id="precos"><div class="wrap">
<div class="head"><span class="eyebrow">O teu investimento</span><h2>Três opções. <em>A mesma intenção.</em></h2></div>
<div class="prices">
<div class="price"><span class="eyebrow">01 · Roupa pronta</span><h3>Revenda</h3><div class="v">49 €</div><p class="small" style="font-size:13px;color:var(--muted)">IVA incluído · pagamento único</p>
<ul><li>Fornecedores de revenda</li><li>Contactos organizados por categoria</li><li>6 meses de acesso</li></ul>
<a class="btn ghost" href="{LINKS['lista_revenda']}" target="_blank" rel="noopener">Comprar a lista de revenda</a></div>
<div class="price"><span class="eyebrow">02 · Produção própria</span><h3>Marca do Zero</h3><div class="v">49 €</div><p style="font-size:13px;color:var(--muted)">IVA incluído · pagamento único</p>
<ul><li>Tecidos, malhas e confeções</li><li>Estampados, bordados e etiquetas</li><li>6 meses de acesso</li></ul>
<a class="btn ghost" href="{LINKS['lista_zero']}" target="_blank" rel="noopener">Comprar a Marca do Zero</a></div>
<div class="price main"><span class="eyebrow">03 · Duas listas + direção</span><h3>Combo Experiência</h3><div class="v">69 €</div><p style="font-size:13px;color:var(--muted)">IVA incluído · pagamento único</p>
<ul><li>Revenda + Marca do Zero</li><li>1 hora comigo para alinhar o negócio</li><li>6 meses de acesso às duas listas</li></ul>
<a class="btn" href="{LINKS['lista_combo']}" target="_blank" rel="noopener">Quero o Combo</a></div>
</div>
<p style="margin-top:20px;font-size:14px;color:var(--muted)">Sem atualizações durante o acesso. A hora comigo está incluída apenas no Combo Experiência.</p>
</div></section>
<section><div class="wrap narrow">
<p class="quote">Criei esta lista a partir de uma dificuldade que se repetia nas marcas que acompanhava: <em>não saber por onde começar a procurar parceiros.</em></p>
<p class="sig" style="margin-top:20px">Tânia Silveira</p>
<p>Antes de contactares fornecedores, lê o guia <a class="link" href="/guias/como-escolher-fornecedor-textil-em-portugal/">Como escolher um fornecedor têxtil em Portugal</a>.</p>
</div></section>
<section class="alt"><div class="wrap narrow"><div class="head"><span class="eyebrow">Perguntas frequentes</span><h2>Antes de <em>comprares.</em></h2></div>{f_h}</div></section>
""" + FOOT
write("/lista-estrategica-de-fornecedores/", p, "0.9")


# =====================================================================
# EMPRESAS
# =====================================================================
emp_faq = [
    ("Como começa o trabalho com uma empresa?", "Sempre por uma consultoria. Conheço a empresa, a equipa, o produto e os números. Só depois apresento um plano, à medida do que encontrei."),
    ("Quanto custa?", "O valor da consultoria é indicado no primeiro contacto. Os planos são construídos para cada empresa, por isso o investimento é apresentado com o plano."),
    ("Trabalhas presencialmente?", "Sim. Estou em Guimarães, no centro da indústria têxtil, e vou às empresas sempre que o trabalho o pede. Também trabalho online."),
    ("Que tipo de empresas acompanhas?", "Fábricas, confeções, empresas têxteis e marcas de moda com equipa e operação montada."),
]
c_h, c_s = crumbs([("Empresas", "/empresas/")])
f_h, f_s = faq_block(emp_faq)
p = head("/empresas/", "Consultoria para empresas têxteis e de moda · Tânia Silveira",
         f"Consultoria estratégica para fábricas, confeções, empresas têxteis e marcas de moda com equipa. Começa por uma consultoria e segue com um plano à medida. {ANOS} anos de chão de fábrica.",
         [service_schema("/empresas/", "Consultoria para empresas têxteis e de moda",
                         "Consultoria estratégica para empresas têxteis e de moda: começa por uma consultoria à empresa e segue com um plano à medida.",
                         {"audience": {"@type": "BusinessAudience", "name": "Fábricas, confeções, empresas têxteis e marcas de moda com equipa"}}),
          c_s, f_s, PERSON])
p += f"""<section class="page-head"><div class="wrap">{c_h}
<span class="eyebrow">Para empresas</span><h1>Antes de um plano, <em>uma consultoria.</em></h1>
<p class="lead">Para fábricas, confeções, empresas têxteis e marcas de moda com equipa. Entro na empresa, olho para o que está a travar o crescimento e só depois proponho o caminho.</p>
<div class="btns" style="margin-top:30px"><a class="btn" href="#pedido">Pedir uma consultoria</a></div></div></section>
<div class="wrap narrow"><div class="tldr"><strong>Em resumo</strong><p>O trabalho de Tânia Silveira com empresas começa sempre por uma consultoria: conhecer a empresa, a equipa, o produto e os números. A partir dessa consultoria é apresentado um plano à medida de cada empresa. Atende presencialmente a partir de Guimarães e online.</p></div></div>
<section><div class="wrap split top">
<div><span class="eyebrow">Como funciona</span><h2>Primeiro percebo. <em>Depois proponho.</em></h2>
<p class="lead">Nenhuma empresa recebe um plano feito antes de eu a conhecer.</p></div>
<div><ol class="steps">
<li><div><b>Primeiro contacto</b><p>Contas-me o que se passa na empresa. Vemos se faz sentido avançar.</p></div></li>
<li><div><b>Consultoria</b><p>Conheço a empresa por dentro: produto, operação, equipa, números e decisões.</p></div></li>
<li><div><b>Plano à medida</b><p>Apresento o que encontrei e um plano com prioridades, formato e investimento.</p></div></li>
<li><div><b>Execução</b><p>Se o plano avançar, acompanho a implementação nos termos definidos.</p></div></li>
</ol></div></div></section>
<section class="dark"><div class="wrap">
<div class="head"><span class="eyebrow">Onde intervenho</span><h2>Do produto <em>à decisão.</em></h2></div>
<div class="pillars">
<div><b>Coleção e vendas</b><p>Que produto faz sentido, o que vende, o que fica parado.</p></div>
<div><b>Custo e preço</b><p>Custos reais, preços com critério, margem que aguenta a estrutura.</p></div>
<div><b>Mercado têxtil</b><p>Posicionamento, clientes e parceiros certos para a fase da empresa.</p></div>
<div><b>Processos e IA</b><p>Rotinas, ferramentas e uso de IA onde poupa tempo. A IA acelera. O critério vem da fábrica.</p></div>
</div></div></section>
<section><div class="wrap split">
<div><span class="eyebrow">Porquê comigo</span><h2>Falo a língua <em>da fábrica e da marca.</em></h2>
<figure class="photo">{pic("mostruario-tecidos-ficha-tecnica", "Mãos a escolher tecidos num mostruário, ao lado de esboços técnicos")}</figure></div>
<div><p>São {ANOS} anos dentro da indústria têxtil: produção, planeamento, produto, fornecedores e gestão comercial. Sei o que acontece entre o tecido e a cliente, e onde as empresas perdem margem sem dar por isso.</p>
<p>Não trago modelos de consultora grande aplicados a frio. Trago critério de quem já esteve no chão de fábrica.</p></div>
</div></section>
<section class="alt" id="pedido"><div class="wrap split top">
<div><span class="eyebrow">Pedir uma consultoria</span><h2>Bora fazer <em>acontecer?</em></h2>
<p class="lead">Conta-me um pouco sobre a empresa. Respondo pessoalmente.</p></div>
<form class="form" name="empresas" method="POST" action="/obrigada/" data-netlify="true" netlify-honeypot="website">
<input type="hidden" name="form-name" value="empresas">
<p class="hp"><label>Não preencher <input name="website"></label></p>
<div><label for="e-nome">Nome</label><input id="e-nome" name="nome" required autocomplete="name"></div>
<div><label for="e-empresa">Empresa</label><input id="e-empresa" name="empresa" required autocomplete="organization"></div>
<div><label for="e-cargo">Cargo</label><input id="e-cargo" name="cargo" autocomplete="organization-title"></div>
<div><label for="e-email">Email</label><input id="e-email" name="email" type="email" required autocomplete="email"></div>
<div><label for="e-tel">Telefone</label><input id="e-tel" name="telefone" type="tel" autocomplete="tel"></div>
<div><label for="e-tipo">Tipo de empresa</label><select id="e-tipo" name="tipo"><option>Fábrica ou confeção</option><option>Empresa têxtil</option><option>Marca de moda com equipa</option><option>Retalho</option><option>Outra</option></select></div>
<div><label for="e-msg">O que se passa na empresa?</label><textarea id="e-msg" name="mensagem" required></textarea></div>
<p style="font-size:13px;color:var(--muted);margin:0">Ao enviar, aceitas a <a href="/politica-de-privacidade/">política de privacidade</a>.</p>
<div><button class="btn" type="submit">Pedir consultoria</button></div>
</form></div></section>
<section><div class="wrap narrow"><div class="head"><span class="eyebrow">Perguntas frequentes</span><h2>O que as empresas <em>me perguntam.</em></h2></div>{f_h}</div></section>
""" + FOOT
write("/empresas/", p, "0.9")


# =====================================================================
# FERRAMENTAS
# =====================================================================
QUIZ = {
    "stage": {"text": "Em que fase está a tua marca?", "options": [
        {"value": "inicio", "label": "Ainda não lancei, ou lancei há pouco"},
        {"value": "operacao", "label": "Já vendo, mas com muito esforço e pouca margem"},
        {"value": "escala", "label": "Vendo bem, mas quero afinar e crescer com precisão"}]},
    "statements": [
        {"area": "produto", "text": "Crio peças novas porque gosto delas, não porque a coleção precisa delas."},
        {"area": "margem", "text": "Defino o preço a olhar para a concorrência, não para os meus custos."},
        {"area": "posicionamento", "text": "Se tapasse o logótipo, a minha marca podia ser confundida com outra."},
        {"area": "decisao", "text": "Mudo de direção sempre que algo não vende como esperava."},
        {"area": "produto", "text": "Não sei quais são as peças que realmente pagam a coleção."},
        {"area": "margem", "text": "Faço descontos para conseguir vender."},
        {"area": "posicionamento", "text": "Não consigo explicar numa frase para quem é a minha marca."},
        {"area": "decisao", "text": "Tomo as decisões importantes por impulso, sem um critério definido."}],
    "answers": [{"value": 2, "label": "Sim"}, {"value": 1, "label": "Às vezes"}, {"value": 0, "label": "Não"}],
    "labels": {"produto": "Produto", "margem": "Margem", "posicionamento": "Posicionamento", "decisao": "Decisão"},
    "services": {
        "fibra": {"name": "Método FIBRA", "href": "/metodo-fibra/", "why": "O que encontraste aqui pede estrutura e acompanhamento, não um ajuste pontual."},
        "tafeta": {"name": "Consultoria Tafetá 360", "href": "/consultoria-tafeta-360/", "why": "A base existe. Uma intervenção focada chega para corrigir e afinar."}},
    "results": {
        "produto": {"title": "O teu gargalo está no produto.", "text": "A coleção cresce por gosto, não por lógica. Há peças a ocupar stock e orçamento sem pagar o lugar que têm. Sem saber o que vende e porquê, cada coleção nova é uma aposta.",
                    "actions": ["Lista as peças da última coleção por unidades vendidas e por margem. As de cima dizem-te onde está a marca.", "Define a função de cada peça antes de a desenhar: entrada, margem ou imagem.", "Corta o que não tem função. Menos referências, mais critério."]},
        "margem": {"title": "O teu gargalo está na margem.", "text": "Vendes, mas o dinheiro não fica. Preço definido pela concorrência e descontos para escoar são sinal de que o custo real nunca foi feito até ao fim.",
                   "actions": ["Faz a conta completa por peça: produção, aviamentos, amostras, portes, comissões e devoluções.", "Revê o preço a partir do custo real, não do que os outros cobram.", "Trava os descontos permanentes. Desconto sem estratégia ensina a cliente a esperar."]},
        "posicionamento": {"title": "O teu gargalo está no posicionamento.", "text": "A marca existe, mas não se distingue. Quando a cliente não percebe porque és tu, a decisão dela passa a ser o preço.",
                           "actions": ["Escreve numa frase: para quem é, que problema resolve, porque és tu. Se não cabe numa frase, ainda não está claro.", "Confirma que produto, preço e comunicação dizem a mesma coisa.", "Deixa de falar para toda a gente. Uma cliente bem definida vende mais do que um público largo."]},
        "decisao": {"title": "O teu gargalo está na decisão.", "text": "Há esforço, mas não há critério. Mudar de direção a cada venda fraca não é flexibilidade. É falta de estrutura para decidir.",
                    "actions": ["Define 3 critérios fixos para aprovar qualquer decisão de coleção, preço ou investimento.", "Dá tempo às decisões antes de as mudar. Uma coleção não se avalia em duas semanas.", "Separa o urgente do estrutural. Reserva tempo na semana só para o estrutural."]},
        "solida": {"title": "A tua base está sólida.", "text": "Não há um gargalo evidente. O próximo passo é afinar com precisão para crescer sem perder margem nem controlo.",
                   "actions": ["Confirma a margem real das tuas 5 peças mais vendidas.", "Revê se a coleção seguinte mantém a lógica que está a resultar.", "Identifica a próxima decisão estrutural e trata-a antes de ser urgente."]}},
}

def tool_schema(path, name, desc):
    return {"@type": "WebApplication", "name": name, "url": SITE + path, "description": desc, "applicationCategory": "BusinessApplication",
            "operatingSystem": "Web", "inLanguage": "pt-PT", "isAccessibleForFree": True,
            "offers": {"@type": "Offer", "price": "0", "priceCurrency": "EUR"}, "author": {"@id": SITE + "/#tania"}}

# Calculadora
c_h, c_s = crumbs([("Ferramentas", "/ferramentas/"), ("Calculadora de margem", "/calculadora-de-margem/")])
calc_faq = [("Como se calcula a margem de uma peça de roupa?", "Margem = (preço recebido sem IVA − custo total) ÷ preço recebido sem IVA. O custo total inclui produção, aviamentos, amostras divididas pelas unidades, portes, taxas de pagamento, comissões e devoluções."),
            ("Que margem deve ter uma marca de roupa?", "A calculadora usa 60% como referência de trabalho para venda direta à cliente final. Venda por grosso, consignação e marketplaces têm outra conta. A margem certa é a que paga a estrutura da tua marca.")]
f_h, f_s = faq_block(calc_faq)
CF = [("Custo da peça", [("producao", "Produção por peça", "Tecido + confeção", "€", "0.1", 18), ("aviamentos", "Aviamentos e embalagem", "Etiquetas, botões, saco, caixa", "€", "0.1", 2.5),
                         ("amostras", "Amostras e desenvolvimento", "Total gasto neste modelo", "€", "10", 600), ("unidades", "Unidades produzidas", "Para dividir o desenvolvimento", "un.", "1", 200)]),
      ("Custos de vender", [("portes", "Portes por envio", "O que pagas tu, não a cliente", "€", "0.1", 4.5), ("taxas", "Taxas de pagamento", "Stripe, MB Way, PayPal…", "%", "0.1", 2.5),
                            ("comissoes", "Comissões", "Marketplace, loja, afiliados", "%", "1", 0), ("devolucoes", "Taxa de devoluções", "Em cada 100 vendas, quantas voltam", "%", "1", 8)]),
      ("Preço", [("pvp", "PVP com IVA", "O preço que a cliente vê", "€", "1", 79), ("desconto", "Desconto médio", "Média real, com saldos e códigos", "%", "1", 10), ("iva", "IVA", "23% no continente", "%", "1", 23)])]
fields = "".join(f'<fieldset class="cgroup"><legend>{g}</legend><div class="cgrid">' + "".join(
    f'<div><label for="c-{k}">{lab}</label><div class="cin"><input id="c-{k}" data-k="{k}" type="number" inputmode="decimal" min="0" step="{st}" value="{dv}" aria-describedby="c-{k}-h"><span>{suf}</span></div><small id="c-{k}-h">{h}</small></div>'
    for k, lab, h, suf, st, dv in fs) + '</div></fieldset>' for g, fs in CF)
p = head("/calculadora-de-margem/", "Calculadora de margem para marcas de roupa · Tânia Silveira",
         "Calcula a margem real de uma peça de roupa: produção, aviamentos, amostras, portes, taxas, devoluções, descontos e IVA. Grátis, feita por uma estrategista têxtil.",
         [tool_schema("/calculadora-de-margem/", "Calculadora de margem para marcas de roupa", "Calcula a margem real por peça de roupa, com IVA, descontos, portes, taxas e devoluções."), c_s, f_s])
p += f"""<section class="page-head"><div class="wrap">{c_h}
<span class="eyebrow">Ferramenta grátis</span><h1>Calculadora de <em>margem real.</em></h1>
<p class="lead">A margem que pensas que tens e a que tens de facto raramente são a mesma. Mete os números de uma peça e vê para onde vai o dinheiro.</p></div></section>
<section style="padding-top:0"><div class="wrap calc" id="calc">
<form class="cform" onsubmit="return false" aria-label="Dados da peça">{fields}</form>
<div class="cres" aria-live="polite">
<div class="cbig"><span class="eyebrow">Margem real por peça</span>
<div class="gauge" id="r-gauge"><i></i></div>
<b id="r-pct" class="big">0%</b><p id="r-eur"></p>
<dl><div><dt>Recebes de facto</dt><dd id="r-recebes"></dd></div><div><dt>Custa-te de facto</dt><dd id="r-custa"></dd></div>
<div><dt>PVP ÷ custo da peça</dt><dd id="r-mult"></dd></div><div><dt>PVP para 60% de margem</dt><dd id="r-alvo"></dd></div></dl></div>
<div id="r-verdict" class="verdict"></div>
<div class="cbox"><b>Para onde vai o dinheiro</b><ul id="r-bars" class="bars"></ul><small>Em percentagem do que recebes por peça, sem IVA e com o desconto médio.</small></div>
<div class="cbox"><p>Os 60% são uma referência de trabalho para venda direta à cliente final. A calculadora mostra os números. A decisão sobre o que fazer com eles é estratégica.</p>
<a class="btn" href="/consultoria-tafeta-360/">Rever preço e margem comigo</a></div>
</div></div></section>
<section class="alt"><div class="wrap narrow"><div class="head"><span class="eyebrow">Perguntas frequentes</span><h2>Sobre <em>margem.</em></h2></div>{f_h}
<p style="margin-top:24px"><a class="link" href="/guias/como-calcular-preco-e-margem-de-uma-peca-de-roupa/">Ler o guia completo de preço e margem →</a></p></div></section>
""" + FOOT
write("/calculadora-de-margem/", p, "0.9")

# Autodiagnóstico
c_h, c_s = crumbs([("Ferramentas", "/ferramentas/"), ("Autodiagnóstico", "/autodiagnostico/")])
p = head("/autodiagnostico/", "Autodiagnóstico para marcas de moda · Tânia Silveira",
         "9 perguntas, 2 minutos. Descobre se o que trava a tua marca de moda é o produto, a margem, o posicionamento ou a decisão, e o que fazer primeiro.",
         [tool_schema("/autodiagnostico/", "Autodiagnóstico para marcas de moda", "Questionário de 9 perguntas que identifica o gargalo de uma marca de moda."), c_s])
p += f"""<section class="page-head"><div class="wrap narrow">{c_h}
<span class="eyebrow">Ferramenta grátis · 2 minutos</span><h1>Onde está o <em>gargalo</em> da tua marca?</h1>
<p class="lead">9 perguntas. Responde com verdade, não com o que gostavas que fosse. No fim, vês o que está a travar a marca e os primeiros 3 passos.</p></div></section>
<section style="padding-top:0"><div class="wrap narrow">
<div id="quiz" class="quiz">
<div class="qtop"><span id="quiz-count">Pergunta 1 de 9</span><button type="button" id="quiz-back" class="linkbtn" hidden>← Voltar</button></div>
<div class="qbar"><i id="quiz-bar"></i></div>
<div id="quiz-box" class="qbox"><noscript>Ativa o JavaScript para fazer o autodiagnóstico.</noscript></div>
</div>
<div id="quiz-result" hidden>
<div class="qcard"><span class="eyebrow">O teu resultado</span><h2 id="qr-title"></h2><p id="qr-text" class="lead"></p><ul id="qr-bars" class="bars big"></ul>
<small>Quanto maior a barra, maior o peso dessa área no que está a travar a marca.</small></div>
<div class="qcard"><h3>Os teus primeiros 3 passos</h3><ol id="qr-actions" class="qsteps"></ol>
<p id="qr-margem" hidden><a class="btn ghost" href="/calculadora-de-margem/">Calcular a margem real</a></p>
<p class="note">Este diagnóstico aponta a direção. Não decide por ti. Quem decide é quem conhece o negócio por dentro.</p></div>
<div class="qcard dark"><span class="eyebrow">Recomendo</span><h2 id="qr-svc"></h2><p id="qr-why"></p>
<div class="btns"><a id="qr-link" class="btn light" href="/metodo-fibra/">Ver</a><a class="btn light" href="/diagnostico-alinhavar/">Pedir o Diagnóstico Alinhavar</a></div></div>
<form class="qcard form" id="qr-form" name="autodiagnostico" method="POST" data-netlify="true" netlify-honeypot="bot-field" style="max-width:none">
<input type="hidden" name="form-name" value="autodiagnostico"><input type="hidden" name="fase"><input type="hidden" name="gargalo"><input type="hidden" name="servico_recomendado"><input type="hidden" name="pontuacoes">
<p class="hp"><label>Não preencher <input name="bot-field"></label></p>
<h3>Queres falar sobre este resultado?</h3><p>Deixa os teus dados. Recebo o teu diagnóstico e respondo por email.</p>
<div><label for="q-nome">Nome</label><input id="q-nome" name="nome" required autocomplete="name"></div>
<div><label for="q-email">Email</label><input id="q-email" name="email" type="email" required autocomplete="email"></div>
<div><label for="q-marca">Marca (nome ou Instagram)</label><input id="q-marca" name="marca"></div>
<label class="chk"><input type="checkbox" name="consentimento" value="sim" required><span>Aceito que os meus dados sejam usados para responder a este pedido, conforme a <a href="/politica-de-privacidade/">política de privacidade</a>.</span></label>
<div class="btns"><button class="btn" type="submit">Enviar o meu diagnóstico</button><button class="btn ghost" type="button" id="qr-restart">Refazer</button></div>
<p id="qr-msg" role="status" style="color:var(--terra);margin:0"></p>
</form></div>
<script type="application/json" id="quiz-data">{json.dumps(QUIZ, ensure_ascii=False)}</script>
</div></section>
""" + FOOT
write("/autodiagnostico/", p, "0.9")

# Ferramentas hub
c_h, c_s = crumbs([("Ferramentas", "/ferramentas/")])
p = head("/ferramentas/", "Ferramentas para marcas de moda · Tânia Silveira",
         "Ferramentas para marcas de moda: calculadora de margem real, autodiagnóstico da marca e lista estratégica de fornecedores têxteis em Portugal.",
         [c_s, {"@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": SITE + u} for i, u in enumerate(["/calculadora-de-margem/", "/autodiagnostico/", "/lista-estrategica-de-fornecedores/"])]}])
p += f"""<section class="page-head"><div class="wrap">{c_h}
<span class="eyebrow">Ferramentas</span><h1>Decide com <em>números,</em> não com palpites.</h1>
<p class="lead">Duas ferramentas grátis e uma lista paga. Para usares sozinha, quando quiseres.</p></div></section>
<section style="padding-top:0"><div class="wrap"><div class="cards">
<a class="card" href="/calculadora-de-margem/"><span class="tag">Grátis · 2 minutos</span><h3>Calculadora de margem real</h3><p>Produção, aviamentos, portes, taxas, devoluções, descontos e IVA. Vês quanto ganhas de facto por peça e o preço certo para 60% de margem.</p><span class="go">Fazer a conta →</span></a>
<a class="card" href="/autodiagnostico/"><span class="tag">Grátis · 9 perguntas</span><h3>Autodiagnóstico da marca</h3><p>Produto, margem, posicionamento ou decisão: descobre o que está a travar a tua marca e os primeiros 3 passos.</p><span class="go">Começar →</span></a>
<a class="card" href="/lista-estrategica-de-fornecedores/"><span class="tag">Desde 49 €</span><h3>Lista Estratégica de Fornecedores</h3><p>Contactos do setor têxtil para revenda e para criar produto próprio, organizados por categoria.</p><span class="go">Ver a lista →</span></a>
</div></div></section>
{final_cta()}""" + FOOT
write("/ferramentas/", p, "0.8")

# =====================================================================
# SOBRE
# =====================================================================
c_h, c_s = crumbs([("Sobre", "/sobre/")])
p = head("/sobre/", "Sobre Tânia Silveira · Estrategista têxtil e de marcas de moda",
         f"Tânia Silveira é estrategista de marcas de moda, com {ANOS} anos na indústria têxtil portuguesa. Transmontana, vive em Guimarães. Criou o Método FIBRA.",
         [c_s, {"@type": "ProfilePage", "url": SITE + "/sobre/", "mainEntity": {"@id": SITE + "/#tania"}, "dateModified": HOJE}, PERSON])
p += f"""<section class="page-head"><div class="wrap split">
<div>{c_h}<span class="eyebrow">Sobre</span><h1>Transmontana de raiz. <em>Têxtil de profissão.</em></h1>
<p class="lead">Sou a Tânia Silveira, estrategista de marcas de moda e negócios têxteis. Nasci em Chaves, cresci em Carrazedo de Montenegro e vivo em Guimarães, no coração da indústria têxtil portuguesa.</p></div>
<figure class="portrait" style="max-width:420px">{pic("tania-silveira-estrategista-moda", "Tânia Silveira, estrategista de marcas de moda, sentada com o portátil", h=1521, lazy=False, sizes="(max-width:860px) 90vw, 36vw")}</figure>
</div></section>
<section style="padding-top:0"><div class="wrap prose">
<div class="tldr"><strong>Em resumo</strong><p>Tânia Silveira é estrategista de produto e estrutura para marcas de moda, baseada em Guimarães, Portugal. Tem {ANOS} anos de experiência na indústria têxtil, em chão de fábrica, produção, planeamento, desenvolvimento de produto e gestão comercial. Criou o Método FIBRA, um acompanhamento de 6 meses para marcas de moda, e a Consultoria Tafetá 360.</p></div>
<h2>Do chão de fábrica à estratégia</h2>
<p>A minha experiência começou dentro da indústria. Produção, planeamento, produto, fornecedores, gestão comercial. Aprendi como uma peça nasce, quanto custa de verdade e onde o dinheiro se perde entre o tecido e a cliente.</p>
<p>Foi aí que percebi uma coisa: a maioria das marcas de moda não tem problema de produto. Tem problema de decisão. Fazem coleções sem lógica, preços sem conta e comunicação sem posicionamento. Trabalham muito e crescem pouco.</p>
<h2>O que faço hoje</h2>
<p>Ponho estrutura, margem e direção em marcas de moda. Não faço conteúdo. Não dou dicas. Organizo as decisões que estão por trás da marca, para que cresça com previsibilidade e não dependa de improviso.</p>
<h2>Como trabalho</h2>
<ul>
<li><b>Estrutura antes do crescimento.</b> Crescer em cima de improviso multiplica o problema.</li>
<li><b>Produto antes da comunicação.</b> Nenhum post salva uma coleção mal pensada.</li>
<li><b>Clareza antes da execução.</b> Primeiro decides, depois fazes.</li>
<li><b>Autoridade com verdade.</b> Digo o que vejo, mesmo quando não é o que queres ouvir.</li>
</ul>
<h2>Marcas com quem já trabalhei</h2>
<p>{', '.join(CLIENTES[:-1])} e {CLIENTES[-1]}.</p>
<p class="sig">Bora fazer acontecer.</p>
</div></section>
{final_cta()}""" + FOOT
write("/sobre/", p, "0.8")

# =====================================================================
# FAQ GERAL
# =====================================================================
all_faq = home_faq + [
    ("Quanto custa trabalhar contigo?", "Depende do serviço. A Lista de Fornecedores tem preço fixo, indicado na <a href=\"/lista-estrategica-de-fornecedores/\">página da lista</a>. O Diagnóstico Alinhavar e o Método FIBRA são por candidatura e o valor é apresentado nesse processo."),
    ("Fazes o conteúdo ou a gestão do Instagram da minha marca?", "Não. Trabalho a estratégia por trás da marca: produto, margem, posicionamento e decisão. A comunicação só resulta quando isso está resolvido."),
    ("Ajudas marcas que ainda não existem?", "Sim, sobretudo na fase de decidir o modelo de negócio e encontrar fornecedores. A <a href=\"/lista-estrategica-de-fornecedores/\">Lista de Fornecedores</a> e o guia <a href=\"/guias/revenda-ou-marca-propria/\">Revenda ou marca própria</a> são um bom ponto de partida."),
    ("Garantes resultados?", "Não prometo resultados garantidos. Garanto critério, estrutura e uma leitura honesta da tua marca. Os resultados dependem das decisões que tomares a partir daí."),
]
c_h, c_s = crumbs([("Perguntas frequentes", "/perguntas-frequentes/")])
f_h, f_s = faq_block(all_faq)
p = head("/perguntas-frequentes/", "Perguntas frequentes · Tânia Silveira", "Respostas diretas sobre os serviços de estratégia para marcas de moda de Tânia Silveira: Diagnóstico Alinhavar, Método FIBRA, Consultoria Tafetá 360 e Lista de Fornecedores.", [c_s, f_s])
p += f"""<section class="page-head"><div class="wrap narrow">{c_h}<span class="eyebrow">Perguntas frequentes</span><h1>Respostas <em>diretas.</em></h1></div></section>
<section style="padding-top:0"><div class="wrap narrow">{f_h}</div></section>{final_cta()}""" + FOOT
write("/perguntas-frequentes/", p, "0.6")

# =====================================================================
# CONTACTO
# =====================================================================
c_h, c_s = crumbs([("Contacto", "/contacto/")])
p = head("/contacto/", "Contacto · Tânia Silveira", "Fala com a Tânia Silveira, estrategista de marcas de moda em Guimarães. Envia uma mensagem ou segue no Instagram e LinkedIn.",
         [c_s, {"@type": "ContactPage", "url": SITE + "/contacto/", "about": {"@id": SITE + "/#negocio"}}])
p += f"""<section class="page-head"><div class="wrap split top">
<div>{c_h}<span class="eyebrow">Contacto</span><h1>Vamos fazer <em>acontecer?</em></h1>
<p class="lead">Envia-me uma mensagem. Respondo pessoalmente.</p>
<p>Se já sabes que queres avançar, vai direto ao <a class="link" href="/diagnostico-alinhavar/">Diagnóstico Alinhavar</a>.</p>
<p><a class="link" href="{LINKS['instagram']}" target="_blank" rel="noopener">Instagram</a> &nbsp;·&nbsp; <a class="link" href="{LINKS['linkedin']}" target="_blank" rel="noopener">LinkedIn</a></p></div>
<form class="form" name="contacto" method="POST" action="/obrigada/" data-netlify="true" netlify-honeypot="empresa">
<input type="hidden" name="form-name" value="contacto">
<p class="hp"><label>Não preencher <input name="empresa"></label></p>
<div><label for="nome">Nome</label><input id="nome" name="nome" required autocomplete="name"></div>
<div><label for="email">Email</label><input id="email" name="email" type="email" required autocomplete="email"></div>
<div><label for="marca">Marca (se já existe)</label><input id="marca" name="marca"></div>
<div><label for="fase">Em que fase estás?</label><select id="fase" name="fase"><option>Tenho a ideia, falta o caminho</option><option>Já vendo, mas fica pouco</option><option>Cresci e virei o gargalo</option><option>Sou uma empresa</option><option>Outra</option></select></div>
<div><label for="msg">Mensagem</label><textarea id="msg" name="mensagem" required></textarea></div>
<p style="font-size:13px;color:var(--muted);margin:0">Ao enviar, aceitas a <a href="/politica-de-privacidade/">política de privacidade</a>.</p>
<div><button class="btn" type="submit">Enviar mensagem</button></div>
</form></div></section>""" + FOOT
write("/contacto/", p, "0.6")

p = head("/obrigada/", "Mensagem enviada · Tânia Silveira", "Obrigada pela tua mensagem.", [], noindex=True)
p += """<section class="page-head final"><div class="wrap"><span class="eyebrow">Mensagem enviada</span><h1>Recebi. <em>Respondo em breve.</em></h1>
<p class="lead">Enquanto esperas, lê um dos guias.</p><div class="btns"><a class="btn" href="/guias/">Ver os guias</a></div></div></section>""" + FOOT
write("/obrigada/", p, None)

# Privacidade
p = head("/politica-de-privacidade/", "Política de privacidade · Tânia Silveira", "Como são tratados os dados pessoais enviados através de taniasilveira.pt.", [])
p += """<section class="page-head"><div class="wrap prose"><span class="eyebrow">Legal</span><h1 style="font-size:clamp(40px,5vw,64px)">Política de <em>privacidade</em></h1>
<p>Esta política explica como são tratados os dados pessoais recolhidos em taniasilveira.pt, nos termos do Regulamento Geral sobre a Proteção de Dados (RGPD).</p>
<h2>Responsável</h2><p>Tânia Silveira, Guimarães, Portugal. Contacto através da <a href="/contacto/">página de contacto</a>.</p>
<h2>Que dados recolho</h2><p>Nome, email, nome da marca e a mensagem que envias no formulário de contacto. Nas candidaturas e compras, os dados pedidos nas plataformas externas usadas para esse fim.</p>
<h2>Para quê</h2><p>Para responder ao teu pedido, analisar candidaturas e prestar os serviços contratados. Não vendo nem cedo os teus dados.</p>
<h2>Quanto tempo</h2><p>Durante o tempo necessário para responder ou prestar o serviço, e pelo prazo exigido por lei para efeitos fiscais.</p>
<h2>Os teus direitos</h2><p>Podes pedir acesso, retificação ou eliminação dos teus dados a qualquer momento. Podes também apresentar reclamação à Comissão Nacional de Proteção de Dados (CNPD).</p>
<h2>Serviços externos</h2><p>O site é alojado num fornecedor externo e usa Google Fonts. As candidaturas, agendamentos e pagamentos são feitos em plataformas de terceiros, com as suas próprias políticas de privacidade.</p>
</div></section>""" + FOOT
write("/politica-de-privacidade/", p, "0.2")

# 404
p = head("/404.html", "Página não encontrada · Tânia Silveira", "Esta página não existe.", [], noindex=True)
p += """<section class="page-head final"><div class="wrap"><span class="eyebrow">Erro 404</span><h1>Esta costura <em>não existe.</em></h1>
<p class="lead">A página que procuras mudou de sítio ou nunca existiu.</p><div class="btns"><a class="btn" href="/">Voltar ao início</a><a class="btn ghost" href="/guias/">Ver os guias</a></div></div></section>""" + FOOT
with open(os.path.join(ROOT, "404.html"), "w", encoding="utf-8") as f:
    f.write(p)

# =====================================================================
# Ficheiros técnicos: sitemap, robots, llms.txt
# =====================================================================
sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(
    f"<url><loc>{SITE}{pth}</loc><lastmod>{HOJE}</lastmod><priority>{pr}</priority></url>\n" for pth, pr in PAGES) + "</urlset>\n"
open(os.path.join(ROOT, "sitemap.xml"), "w").write(sm)

open(os.path.join(ROOT, "robots.txt"), "w").write(f"""# Motores de busca e assistentes de IA são bem-vindos.
User-agent: *
Allow: /
Disallow: /obrigada/

User-agent: GPTBot
Allow: /
User-agent: OAI-SearchBot
Allow: /
User-agent: ChatGPT-User
Allow: /
User-agent: ClaudeBot
Allow: /
User-agent: Claude-SearchBot
Allow: /
User-agent: Claude-User
Allow: /
User-agent: PerplexityBot
Allow: /
User-agent: Google-Extended
Allow: /
User-agent: Applebot-Extended
Allow: /

Sitemap: {SITE}/sitemap.xml
""")

llms = f"""# Tânia Silveira — Estratégia para marcas de moda e negócios têxteis

> Tânia Silveira é estrategista de marcas de moda em Portugal (Guimarães), com {ANOS} anos de experiência na indústria têxtil: chão de fábrica, produção, planeamento, desenvolvimento de produto e gestão comercial. Ajuda marcas de moda a ter estrutura, margem e direção para crescer com previsibilidade. Não faz conteúdo nem design: trabalha produto, preço, margem, coleção, posicionamento e decisão.

Língua: português de Portugal. Atende marcas de todo o país, online e presencial.

## Serviços
- [Diagnóstico Alinhavar]({SITE}/diagnostico-alinhavar/): sessão estratégica de 30 minutos, por candidatura, para identificar o gargalo de uma marca de moda (produto, margem, posicionamento ou decisão).
- [Método FIBRA]({SITE}/metodo-fibra/): acompanhamento estratégico 1:1 de 6 meses para marcas de moda. Pilares: Mentalidade, Produto, Digital. Inclui coleção, lógica de produto, margem, posicionamento e mentalidade de decisão.
- [Consultoria Tafetá 360]({SITE}/consultoria-tafeta-360/): sessão estratégica de 2 horas + seguimento de 1 hora ao fim de um mês, para marcas que já vendem e precisam de afinar produto, margem e estratégia comercial.
- [Consultoria para empresas]({SITE}/empresas/): para fábricas, confeções, empresas têxteis e marcas de moda com equipa. Começa sempre por uma consultoria; a partir dela é apresentado um plano à medida.
- [Calculadora de margem]({SITE}/calculadora-de-margem/): ferramenta gratuita que calcula a margem real de uma peça de roupa, com IVA, descontos, portes, taxas e devoluções.
- [Autodiagnóstico]({SITE}/autodiagnostico/): 9 perguntas que identificam o gargalo de uma marca de moda (produto, margem, posicionamento ou decisão) e o serviço indicado.
- [Lista Estratégica de Fornecedores]({SITE}/lista-estrategica-de-fornecedores/): contactos de fornecedores têxteis em Portugal para revenda e para marca própria. Acesso digital de 6 meses.

## Guias
""" + "".join(f"- [{t}]({SITE}{pth}): {d}\n" for pth, t, d, _ in GUIAS) + f"""
## Sobre
- [Sobre Tânia Silveira]({SITE}/sobre/)
- [Perguntas frequentes]({SITE}/perguntas-frequentes/)
- [Contacto]({SITE}/contacto/)
- Instagram: {LINKS['instagram']}
- LinkedIn: {LINKS['linkedin']}
"""
open(os.path.join(ROOT, "llms.txt"), "w").write(llms)
print("Páginas:", len(PAGES))
