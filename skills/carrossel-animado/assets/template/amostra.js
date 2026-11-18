// Amostra da marca: as mesmas fontes e cores nos três fundos, com as letras acentuadas.
// Em coluna, para o texto nunca se sobrepor, seja qual for a largura da fonte.
const BR = MARCA.idioma === 'pt-BR';
const LINHA = 'Ação, coração, útil, é, à, ã, õ, ç';
function amostra(titulo, extra) {
  const c = el('abs', { left: '64px', top: '150px', width: '950px', display: 'flex', flexDirection: 'column', gap: '56px' });
  el('titulo', { fontSize: '150px', lineHeight: 0.96 }, titulo, c);
  el('texto', { fontSize: '42px', lineHeight: 1.3 }, LINHA, c);
  extra(c);
  handle();
}
const SLIDES = {
  1: () => {
    amostra(`${BR ? 'Seu título' : 'O teu título'}<br><i class="ac">em grande.</i>`, (c) => el('etiqueta', { fontSize: '34px', color: 'var(--ac)' }, 'ETIQUETA', c));
    return { seek() {} };
  },
  2: () => {
    amostra('Um cartaz<br><i class="ac">forte.</i>', () => {});
    return { theme: 'destaque', seek() {} };
  },
  3: () => {
    amostra('Um slide<br><i class="ac">para guardar.</i>', (c) => el('titulo', { fontSize: '76px', fontStyle: 'italic' }, '<span class="marcador">Com marcador</span>', c));
    return { theme: 'papel', seek() {} };
  },
};

arrancar(SLIDES);
