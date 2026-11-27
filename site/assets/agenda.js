/* Agenda Tânia Silveira — escolhe dia, hora e envia o pedido */
(function () {
  var root = document.querySelector('[data-agenda]');
  if (!root) return;
  var CFG = JSON.parse(document.getElementById('agenda-cfg').textContent);
  var EV = CFG.eventos[root.dataset.agenda];
  var API = root.dataset.api || '';            // '/.netlify/functions' quando o Google estiver ligado
  var MESES = ['janeiro','fevereiro','março','abril','maio','junho','julho','agosto','setembro','outubro','novembro','dezembro'];
  var DIAS = ['dom','seg','ter','qua','qui','sex','sáb'];
  var DIAS_L = ['domingo','segunda-feira','terça-feira','quarta-feira','quinta-feira','sexta-feira','sábado'];
  var hoje = new Date(); hoje.setHours(0,0,0,0);
  var limite = new Date(hoje); limite.setDate(limite.getDate() + CFG.dias_a_mostrar);
  var minimo = new Date(Date.now() + CFG.antecedencia_horas * 3600e3);
  var view = new Date(hoje.getFullYear(), hoje.getMonth(), 1);
  var escolha = { dia: null, hora: null };
  var ocupados = {}; // 'YYYY-MM-DD' -> ['10:00']

  function iso(d) { return d.getFullYear() + '-' + String(d.getMonth()+1).padStart(2,'0') + '-' + String(d.getDate()).padStart(2,'0'); }
  function slots(d) {
    if (d < hoje || d > limite || CFG.bloqueados.indexOf(iso(d)) > -1) return [];
    var wd = d.getDay() === 0 ? 7 : d.getDay();
    return (CFG.horario[wd] || []).filter(function (h) {
      var p = h.split(':'); var t = new Date(d); t.setHours(+p[0], +p[1], 0, 0);
      return t >= minimo && (ocupados[iso(d)] || []).indexOf(h) < 0;
    });
  }
  var $ = function (s) { return root.querySelector(s); };
  var steps = root.querySelectorAll('.bk-step');
  function go(n) { steps.forEach(function (s, i) { s.hidden = i !== n; }); root.querySelectorAll('.bk-prog li').forEach(function (li, i) { li.classList.toggle('on', i <= n); }); }

  function carregarOcupados() {
    if (!API) return Promise.resolve();
    var de = iso(new Date(view.getFullYear(), view.getMonth(), 1)), ate = iso(new Date(view.getFullYear(), view.getMonth()+1, 0));
    return fetch(API + '/disponibilidade?evento=' + root.dataset.agenda + '&de=' + de + '&ate=' + ate)
      .then(function (r) { return r.ok ? r.json() : {}; }).then(function (j) { Object.assign(ocupados, j.ocupados || {}); }).catch(function () {});
  }
  function cal() {
    $('.bk-mes').textContent = MESES[view.getMonth()] + ' ' + view.getFullYear();
    var g = $('.bk-grid'); g.innerHTML = DIAS.slice(1).concat(DIAS[0]).map(function (d) { return '<span class="bk-dow">' + d + '</span>'; }).join('');
    var first = (view.getDay() + 6) % 7, n = new Date(view.getFullYear(), view.getMonth()+1, 0).getDate();
    for (var i = 0; i < first; i++) g.insertAdjacentHTML('beforeend', '<span></span>');
    for (var d = 1; d <= n; d++) {
      var dt = new Date(view.getFullYear(), view.getMonth(), d), ok = slots(dt).length > 0, sel = escolha.dia && iso(escolha.dia) === iso(dt);
      g.insertAdjacentHTML('beforeend', '<button type="button" class="bk-d' + (ok ? ' ok' : '') + (sel ? ' sel' : '') + '"' + (ok ? '' : ' disabled') + ' data-d="' + iso(dt) + '" aria-label="' + d + ' de ' + MESES[view.getMonth()] + (ok ? ', com horas livres' : ', sem horas livres') + '">' + d + '</button>');
    }
    $('.bk-prev').disabled = view <= new Date(hoje.getFullYear(), hoje.getMonth(), 1);
    $('.bk-next').disabled = new Date(view.getFullYear(), view.getMonth()+1, 1) > limite;
  }
  function horas() {
    var d = escolha.dia, hs = slots(d);
    $('.bk-dia').textContent = DIAS_L[d.getDay()] + ', ' + d.getDate() + ' de ' + MESES[d.getMonth()];
    $('.bk-hs').innerHTML = hs.length ? hs.map(function (h) { return '<button type="button" class="bk-h" data-h="' + h + '">' + h + '</button>'; }).join('') : '<p class="bk-none">Sem horas livres neste dia.</p>';
  }
  root.addEventListener('click', function (ev) {
    var b = ev.target.closest('button'); if (!b) return;
    if (b.classList.contains('bk-prev')) { view.setMonth(view.getMonth()-1); carregarOcupados().then(cal); }
    else if (b.classList.contains('bk-next')) { view.setMonth(view.getMonth()+1); carregarOcupados().then(cal); }
    else if (b.dataset.d) { var p = b.dataset.d.split('-'); escolha.dia = new Date(+p[0], +p[1]-1, +p[2]); cal(); horas(); go(1); }
    else if (b.dataset.h) { escolha.hora = b.dataset.h; resumo(); go(2); }
    else if (b.dataset.back) { go(+b.dataset.back); }
  });
  function resumo() {
    var d = escolha.dia, txt = DIAS_L[d.getDay()] + ', ' + d.getDate() + ' de ' + MESES[d.getMonth()] + ' · ' + escolha.hora;
    root.querySelectorAll('.bk-res').forEach(function (e) { e.textContent = txt; });
    var f = $('form'); f.elements.data.value = iso(d); f.elements.hora.value = escolha.hora; f.elements.quando.value = txt;
  }
  $('form').addEventListener('submit', function (ev) {
    ev.preventDefault();
    var f = ev.target, btn = f.querySelector('button[type=submit]'), msg = f.querySelector('.bk-msg');
    btn.disabled = true; msg.textContent = '';
    var body = new URLSearchParams(new FormData(f)).toString();
    var url = API ? API + '/marcar' : '/';
    fetch(url, { method: 'POST', headers: { 'Content-Type': 'application/x-www-form-urlencoded' }, body: body })
      .then(function (r) { if (!r.ok) throw 0; go(3); })
      .catch(function () { btn.disabled = false; msg.textContent = 'Não foi possível enviar agora. Tenta de novo ou escreve para ' + root.dataset.email + '.'; });
  });
  carregarOcupados().then(function () {
    // abre no primeiro mês com horas livres
    for (var k = 0; k < 3; k++) { var tem = false; var n = new Date(view.getFullYear(), view.getMonth()+1, 0).getDate();
      for (var d = 1; d <= n; d++) if (slots(new Date(view.getFullYear(), view.getMonth(), d)).length) { tem = true; break; }
      if (tem) break; view.setMonth(view.getMonth()+1); }
    cal(); go(0);
  });
})();
