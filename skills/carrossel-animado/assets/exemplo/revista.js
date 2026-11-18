// EXEMPLO em modo revista: só para ler, porque precisa de fotos fotos/f1 a f6. Mostra como se constrói cada gesto.
// O texto é só de exemplo: diz o que cada composição faz. Não repitas as composições sem razão.

const SEAM = [760, 1040, 1120, 300, 420];

const SLIDES = {
  // A palavra gigante atrás da cabeça. Vai em s.tras, que fica entre a foto e o recorte.
  1: () => {
    const s = cena(1, { y: -140 });
    const g = el('abs titulo', { left: '30px', top: '56px', whiteSpace: 'nowrap', fontSize: '296px', lineHeight: 1, fontStyle: 'italic' }, 'Palavra', s.tras);
    scrim(24, 46);
    el('abs titulo', { left: '64px', right: '64px', top: '950px', fontSize: '132px', lineHeight: 0.94 }, 'atrás da cabeça, <i class="ac">e título por baixo.</i>');
    handle();
    const seta = el('seta', {}, 'Desliza <b>&gt;</b>').querySelector('b');
    return {
      seek(t) {
        zoom(s.c, t);
        g.style.transform = `translateX(${14 * wave(t, 1)}px)`;
        seta.style.transform = `translateX(${8 + 8 * wave(t, 2, -Math.PI / 2)}px)`;
      },
    };
  },
  // Um carimbo em marcador que cai com peso, e o resto quieto.
  2: () => {
    const s = cena(2, { x: -110, y: -190 });
    scrim(26, 48);
    el('abs titulo', { left: '64px', right: '64px', top: '846px', fontSize: '142px', lineHeight: 0.94 }, 'Um carimbo<br><i class="ac">que cai.</i>');
    handle();
    const stamp = el('abs titulo', { left: '60px', top: '58px', fontSize: '128px', lineHeight: 1, transformOrigin: '30% 60%', whiteSpace: 'nowrap', fontStyle: 'italic' }, '<span class="marcador">Carimbo!</span>');
    const REST = 'rotate(-3deg)';
    return {
      seek(t) {
        zoom(s.c, t);
        if (t < 1.5) { stamp.style.opacity = 1; stamp.style.transform = REST; }
        else if (t < 1.75) { stamp.style.opacity = 1 - (t - 1.5) / 0.25; stamp.style.transform = REST; }
        else if (t < 2.75) { stamp.style.opacity = 0; }
        else if (t < 3) {
          const p = inCubic((t - 2.75) / 0.25);
          stamp.style.opacity = clamp(p * 3);
          stamp.style.transform = `${REST} scale(${2.1 - 1.1 * p})`;
        } else {
          const d = t - 3;
          const a = d > 1 ? 0 : Math.exp(-d * 9) * Math.cos(d * 26);
          stamp.style.opacity = 1;
          stamp.style.transform = a === 0 ? REST : `${REST} scale(${1 + 0.1 * a},${1 - 0.1 * a})`;
        }
      },
    };
  },
  // Um número que corre atrás da cabeça. Passa pela opacidade 0 antes de saltar.
  3: () => {
    const s = cena(3, { x: 0, y: -40, w: 1080 });
    const tc = el('abs titulo', { left: 0, right: 0, top: '30px', textAlign: 'center', fontSize: '254px', lineHeight: 1, whiteSpace: 'nowrap', fontVariantNumeric: 'lining-nums tabular-nums' }, '02:00:00', s.tras);
    scrim(26, 44);
    el('abs titulo', { left: '64px', width: '950px', top: '850px', fontSize: '84px', lineHeight: 1 }, 'Um número a correr,<br>atrás da cabeça,<br><i class="ac">e uma pergunta por baixo?</i>');
    handle();
    const fmt = (x) => [x / 3600, (x % 3600) / 60, x % 60].map((v) => String(Math.floor(v)).padStart(2, '0')).join(':');
    return {
      seek(t) {
        zoom(s.c, t);
        const p = t < 0.5 ? 1 : inOut(clamp((t - 0.5) / 4));
        tc.textContent = fmt(Math.round(7200 * p));
        tc.style.opacity = salto(t, 0.5);
      },
    };
  },
  // Poster na cor de destaque, com o recorte da pessoa por cima de uma película.
  4: () => {
    const counter = el('abs titulo', { left: '64px', top: '620px', fontSize: '176px', lineHeight: 1, fontVariantNumeric: 'lining-nums tabular-nums' }, '240');
    const tira = el('tira', { top: '990px' });
    el('furos', { top: '9px' }, '', tira); el('furos', { bottom: '9px' }, '', tira);
    const cels = [], dots = [];
    for (let i = 0; i < 10; i++) {
      cels.push(el('cel', { left: px(18 + i * 106) }, '', tira));
      dots.push(el('', { top: px(10 + (i / 9) * 74) }, '', cels[i], 'i'));
    }
    recorte(4, { x: 262, y: 210, w: 960 });
    el('abs titulo', { left: '64px', top: '64px', width: '960px', fontSize: '128px', lineHeight: 0.96 }, 'Poster com<br>a <i class="ac">pessoa à frente.</i>');
    handle();
    return {
      theme: 'destaque',
      seek(t) {
        const prog = t < 1.75 ? 1 : clamp((t - 2) / 4);
        const fade = salto(t, 1.75);
        counter.textContent = String(Math.round(prog * 240));
        counter.style.opacity = fade;
        cels.forEach((c, i) => { dots[i].style.opacity = (0.12 + 0.88 * clamp(prog * 10 - i)) * fade; });
      },
    };
  },
  // Antes e depois: a mesma foto em dois cartões.
  5: () => {
    el('abs titulo', { left: '64px', top: '62px', fontSize: '168px', lineHeight: 0.92 }, 'Antes<br><i class="ac">e depois.</i>');
    const L = el('cartao', { left: '64px', backgroundImage: 'url(fotos/f5.jpg)' });
    const R = el('cartao', { left: '560px', backgroundImage: 'url(fotos/f5.jpg)' });
    el('rot', {}, 'Antes', L);
    el('rot', { color: COR.claro }, 'Depois', R);
    const chips = [['Um', 24, 96], ['Dois', 290, 150], ['Três', 30, 330], ['Quatro', 300, 400]].map((c) => el('etq', { left: px(c[1]), top: px(c[2]) }, c[0], L));
    const um = el('etq', { left: '24px', top: '540px', background: COR.marcador }, 'Só um', R);
    handle();
    return {
      seek(t) {
        chips.forEach((c, i) => {
          const a = wave(t, 8, i % 2 ? Math.PI : 0);
          c.style.transform = `translate(${10 * a}px,${-14 * a}px) rotate(${6 * a}deg)`;
        });
        let x = 0, op = 1;
        if (t >= 1.5 && t < 1.75) op = 1 - (t - 1.5) / 0.25;
        else if (t >= 1.75 && t < 2) op = 0;
        else if (t >= 2 && t < 2.75) { const p = outCubic((t - 2) / 0.75); x = -60 * (1 - p); op = p; }
        um.style.opacity = op;
        um.style.transform = `translateX(${x}px)`;
      },
    };
  },
  // A chamada para ação, com uma palavra atrás da cabeça.
  6: () => {
    const s = cena(6, { y: -120 });
    const g = el('abs titulo', { left: '48px', top: '70px', fontSize: '300px', lineHeight: 1, fontStyle: 'italic', whiteSpace: 'nowrap' }, 'guia?', s.tras);
    el('abs titulo', { left: '64px', top: '16px', fontSize: '84px', lineHeight: 1 }, 'Queres o', s.tras);
    scrim(22, 40, 0.96);
    el('abs titulo', { left: '64px', width: '950px', top: '1058px', fontSize: '84px', lineHeight: 1 }, 'Comenta <i class="ac">PALAVRA</i><br>e <span style="white-space:nowrap">envio-te</span> o guia.');
    handle();
    return {
      seek(t) {
        zoom(s.c, t);
        g.style.transform = `translateX(${12 * wave(t, 1)}px)`;
      },
    };
  },
};

arrancar(SLIDES, { seam: SEAM });
