// GET /.netlify/functions/disponibilidade?evento=tafeta&de=2026-12-01&ate=2026-12-31
// Devolve as horas do horário que já estão ocupadas no Google: { ocupados: { "2026-12-02": ["10:00"] } }
const cfg = require('./_agenda.json');
const { ocupado } = require('./_google');
const { isoLisboa } = require('./_lisboa');

exports.handler = async (event) => {
  const q = event.queryStringParameters || {};
  const ev = cfg.eventos[q.evento];
  if (!ev || !/^\d{4}-\d{2}-\d{2}$/.test(q.de || '') || !/^\d{4}-\d{2}-\d{2}$/.test(q.ate || '')) return { statusCode: 400, body: '{}' };
  try {
    const busy = await ocupado(isoLisboa(q.de, '00:00'), isoLisboa(q.ate, '23:59'));
    const out = {};
    for (let d = new Date(q.de + 'T12:00:00Z'); d <= new Date(q.ate + 'T12:00:00Z'); d.setUTCDate(d.getUTCDate() + 1)) {
      const dia = d.toISOString().slice(0, 10); const wd = d.getUTCDay() || 7;
      for (const h of cfg.horario[wd] || []) {
        const a = new Date(isoLisboa(dia, h)), b = new Date(isoLisboa(dia, h, ev.duracao));
        if (busy.some(x => new Date(x.start) < b && new Date(x.end) > a)) (out[dia] = out[dia] || []).push(h);
      }
    }
    return { statusCode: 200, headers: { 'Content-Type': 'application/json', 'Cache-Control': 'no-store' }, body: JSON.stringify({ ocupados: out }) };
  } catch (e) {
    console.error(e);
    return { statusCode: 200, headers: { 'Content-Type': 'application/json' }, body: '{"ocupados":{}}' };
  }
};
