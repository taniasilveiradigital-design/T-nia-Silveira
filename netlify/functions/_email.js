// Envia emails a partir de contacto@taniasilveira.pt (Resend). Variável: RESEND_API_KEY.
const FROM = 'Tânia Silveira <contacto@taniasilveira.pt>';
const esc = s => String(s || '').replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));

function moldura(titulo, corpo) {
  return `<!doctype html><html lang="pt-PT"><body style="margin:0;background:#faf6f1;font-family:Raleway,Helvetica,Arial,sans-serif;color:#33221b">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:#faf6f1;padding:32px 12px"><tr><td align="center">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="max-width:560px;background:#ffffff;border:1px solid #e2d4c7">
<tr><td style="background:#2b1c16;padding:30px 36px">
<div style="font:600 10px/1.6 Helvetica,Arial,sans-serif;letter-spacing:3px;text-transform:uppercase;color:#bfa795">Tânia Silveira · Estratégia para moda e têxtil</div>
<div style="font:400 30px/1.15 Georgia,serif;color:#ffffff;margin-top:10px">${titulo}</div></td></tr>
<tr><td style="padding:0 36px"><div style="border-top:1.5px dashed #ba8166;margin:0"></div></td></tr>
<tr><td style="padding:28px 36px 34px;font-size:15px;line-height:1.65">${corpo}</td></tr>
<tr><td style="background:#f3ebe2;padding:20px 36px;font-size:12px;color:#6f5a4f;line-height:1.6">
<span style="font:italic 20px Georgia,serif;color:#b26d47">Tânia Silveira</span><br>
taniasilveira.pt · contacto@taniasilveira.pt · Guimarães, Portugal</td></tr>
</table></td></tr></table></body></html>`;
}

function linha(rotulo, valor) {
  return `<tr><td style="padding:10px 0;border-bottom:1px solid #e2d4c7;font:600 10px/1.6 Helvetica,Arial,sans-serif;letter-spacing:2px;text-transform:uppercase;color:#b26d47;width:120px;vertical-align:top">${rotulo}</td><td style="padding:10px 0;border-bottom:1px solid #e2d4c7;color:#33221b">${valor}</td></tr>`;
}

function confirmacaoCliente(m) {
  const meet = m.meet ? `<p style="margin:26px 0"><a href="${esc(m.meet)}" style="background:#b26d47;color:#ffffff;text-decoration:none;font:600 12px/1 Helvetica,Arial,sans-serif;letter-spacing:2px;text-transform:uppercase;padding:16px 26px;display:inline-block">Entrar na videochamada</a></p>` : '';
  return moldura('Está marcado.', `
<p style="margin:0 0 18px">Olá ${esc(m.nome.split(' ')[0])},</p>
<p style="margin:0 0 20px">A tua sessão ficou marcada. Guarda este email: tem tudo o que precisas.</p>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0">${linha('Sessão', esc(m.evento))}${linha('Quando', esc(m.quando) + ' (hora de Lisboa)')}${linha('Onde', 'Google Meet')}</table>
${meet}
<div style="background:#faf6f1;border-left:2px solid #ba8166;padding:14px 18px;margin:8px 0 20px">
<b style="font:400 18px Georgia,serif;color:#5c3b2e">Antes da sessão</b><br>Traz os números da tua marca: custos de uma peça, preços, vendas dos últimos meses. O trabalho começa antes de entrares.</div>
<p style="margin:0">Se precisares de mudar a hora, responde a este email com pelo menos 72 horas de antecedência.</p>
<p style="margin:18px 0 0">Bora fazer acontecer.</p>`);
}

function avisoTania(m) {
  return moldura('Nova marcação', `<table role="presentation" width="100%" cellpadding="0" cellspacing="0">
${linha('Sessão', esc(m.evento))}${linha('Quando', esc(m.quando))}${linha('Nome', esc(m.nome))}${linha('Email', esc(m.email))}${linha('Marca', esc(m.marca) || '—')}${linha('Quer trabalhar', esc(m.mensagem) || '—')}${linha('Meet', m.meet ? `<a href="${esc(m.meet)}">${esc(m.meet)}</a>` : '—')}</table>`);
}

function ics(m) {
  const f = s => s.replace(/[-:]/g, '').replace(/\.\d{3}/, '');
  return ['BEGIN:VCALENDAR', 'VERSION:2.0', 'PRODID:-//taniasilveira.pt//agenda//PT', 'METHOD:PUBLISH', 'BEGIN:VEVENT',
    'UID:' + m.uid + '@taniasilveira.pt', 'DTSTAMP:' + f(new Date().toISOString()), 'DTSTART:' + f(m.inicio), 'DTEND:' + f(m.fim),
    'SUMMARY:' + m.evento + ' · Tânia Silveira', 'LOCATION:' + (m.meet || 'Google Meet'), 'DESCRIPTION:' + (m.meet ? 'Videochamada: ' + m.meet : ''),
    'ORGANIZER;CN=Tânia Silveira:mailto:contacto@taniasilveira.pt', 'END:VEVENT', 'END:VCALENDAR'].join('\r\n');
}

async function enviar({ para, assunto, html, anexoIcs, responderA }) {
  const r = await fetch('https://api.resend.com/emails', {
    method: 'POST',
    headers: { Authorization: 'Bearer ' + process.env.RESEND_API_KEY, 'Content-Type': 'application/json' },
    body: JSON.stringify({
      from: FROM, to: [para], subject: assunto, html, reply_to: responderA || 'contacto@taniasilveira.pt',
      attachments: anexoIcs ? [{ filename: 'sessao-tania-silveira.ics', content: Buffer.from(anexoIcs).toString('base64') }] : undefined
    })
  });
  if (!r.ok) throw new Error('resend ' + r.status + ' ' + (await r.text()));
}

module.exports = { confirmacaoCliente, avisoTania, ics, enviar };
