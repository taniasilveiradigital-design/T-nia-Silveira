// Motor. Não se mexe em cada carrossel: o carrossel vive em slides.js. Tudo é função de t.
const T = 8;
const COR = MARCA.cores;
const stage = document.getElementById('stage');
const content = document.getElementById('content');
const clamp = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
const outCubic = (x) => 1 - Math.pow(1 - x, 3);
const inOut = (x) => (x < 0.5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2);
const inCubic = (x) => x * x * x;
const wave = (t, k, ph = 0) => Math.sin((2 * Math.PI * k * t) / T + ph);
const salto = (t, at, d = 0.25) => clamp(Math.abs(t - at) / d);

function el(cls, css = {}, html = '', pai = content, tag = 'div') {
  const e = document.createElement(tag);
  if (cls) e.className = cls;
  Object.assign(e.style, css);
  e.innerHTML = html;
  pai.appendChild(e);
  return e;
}
const px = (n) => n + 'px';

// Fotografia, camada de trás (fica entre o fundo e a pessoa) e recorte, sempre juntos.
function cena(n, { x = -70, y = -205, w = 1220 } = {}) {
  const c = el('cena');
  const css = { left: px(x), top: px(y), width: px(w), height: px((w * 16) / 9) };
  const f = el('', css, '', c, 'img'); f.src = `fotos/f${n}.jpg`;
  el('cima', {}, '', c);
  const tras = el('tras', {}, '', c);
  const p = el('', css, '', c, 'img'); p.src = `fotos/f${n}.png`;
  return { c, tras };
}
const zoom = (c, t) => { c.style.transform = `scale(${1 + 0.022 * (0.5 - 0.5 * Math.cos((2 * Math.PI * t) / T))})`; };
const scrim = (de, ate, forte = 0.95) => el('scrim', { background: `linear-gradient(0deg,rgba(var(--escuro-rgb),${forte}),rgba(var(--escuro-rgb),${forte * 0.72}) ${de}%,rgba(var(--escuro-rgb),0) ${ate}%)` });
const handle = () => el('handle', {}, MARCA.handle);

// Ajudas de motion.
const mod = (x, m) => ((x % m) + m) % m;
// Ressalto: de 0 a 1, passa um pouco por cima e assenta.
const ressalto = (x) => { const k = clamp(x); return 1 - Math.exp(-6 * k) * Math.cos(11 * k); };
// Números aleatórios sempre iguais: const r = semente(7); r() dá um valor entre 0 e 1.
function semente(n) { let v = n; return () => (v = (v * 16807) % 2147483647) / 2147483647; }
// Recorte sem a foto de fundo, com a mesma cor de cena(). Devolve o elemento img.
function recorte(n, { x = 0, y = 0, w = 1080, pai = content } = {}) {
  const r = el('', { position: 'absolute', left: px(x), top: px(y), width: px(w), filter: 'var(--foto)' }, '', pai, 'img');
  r.src = `fotos/f${n}.png`;
  return r;
}

// Tela de desenho a toda a área, para motion. Devolve o contexto 2D. Limpa-a tu em cada seek.
function tela(pai = content) {
  const c = el('', { position: 'absolute', left: 0, top: 0 }, '', pai, 'canvas');
  c.width = 1080; c.height = 1350;
  return c.getContext('2d');
}

// Placa em perspetiva. (x, y) é o vértice de cima. Cria primeiro as de baixo: a última fica por cima.
function placa(x, y, html, { cor = COR.escuro2, lado = COR.destaque, fundo = COR.destaquePapel, d = 26, pai = content } = {}) {
  const w = el('placa', { left: px(x), top: px(y) }, '', pai);
  const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
  svg.setAttribute('width', '450'); svg.setAttribute('height', String(225 + d));
  svg.innerHTML = `<polygon fill="${lado}" points="0,112.5 225,225 225,${225 + d} 0,${112.5 + d}"/><polygon fill="${fundo}" points="225,225 450,112.5 450,${112.5 + d} 225,${225 + d}"/>`;
  w.appendChild(svg);
  w.face = el('face', { background: cor }, html, w);
  return w;
}

// A luz atravessa cada costura: sai de um slide à mesma altura a que entra no seguinte.
function luzes(id, total, seam) {
  const out = [];
  const cria = (css) => {
    const l = el('luz', css);
    // Fica por cima da foto e por baixo do texto, para nunca o apagar.
    const fotos = content.querySelectorAll(':scope > .cena');
    const depois = fotos.length ? fotos[fotos.length - 1].nextSibling : content.firstChild;
    content.insertBefore(l, depois);
    out.push(l);
  };
  // Em seam, null deixa essa costura sem luz.
  if (id > 1 && seam[id - 2] != null) cria({ left: '-320px', top: px(seam[id - 2] - 560) });
  if (id < total && seam[id - 1] != null) cria({ left: '760px', top: px(seam[id - 1] - 560) });
  return (t) => out.forEach((l) => { l.style.opacity = 0.62 + 0.22 * wave(t, 1); });
}

// Última linha de slides.js: arrancar(SLIDES, { seam: [...] }).
function arrancar(SLIDES, { seam = [] } = {}) {
  const id = +new URLSearchParams(location.search).get('s') || 1;
  const total = Object.keys(SLIDES).length;
  const slide = SLIDES[id]();
  if (slide.theme) stage.classList.add(slide.theme);
  const luz = luzes(id, total, seam);
  const grao = el('', {}, '', stage, 'img'); grao.id = 'grao'; grao.src = 'fotos/grao.png';
  window.TOTAL = total;
  window.DUR = T;
  window.seek = (t) => { slide.seek(t); luz(t); };
  window.seek(0);
}
