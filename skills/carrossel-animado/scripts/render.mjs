// Fotografa cada slide frame a frame, FORA DE ORDEM de propósito: prova que tudo depende só de t.
// Uso: node render.mjs            (todos os slides, todos os frames)
//      node render.mjs --static   (só o frame 0 de cada slide, para rever o desenho)
//      node render.mjs --slide 3  (um só slide)
//      node render.mjs --at 2,3.5 (frames nesses segundos em static/em/, sem render completo)
import fs from 'node:fs';
import { createRequire } from 'node:module';
import path from 'node:path';
import os from 'node:os';
import { pathToFileURL } from 'node:url';

const FPS = 30;
const args = process.argv.slice(2);
const atIdx = args.indexOf('--at');
const atTimes = atIdx >= 0 ? args[atIdx + 1].split(',').map(Number) : null;
const onlyStatic = args.includes('--static') || !!atTimes;
const oneIdx = args.indexOf('--slide');
// O motor e o navegador vivem numa só pasta, instalados uma vez por verificar.py.
const CASA = process.env.CARROSSEL_CASA || path.join(os.homedir(), '.carrossel-animado');
const browsers = path.join(CASA, 'browser');
const NOMES = process.platform === 'win32' ? ['chrome-headless-shell.exe', 'headless_shell.exe'] : ['chrome-headless-shell', 'headless_shell'];
const exe = fs.existsSync(browsers) ? fs.readdirSync(browsers, { recursive: true }).map(String).filter((f) => NOMES.includes(path.basename(f))).map((f) => path.join(browsers, f)).sort().pop() : null;
if (!exe) { console.error('O computador ainda não está preparado. Corre verificar.py.'); process.exit(1); }
const { chromium } = createRequire(path.join(CASA, 'motor', 'package.json'))('playwright-core');
const root = pathToFileURL(path.resolve('index.html')).href;

const browser = await chromium.launch({ executablePath: exe, headless: true });
const ctx = await browser.newContext({ viewport: { width: 1080, height: 1350 }, deviceScaleFactor: 1 });
fs.mkdirSync('static', { recursive: true });
// A folha de tempos só mostra o último pedido: frames antigos enganam.
if (oneIdx < 0) fs.rmSync('static/em', { recursive: true, force: true });
const cues = fs.existsSync('duracoes.json') ? JSON.parse(fs.readFileSync('duracoes.json', 'utf8')) : {};

async function openSlide(s) {
  const page = await ctx.newPage();
  page.on('pageerror', (e) => { console.error(`slide ${s}:`, e.message); process.exitCode = 1; });
  await page.goto(`${root}?s=${s}`);
  // Carrega todas as fontes, também as que só o canvas usa: o DOM não as pede.
  await page.evaluate(() => Promise.allSettled([...document.fonts].map((f) => f.load())));
  // Uma fonte que falha cai para Times sem dar erro. Melhor parar já.
  const bad = await page.evaluate(() => [...document.fonts].filter((f) => f.status === 'error').map((f) => `${f.family} ${f.weight} ${f.style}`));
  if (bad.length) { console.error(`Fontes que não carregaram: ${bad.join(', ')}. O caminho da pasta pode ser demasiado longo.`); process.exit(1); }
  // Uma imagem em falta deixa um slide com ar de completo, sem qualquer erro.
  await page.waitForLoadState('load');
  const semImg = await page.evaluate(() => [...document.images].filter((i) => !i.complete || !i.naturalWidth).map((i) => i.getAttribute('src')));
  if (semImg.length) { console.error(`Slide ${s}: imagens que não carregaram: ${semImg.join(', ')}`); process.exit(1); }
  return page;
}

