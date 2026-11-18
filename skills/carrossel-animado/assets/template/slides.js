// Substitui por completo. Cada slide devolve { theme?, seek(t) }. Ver references/motor.md.
const SLIDES = {
  1: () => {
    el('abs titulo', { left: '64px', top: '120px', width: '950px', fontSize: '160px', lineHeight: 0.94 }, 'Título em duas linhas,<br><i class="ac">a segunda em itálico.</i>');
    handle();
    return { theme: 'papel', seek(t) {} };
  },
};

arrancar(SLIDES);
