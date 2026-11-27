// POST /.netlify/functions/marcar  (form-urlencoded)
// Confirma que a hora está livre, cria o evento com Meet no Google e envia os emails a partir de contacto@.
const cfg = require('./_agenda.json');
const { ocupado, criarEvento } = require('./_google');
const { isoLisboa } = require('./_lisboa');
const { confirmacaoCliente, avisoTania, ics, enviar } = require('./_email');

exports.handler = async (event) => {
  if (event.httpMethod !== 'POST') return { statusCode: 405, body: '' };
  const f = Object.fromEntries(new URLSearchParams(event.body || ''));
  if (f['bot-field']) return { statusCode: 200, body: 'ok' };
  const ev = cfg.eventos[f.evento];
  const valido = ev && /^\d{4}-\d{2}-\d{2}$/.test(f.data) && /^\d{2}:\d{2}$/.test(f.hora) && f.nome && /^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(f.email || '');
  if (!valido) return { statusCode: 400, body: 'dados em falta' };
  const wd = new Date(f.data + 'T12:00:00Z').getUTCDay() || 7;
  if (!(cfg.horario[wd] || []).includes(f.hora) || cfg.bloqueados.includes(f.data)) return { statusCode: 409, body: 'hora fora do horário' };
  const inicio = isoLisboa(f.data, f.hora), fim = isoLisboa(f.data, f.hora, ev.duracao);
  if (new Date(inicio) < new Date(Date.now() + cfg.antecedencia_horas * 3600e3)) return { statusCode: 409, body: 'antecedência insuficiente' };
  try {
    const busy = await ocupado(inicio, fim);
    if (busy.length) return { statusCode: 409, body: 'hora já ocupada' };
    const desc = `Marcação pelo site\nNome: ${f.nome}\nEmail: ${f.email}\nMarca: ${f.marca || '—'}\nQuer trabalhar: ${f.mensagem || '—'}`;
    const { id, meet } = await criarEvento({ inicio, fim, titulo: `${ev.nome} · ${f.nome}`, descricao: desc });
    const m = { ...f, evento: ev.nome, meet, inicio, fim, uid: id };
    await enviar({ para: f.email, assunto: `Está marcado: ${ev.nome}, ${f.quando}`, html: confirmacaoCliente(m), anexoIcs: ics(m) });
    await enviar({ para: 'contacto@taniasilveira.pt', assunto: `Nova marcação: ${f.nome}, ${f.quando}`, html: avisoTania(m), responderA: f.email });
    return { statusCode: 200, headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ ok: true }) };
  } catch (e) {
    console.error(e);
    return { statusCode: 500, body: 'erro' };
  }
};