async function renderSlide(s) {
  const page = await openSlide(s);
  const dur = await page.evaluate(() => window.DUR);
  cues[s] = { dur };
  const tag = String(s).padStart(2, '0');
  await page.evaluate(() => window.seek(0));
  await page.screenshot({ path: `static/s${tag}.png` });
  // Abaixo de 28 px lê-se mal no telemóvel. É aviso e não erro: cabe a quem revê decidir.
  const small = await page.evaluate(() => {
    const out = new Set();
    const walk = document.createTreeWalker(document.getElementById('content'), NodeFilter.SHOW_TEXT);
    while (walk.nextNode()) {
      const txt = walk.currentNode.textContent.trim();
      if (txt && parseFloat(getComputedStyle(walk.currentNode.parentElement).fontSize) < 28) out.add(txt.slice(0, 40));
    }
    return [...out];
  });
  // Com fontes da aluna, o texto pode sair do slide. A palavra atrás da cabeça pode: é de propósito.
  const fora = await page.evaluate(() => {
    const out = new Set();
    const walk = document.createTreeWalker(document.getElementById('content'), NodeFilter.SHOW_TEXT);
    while (walk.nextNode()) {
      if (walk.currentNode.parentElement.closest('.tras') || !walk.currentNode.textContent.trim()) continue;
      const range = document.createRange();
      range.selectNodeContents(walk.currentNode);
      for (const b of range.getClientRects()) {
        if (b.width && (b.left < 0 || b.right > 1080 || b.bottom > 1350)) out.add(walk.currentNode.textContent.trim().slice(0, 30));
      }
    }
    return [...out];
  });
  if (fora.length) console.log(`AVISO slide ${s}: texto a sair do slide: ${fora.join(' | ')}`);
  // Texto nos cantos à direita fica por baixo do contador e do ícone de som do Instagram.
  cues[s].cantos = await page.evaluate(() => {
    const out = new Set();
    const walk = document.createTreeWalker(document.getElementById('content'), NodeFilter.SHOW_TEXT);
    while (walk.nextNode()) {
      const range = document.createRange();
      range.selectNodeContents(walk.currentNode);
      for (const b of range.getClientRects()) {
        if (b.width && b.right > 940 && (b.top < 120 || b.bottom > 1240)) out.add(walk.currentNode.textContent.trim().slice(0, 30));
      }
    }
    return [...out];
  });
  if (cues[s].cantos.length) console.log(`AVISO slide ${s}: texto nos cantos: ${cues[s].cantos.join(' | ')}`);
  if (small.length) console.log(`AVISO slide ${s}: texto abaixo de 28 px: ${small.join(' | ')}`);
  if (atTimes) {
    fs.mkdirSync('static/em', { recursive: true });
    for (const f of fs.readdirSync('static/em')) if (f.startsWith(`s${tag}_`)) fs.rmSync(`static/em/${f}`);
    for (const t of atTimes) {
      await page.evaluate((x) => window.seek(x), t);
      await page.screenshot({ path: `static/em/s${tag}_${t.toFixed(2)}.png` });
    }
  }
  if (!onlyStatic) {
    const dir = `frames/s${tag}`;
    fs.rmSync(dir, { recursive: true, force: true });
    fs.mkdirSync(dir, { recursive: true });
    const n = Math.round(dur * FPS);
    const order = Array.from({ length: n }, (_, i) => i);
    let x = 12345 + s;
    for (let i = n - 1; i > 0; i--) { x = (x * 16807) % 2147483647; const j = x % (i + 1); [order[i], order[j]] = [order[j], order[i]]; }
    let feitos = 0;
    for (const f of order) {
      await page.evaluate((t) => window.seek(t), f / FPS);
      await page.screenshot({ path: `${dir}/${String(f).padStart(3, '0')}.png` });
      if (++feitos % 60 === 0) console.log(`slide ${s}: ${feitos}/${n}`);
    }
    console.log(`slide ${s}: ${n} frames`);
  }
  await page.close();
}

const probe = await openSlide(1);
const TOTAL = await probe.evaluate(() => window.TOTAL);
await probe.close();
for (const k of Object.keys(cues)) if (+k > TOTAL) delete cues[k];
// Se o carrossel encolheu, tira o que sobrou dos slides que já não existem.
for (const f of fs.readdirSync('static')) { const m = f.match(/^s(\d+)\.png$/); if (m && +m[1] > TOTAL) fs.rmSync(`static/${f}`); }
if (fs.existsSync('frames')) for (const f of fs.readdirSync('frames')) { const m = f.match(/^s(\d+)$/); if (m && +m[1] > TOTAL) fs.rmSync(`frames/${f}`, { recursive: true }); }
const queue = oneIdx >= 0 ? [+args[oneIdx + 1]] : Array.from({ length: TOTAL }, (_, i) => i + 1);
const workers = Math.min(4, Math.max(1, os.cpus().length - 2));
await Promise.all(Array.from({ length: workers }, async () => { while (queue.length) await renderSlide(queue.shift()); }));
fs.writeFileSync('duracoes.json', JSON.stringify(cues, null, 1));
await browser.close();
