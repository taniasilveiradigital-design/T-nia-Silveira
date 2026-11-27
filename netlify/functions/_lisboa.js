// Converte "YYYY-MM-DD" + "HH:MM" de Lisboa para ISO com o desvio certo (inverno +00:00, verão +01:00).
function offsetLisboa(y, m, d, hh, mm) {
  const guess = Date.UTC(y, m - 1, d, hh, mm);
  const parts = new Intl.DateTimeFormat('en-GB', { timeZone: 'Europe/Lisbon', hour12: false, year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit' })
    .formatToParts(new Date(guess)).reduce((a, p) => (a[p.type] = p.value, a), {});
  const asLocal = Date.UTC(+parts.year, +parts.month - 1, +parts.day, +parts.hour % 24, +parts.minute);
  return (asLocal - guess) / 60000;
}
function isoLisboa(data, hora, somaMin = 0) {
  const [y, m, d] = data.split('-').map(Number); const [hh, mm] = hora.split(':').map(Number);
  const off = offsetLisboa(y, m, d, hh, mm);
  const utc = Date.UTC(y, m - 1, d, hh, mm) - off * 60000 + somaMin * 60000;
  return new Date(utc).toISOString();
}
module.exports = { isoLisboa };
