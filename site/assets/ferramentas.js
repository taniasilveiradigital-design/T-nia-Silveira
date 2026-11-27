/* Ferramentas interativas: calculadora de margem, mini-calculadora, autodiagnóstico, linha que cose */
(function () {
  var eur = new Intl.NumberFormat('pt-PT', { style: 'currency', currency: 'EUR' });
  function pct(n) { return (n * 100).toFixed(1).replace('.', ',') + '%'; }
  function num(el) { var n = parseFloat(String(el.value).replace(',', '.')); return isFinite(n) && n >= 0 ? n : 0; }
  function $(s, r) { return (r || document).querySelector(s); }
  function $$(s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); }
  var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;

  function verdict(m) {
    if (m < 0.3) return { k: 'mau', label: 'Estás a pagar para vender.', text: 'Com esta margem, cada venda mal cobre a operação. Mais vendas não resolvem: o problema está no preço ou no custo.' };
    if (m < 0.5) return { k: 'curto', label: 'Margem curta.', text: 'Sobra pouco para marketing, stock parado e imprevistos. Qualquer desconto extra come o lucro.' };
    if (m < 0.6) return { k: 'ok', label: 'Margem razoável.', text: 'Há base, mas pouca folga. Afinar custo ou preço dá-te espaço para crescer sem aperto.' };
    return { k: 'bom', label: 'Margem saudável.', text: 'Há espaço para investir na marca. Garante que se mantém quando entram saldos e devoluções.' };
  }

  /* ---------- Calculadora completa ---------- */
  var calc = $('#calc');
  if (calc) {
    var TARGET = 0.6;
    var f = {};
    $$('input[data-k]', calc).forEach(function (i) { f[i.dataset.k] = i; });
    var out = {
      pct: $('#r-pct'), eur: $('#r-eur'), recebes: $('#r-recebes'), custa: $('#r-custa'),
      mult: $('#r-mult'), alvo: $('#r-alvo'), verdict: $('#r-verdict'), bars: $('#r-bars'), gauge: $('#r-gauge')
    };
    function run() {
      var v = {}; Object.keys(f).forEach(function (k) { v[k] = num(f[k]); });
      var pvpSemIva = v.pvp / (1 + v.iva / 100);
      var efetivo = pvpSemIva * (1 - v.desconto / 100);
      var desenv = v.unidades > 0 ? v.amostras / v.unidades : 0;
      var peca = v.producao + v.aviamentos + desenv;
      var taxasPct = (v.taxas + v.comissoes) / 100;
      var custoTaxas = efetivo * taxasPct;
      var custoDev = (v.devolucoes / 100) * v.portes * 2; // cada devolução paga portes de ida e volta
      var fixo = peca + v.portes + custoDev;
      var total = fixo + custoTaxas;
      var margem = efetivo - total;
      var mPct = efetivo > 0 ? margem / efetivo : 0;
      var mult = v.producao + v.aviamentos > 0 ? v.pvp / (v.producao + v.aviamentos) : 0;
      var denom = 1 - taxasPct - TARGET;
      var alvo = denom > 0 ? (fixo / denom / (1 - v.desconto / 100)) * (1 + v.iva / 100) : NaN;
      out.pct.textContent = pct(mPct);
      out.eur.textContent = eur.format(margem) + ' por peça vendida';
      out.recebes.textContent = eur.format(efetivo);
      out.custa.textContent = eur.format(total);
      out.mult.textContent = mult.toFixed(1).replace('.', ',') + '×';
      out.alvo.textContent = isFinite(alvo) ? eur.format(alvo) : '—';
      var vd = verdict(mPct);
      out.verdict.className = 'verdict v-' + vd.k;
      out.verdict.innerHTML = '<b>' + vd.label + '</b><span>' + vd.text + '</span>';
      out.gauge.style.setProperty('--m', Math.max(0, Math.min(1, mPct)));
      var parts = [
        ['Peça (produção + aviamentos)', v.producao + v.aviamentos],
        ['Desenvolvimento por peça', desenv],
        ['Portes', v.portes],
        ['Devoluções', custoDev],
        ['Taxas e comissões', custoTaxas]
      ];
      out.bars.innerHTML = parts.map(function (p) {
        var w = efetivo > 0 ? Math.min(100, p[1] / efetivo * 100) : 0;
        return '<li><div class="bl"><span>' + p[0] + '</span><b>' + eur.format(p[1]) + '</b></div><div class="bar"><i style="width:' + w + '%"></i></div></li>';
      }).join('');
    }
    calc.addEventListener('input', run);
    run();
  }

  /* ---------- Mini-calculadora (página inicial) ---------- */
  var mini = $('#mini-calc');
  if (mini) {
    var c = $('#m-custo', mini), p = $('#m-pvp', mini), d = $('#m-desc', mini), dv = $('#m-desc-v', mini);
    function runMini() {
      var semIva = num(p) / 1.23 * (1 - num(d) / 100);
      var m = semIva > 0 ? (semIva - num(c)) / semIva : 0;
      dv.textContent = num(d) + '%';
      $('#m-pct', mini).textContent = pct(m);
      $('#m-eur', mini).textContent = eur.format(semIva - num(c)) + ' por peça, antes de portes, taxas e devoluções';
      var vd = verdict(m);
      var vEl = $('#m-verdict', mini); vEl.className = 'verdict v-' + vd.k; vEl.innerHTML = '<b>' + vd.label + '</b>';
      mini.style.setProperty('--m', Math.max(0, Math.min(1, m)));
    }
    mini.addEventListener('input', runMini);
    runMini();
  }

  /* ---------- Autodiagnóstico ---------- */
  var quiz = $('#quiz');
  if (quiz) {
    var Q = JSON.parse($('#quiz-data').textContent);
    var stage = null, answers = [], step = 0;
    var total = Q.statements.length + 1;
    var box = $('#quiz-box', quiz), bar = $('#quiz-bar', quiz), count = $('#quiz-count', quiz), back = $('#quiz-back', quiz);
    var resultEl = $('#quiz-result');

    function render() {
      bar.style.width = (step / total * 100) + '%';
      count.textContent = 'Pergunta ' + (step + 1) + ' de ' + total;
      back.hidden = step === 0;
      var html;
      if (step === 0) {
        html = '<p class="q">' + Q.stage.text + '</p><div class="opts col">' + Q.stage.options.map(function (o) {
          return '<button type="button" class="opt' + (stage === o.value ? ' on' : '') + '" data-stage="' + o.value + '">' + o.label + '</button>';
        }).join('') + '</div>';
      } else {
        var s = Q.statements[step - 1];
        html = '<p class="q">“' + s.text + '”</p><p class="qh">Isto acontece na tua marca?</p><div class="opts">' + Q.answers.map(function (o) {
          return '<button type="button" class="opt' + (answers[step - 1] === o.value ? ' on' : '') + '" data-v="' + o.value + '">' + o.label + '</button>';
        }).join('') + '</div>';
      }
      box.classList.remove('in'); box.innerHTML = html;
      requestAnimationFrame(function () { box.classList.add('in'); });
    }
    box.addEventListener('click', function (ev) {
      var b = ev.target.closest('button'); if (!b) return;
      if (b.dataset.stage) { stage = b.dataset.stage; step = 1; }
      else { answers[step - 1] = +b.dataset.v; step++; }
      if (step > Q.statements.length) return finish();
      render();
    });
    back.addEventListener('click', function () { if (step > 0) { step--; render(); } });

    function compute() {
      var sc = { produto: 0, margem: 0, posicionamento: 0, decisao: 0 };
      Q.statements.forEach(function (s, i) { sc[s.area] += answers[i] || 0; });
      var tot = 0, max = 0; Object.keys(sc).forEach(function (k) { tot += sc[k]; max = Math.max(max, sc[k]); });
      var main = (tot <= 3 || max <= 1) ? 'solida' : ['decisao', 'produto', 'margem', 'posicionamento'].filter(function (a) { return sc[a] === max; })[0];
      var service = (stage !== 'inicio' && (main === 'solida' || (stage === 'escala' && tot <= 8))) ? 'tafeta' : 'fibra';
      return { sc: sc, main: main, service: service };
    }
    function finish() {
      var r = compute(), res = Q.results[r.main], svc = Q.services[r.service];
      quiz.hidden = true; resultEl.hidden = false;
      $('#qr-title').textContent = res.title;
      $('#qr-text').textContent = res.text;
      $('#qr-bars').innerHTML = Object.keys(r.sc).map(function (a) {
        return '<li><div class="bl"><span>' + Q.labels[a] + '</span><b>' + r.sc[a] + '/4</b></div><div class="bar"><i class="' + (a === r.main ? 'main' : '') + '" data-w="' + (r.sc[a] / 4 * 100) + '"></i></div></li>';
      }).join('');
      $('#qr-actions').innerHTML = res.actions.map(function (a) { return '<li>' + a + '</li>'; }).join('');
      $('#qr-margem').hidden = r.main !== 'margem';
      $('#qr-svc').textContent = svc.name; $('#qr-why').textContent = svc.why;
      var l = $('#qr-link'); l.href = svc.href; l.textContent = 'Ver ' + svc.name;
      var form = $('#qr-form');
      form.elements.fase.value = stage; form.elements.gargalo.value = r.main;
      form.elements.servico_recomendado.value = svc.name;
      form.elements.pontuacoes.value = Object.keys(r.sc).map(function (a) { return Q.labels[a] + ': ' + r.sc[a] + '/4'; }).join(' | ');
      resultEl.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth', block: 'start' });
      setTimeout(function () { $$('#qr-bars i').forEach(function (i) { i.style.width = i.dataset.w + '%'; }); }, 250);
    }
    $('#qr-restart').addEventListener('click', function () {
      stage = null; answers = []; step = 0; resultEl.hidden = true; quiz.hidden = false; render();
      quiz.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth', block: 'start' });
    });
    var qf = $('#qr-form');
    qf.addEventListener('submit', function (ev) {
      ev.preventDefault();
      var msg = $('#qr-msg');
      var body = new URLSearchParams(new FormData(qf)).toString();
      fetch('/', { method: 'POST', headers: { 'Content-Type': 'application/x-www-form-urlencoded' }, body: body })
        .then(function (r) { if (!r.ok) throw 0; location.href = '/obrigada/'; })
        .catch(function () { msg.textContent = 'Não foi possível enviar agora. Tenta de novo ou usa a página de contacto.'; });
    });
    render();
  }

  /* ---------- A linha que cose ---------- */
  var stitches = $$('.sew');
  var progress = $('#sew-progress');
  if (stitches.length || progress) {
    var tick = function () {
      var vh = innerHeight;
      stitches.forEach(function (s) {
        var r = s.getBoundingClientRect();
        var p = reduce ? 1 : Math.max(0, Math.min(1, (vh * 0.95 - r.top) / (vh * 0.6 + r.height)));
        s.style.setProperty('--p', p);
      });
      if (progress) {
        var h = document.documentElement.scrollHeight - vh;
        progress.style.setProperty('--p', h > 0 ? scrollY / h : 0);
      }
    };
    var ticking = false;
    addEventListener('scroll', function () { if (!ticking) { ticking = true; requestAnimationFrame(function () { tick(); ticking = false; }); } }, { passive: true });
    addEventListener('resize', tick);
    tick();
  }
})();

