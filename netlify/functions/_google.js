// Ligação ao Google Calendar da Tânia (conta onde faz os Meet).
// Variáveis no Netlify: GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, GOOGLE_REFRESH_TOKEN, GOOGLE_CALENDAR_ID (normalmente "primary").
const TOKEN_URL = 'https://oauth2.googleapis.com/token';
const API = 'https://www.googleapis.com/calendar/v3';

async function token() {
  const r = await fetch(TOKEN_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({
      client_id: process.env.GOOGLE_CLIENT_ID,
      client_secret: process.env.GOOGLE_CLIENT_SECRET,
      refresh_token: process.env.GOOGLE_REFRESH_TOKEN,
      grant_type: 'refresh_token'
    })
  });
  if (!r.ok) throw new Error('google token ' + r.status);
  return (await r.json()).access_token;
}

async function ocupado(de, ate) {
  const t = await token();
  const r = await fetch(API + '/freeBusy', {
    method: 'POST',
    headers: { Authorization: 'Bearer ' + t, 'Content-Type': 'application/json' },
    body: JSON.stringify({ timeMin: de, timeMax: ate, timeZone: 'Europe/Lisbon', items: [{ id: process.env.GOOGLE_CALENDAR_ID || 'primary' }] })
  });
  if (!r.ok) throw new Error('freebusy ' + r.status);
  const j = await r.json();
  return Object.values(j.calendars)[0].busy || [];
}

// Cria o evento com Meet. Sem convidados: o convite à cliente é enviado pelo nosso email (contacto@).
async function criarEvento({ inicio, fim, titulo, descricao }) {
  const t = await token();
  const cal = encodeURIComponent(process.env.GOOGLE_CALENDAR_ID || 'primary');
  const r = await fetch(`${API}/calendars/${cal}/events?conferenceDataVersion=1&sendUpdates=none`, {
    method: 'POST',
    headers: { Authorization: 'Bearer ' + t, 'Content-Type': 'application/json' },
    body: JSON.stringify({
      summary: titulo,
      description: descricao,
      start: { dateTime: inicio, timeZone: 'Europe/Lisbon' },
      end: { dateTime: fim, timeZone: 'Europe/Lisbon' },
      conferenceData: { createRequest: { requestId: 'ts-' + Date.now(), conferenceSolutionKey: { type: 'hangoutsMeet' } } },
      reminders: { useDefault: true }
    })
  });
  if (!r.ok) throw new Error('evento ' + r.status + ' ' + (await r.text()));
  const ev = await r.json();
  const meet = ev.hangoutLink || (ev.conferenceData?.entryPoints || []).find(e => e.entryPointType === 'video')?.uri || '';
  return { id: ev.id, meet };
}

module.exports = { ocupado, criarEvento };