/* ---------- Guia grátis + vídeos ---------- */
(function () {
  document.querySelectorAll('form[data-guia]').forEach(function (f) {
    f.addEventListener('submit', function (ev) {
      ev.preventDefault();
      var ok = f.querySelector('.gok'), btn = f.querySelector('button');
      btn.disabled = true;
      fetch('/', { method: 'POST', headers: { 'Content-Type': 'application/x-www-form-urlencoded' }, body: new URLSearchParams(new FormData(f)).toString() })
        .catch(function () {})
        .then(function () { ok.hidden = false; btn.hidden = true; });
    });
  });
  if (window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches) {
    document.querySelectorAll('video[autoplay]').forEach(function (v) { v.removeAttribute('autoplay'); v.pause(); v.controls = true; });
  }
})();

/* ---------- Diagrama FIBRA + barra fixa ---------- */
(function () {
  var items = document.querySelectorAll('.vi'), rings = document.querySelectorAll('.vc');
  function set(k) {
    items.forEach(function (i) { i.classList.toggle('on', i.dataset.k === k); i.setAttribute('aria-pressed', i.dataset.k === k); });
    rings.forEach(function (r) { r.classList.toggle('on', r.dataset.k === k); });
  }
  if (items.length) {
    items.forEach(function (i) { i.addEventListener('click', function () { set(i.dataset.k); }); i.addEventListener('mouseenter', function () { set(i.dataset.k); }); });
    rings.forEach(function (r) { r.addEventListener('click', function () { set(r.dataset.k); }); });
    set('mentalidade');
  }
  var bar = document.getElementById('stickybar');
  if (bar) {
    var show = function () { var on = scrollY > innerHeight * 0.9; bar.hidden = !on; document.body.classList.toggle('has-bar', on); };
    addEventListener('scroll', show, { passive: true }); show();
  }
})();

/* ---------- Quatro caminhos ---------- */
(function () {
  var ps = document.querySelectorAll('.jp');
  if (!ps.length) return;
  function open(p) { ps.forEach(function (x) { var on = x === p; x.classList.toggle('on', on); x.setAttribute('aria-expanded', on); }); }
  ps.forEach(function (p) {
    p.addEventListener('click', function (ev) { if (!p.classList.contains('on')) { ev.preventDefault(); open(p); } });
    p.addEventListener('keydown', function (ev) { if ((ev.key === 'Enter' || ev.key === ' ') && !p.classList.contains('on')) { ev.preventDefault(); open(p); } });
    if (matchMedia('(hover:hover)').matches) p.addEventListener('mouseenter', function () { open(p); });
  });
})();

/* ---------- Agenda Cal.com (só quando há link configurado) ---------- */
(function () {
  var els = document.querySelectorAll('.ag-cal[data-cal]');
  if (!els.length) return;
  (function (C, A, L) { var p = function (a, ar) { a.q.push(ar); }; var d = C.document; C.Cal = C.Cal || function () { var cal = C.Cal; var ar = arguments; if (!cal.loaded) { cal.ns = {}; cal.q = cal.q || []; d.head.appendChild(d.createElement('script')).src = A; cal.loaded = true; } if (ar[0] === L) { var api = function () { p(api, arguments); }; var namespace = ar[1]; api.q = api.q || []; if (typeof namespace === 'string') { cal.ns[namespace] = cal.ns[namespace] || api; p(cal.ns[namespace], ar); p(cal, ['initNamespace', namespace]); } else p(cal, ar); return; } p(cal, ar); }; })(window, 'https://app.cal.com/embed/embed.js', 'init');
  els.forEach(function (el, i) {
    var ns = 'ts' + i;
    Cal('init', ns, { origin: 'https://cal.com' });
    Cal.ns[ns]('inline', { elementOrSelector: '#' + el.id, calLink: el.dataset.cal, config: { layout: 'month_view', theme: 'light' } });
    Cal.ns[ns]('ui', { theme: 'light', hideEventTypeDetails: true, layout: 'month_view', cssVarsPerTheme: { light: { 'cal-brand': '#5c3b2e', 'cal-bg': '#faf6f1', 'cal-bg-emphasis': '#f3ebe2', 'cal-text': '#33221b', 'cal-border': '#e2d4c7' } } });
  });
})();
