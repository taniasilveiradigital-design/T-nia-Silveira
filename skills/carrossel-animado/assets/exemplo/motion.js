// EXEMPLO em modo motion, sem fotos: mostra como se constrói cada gesto. Não repitas as composições sem razão.
// Corre com: python novo.py nome --exemplo

const SLIDES = {
  // 1 PARAR: muitas coisas a mexer ao mesmo tempo, e o título quieto.
  1: () => {
    const SPOTS = [['Título', 90, 120], ['Foto', 640, 90], ['Ícone', 330, 250], ['Fundo', 780, 300], ['Seta', 120, 420], ['Moldura', 520, 470], ['Logótipo', 240, 620], ['Autocolante', 640, 680]];
    const chips = SPOTS.map((c) => el('etq', { left: px(c[1]), top: px(c[2]), fontSize: '38px' }, c[0]));
    el('abs titulo', { left: '60px', top: '830px', fontSize: '172px', lineHeight: 0.92, whiteSpace: 'nowrap' }, 'Se tudo mexe,<br><i class="ac">nada se lê.</i>');
    handle();
    const seta = el('seta', {}, 'Desliza <b>&gt;</b>').querySelector('b');
    return {
      seek(t) {
        // Oito voltas certas em 8 s: o fim encaixa no início.
        chips.forEach((c, i) => {
          const a = wave(t, 8, i % 2 ? Math.PI : 0);
          c.style.transform = `translate(${12 * a}px,${-16 * a}px) rotate(${6 * a}deg)`;
        });
        seta.style.transform = `translateX(${8 + 8 * wave(t, 2, -Math.PI / 2)}px)`;
      },
    };
  },
  // 2 REVELAÇÃO: o contador e a película enchem-se. O que salta passa pela opacidade 0.
  2: () => {
    el('abs titulo', { left: '60px', top: '64px', fontSize: '150px', lineHeight: 0.94 }, 'Um vídeo é<br><i class="ac">muitas fotos.</i>');
    const counter = el('abs titulo', { left: '60px', top: '440px', fontSize: '300px', lineHeight: 1, fontVariantNumeric: 'lining-nums tabular-nums' }, '240');
    el('abs texto', { left: '64px', top: '780px', fontSize: '44px', fontWeight: 600 }, 'fotos, só neste slide.');
    const tira = el('tira', { top: '960px' });
    el('furos', { top: '9px' }, '', tira); el('furos', { bottom: '9px' }, '', tira);
    const cels = [], dots = [];
    for (let i = 0; i < 10; i++) {
      cels.push(el('cel', { left: px(18 + i * 106) }, '', tira));
      dots.push(el('', { top: px(10 + (i / 9) * 74) }, '', cels[i], 'i'));
    }
    handle();
    return {
      theme: 'destaque',
      seek(t) {
        const prog = t < 1.75 ? 1 : clamp((t - 2) / 4);
        const fade = salto(t, 1.75);
        counter.textContent = String(Math.round(prog * 240));
        counter.style.opacity = fade;
        cels.forEach((c, i) => {
          dots[i].style.opacity = (0.12 + 0.88 * clamp(prog * 10 - i)) * fade;
        });
      },
    };
  },
  // 3 DEMONSTRAÇÃO: uma cena em canvas. A bola estica no ar e achata ao chegar.
  3: () => {
    const g = tela();
    el('abs titulo', { left: '60px', top: '64px', fontSize: '150px', lineHeight: 0.94 }, 'O peso é<br><i class="ac">o que convence.</i>');
    el('abs texto', { left: '64px', top: '1090px', width: '950px', fontSize: '42px', lineHeight: 1.3 }, 'O que cai estica no ar e achata ao chegar. Sem isto, parece um slide de escritório.');
    handle();
    const CHAO = 1000, R = 92;
    return {
      seek(t) {
        g.clearRect(0, 0, 1080, 1350);
        const u = mod(t, 2);   // Ciclo de 2 s, quatro vezes em 8 s.
        let y = 0, estica = 0, achata = 0;
        if (u >= 0.4 && u < 1.6) {
          const p = (u - 0.4) / 1.2;
          y = 430 * 4 * p * (1 - p);
          estica = 0.22 * Math.abs(1 - 2 * p);
        } else if (u >= 1.6) {
          // O ressalto apaga-se antes dos 2 s, para o frame 0 ser a bola em repouso.
          const d = u - 1.6;
          achata = 0.34 * Math.exp(-d * 9) * Math.cos(d * 24) * (1 - d / 0.4);
        }
        const sx = 1 - estica * 0.6 + achata, sy = 1 + estica - achata;
        // Sombra: encolhe quando a bola sobe.
        g.fillStyle = 'rgba(0,0,0,.35)';
        g.beginPath(); g.ellipse(540, CHAO + 6, R * (1.1 - y / 900) * sx, 20 * (1 - y / 900), 0, 0, 7); g.fill();
        g.fillStyle = COR.creme; g.fillRect(64, CHAO, 952, 6);
        g.save();
        g.translate(540, CHAO - y); g.scale(sx, sy);
        g.fillStyle = COR.destaque;
        g.beginPath(); g.arc(0, -R, R, 0, 7); g.fill();
        g.restore();
      },
    };
  },
  // 4 GUARDAR: papel, vale sozinho fora do carrossel. Os números acendem um a um.
  4: () => {
    el('abs etiqueta', { left: '64px', top: '64px', fontSize: '28px', letterSpacing: '.08em', color: 'var(--ac)' }, 'GUARDA ESTE SLIDE');
    el('abs titulo', { left: '60px', top: '124px', fontSize: '112px', lineHeight: 1, whiteSpace: 'nowrap' }, 'As regras, <i class="ac">em 5 linhas</i>');
    const ROWS = [
      ['O primeiro frame é a capa.', 'Antes de mexer, já é um slide acabado.'],
      ['Texto antes do movimento.', 'Primeiro o que se diz, depois o que mexe.'],
      ['Um gesto por slide.', 'O resto fica quieto e legível.'],
      ['Gestos a tempo.', 'Começam a cada meio segundo, nunca ao calhas.'],
      ['O fim cola no início.', 'O último frame encaixa no primeiro.'],
    ];
    const nums = ROWS.map((r, i) => {
      const l = el('linha', { top: px(270 + i * 186) }, `<div class="num">${i + 1}</div><div><b>${r[0]}</b><span>${r[1]}</span></div>`);
      return l.querySelector('.num');
    });
    handle();
    const AT = [2, 2.5, 3, 3.5, 4];
    return {
      theme: 'papel',
      seek(t) {
        nums.forEach((n, i) => {
          const on = t < 1.25 || t >= AT[i];
          n.style.background = on ? COR.destaquePapel : 'transparent';
          n.style.color = on ? COR.creme : COR.escuro;
          n.style.boxShadow = on ? 'none' : `inset 0 0 0 2px ${COR.escuro}`;
          const d = t - AT[i];
          n.style.transform = `scale(${1 + 0.28 * (d >= 0 && d < 0.5 ? Math.exp(-d * 9) : 0)})`;
        });
      },
    };
  },
  // 5 APLICAÇÃO: o pedido escreve-se sozinho. O texto por escrever ocupa espaço, para a caixa não mudar.
  5: () => {
    el('abs titulo', { left: '60px', top: '120px', fontSize: '168px', lineHeight: 0.94 }, 'Começa por<br><i class="ac">um slide só.</i>');
    const v = el('vidro', { top: '560px', height: '500px' });
    el('', { font: '500 30px Etiqueta', color: COR.claro, marginBottom: '20px' }, 'Experimenta pedir:', v);
    const PEDIDO = 'Anima só o título da minha capa. O primeiro frame fica igual à imagem original, e o vídeo dá a volta em 8 segundos, sem som.';
    const box = el('', { font: '500 48px/1.3 Texto' }, '', v);
    const shown = el('', {}, '', box, 'span');
    const caret = el('caret', {}, '', box, 'span');
    const rest = el('', { visibility: 'hidden' }, '', box, 'span');
    handle();
    return {
      seek(t) {
        const done = t < 1.75 ? 1 : clamp((t - 2) / 3.75);
        const n = Math.floor(PEDIDO.length * done);
        box.style.opacity = salto(t, 1.75);
        shown.textContent = PEDIDO.slice(0, n);
        rest.textContent = PEDIDO.slice(n);
        caret.style.display = done > 0 && done < 1 ? 'inline-block' : 'none';
      },
    };
  },
  // 6 AGIR: o comentário escreve-se e o coração salta. Uma só chamada para ação.
  6: () => {
    el('abs titulo', { left: '60px', top: '150px', fontSize: '190px', lineHeight: 0.92 }, 'Queres<br><i class="ac">o modelo?</i>');
    el('abs titulo', { left: '64px', top: '760px', width: '950px', fontSize: '84px', lineHeight: 1 }, 'Comenta <i class="ac">MEXE</i> e <span style="white-space:nowrap">envio-te</span> o guia.');
    const caixa = el('caixa', { top: '1000px' });
    const txt = el('abs', { left: '46px', top: '32px', font: '600 44px Texto', whiteSpace: 'nowrap', letterSpacing: '.02em' }, '', caixa);
    const heart = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    heart.setAttribute('viewBox', '0 0 24 24'); heart.setAttribute('width', '68'); heart.setAttribute('height', '68');
    heart.style.cssText = 'position:absolute;left:846px;top:24px;transform-origin:50% 50%;will-change:transform';
    heart.innerHTML = `<path fill="${COR.destaquePapel}" d="M12 21s-7.5-4.6-9.8-9.2C.6 8.5 2.4 4.6 6.2 4.3c2.3-.2 4.3 1 5.8 3.1 1.5-2.1 3.5-3.3 5.8-3.1 3.8.3 5.6 4.2 4 7.5C19.5 16.4 12 21 12 21z"/>`;
    caixa.appendChild(heart);
    handle();
    const PALAVRA = 'MEXE';
    return {
      theme: 'destaque',
      seek(t) {
        const done = t < 1.75 ? 1 : clamp((t - 2) / 1.25);
        const n = Math.floor(PALAVRA.length * done);
        txt.style.opacity = salto(t, 1.75);
        txt.innerHTML = PALAVRA.slice(0, n) + (done > 0 && done < 1 ? '<span class="caret"></span>' : '');
        let k = 1;
        if (t >= 1.5 && t < 1.75) k = 1 - inOut((t - 1.5) / 0.25);
        else if (t >= 1.75 && t < 4) k = 0;
        else if (t >= 4 && t < 4.9) { const d = t - 4; k = Math.max(0, 1 + 0.5 * Math.exp(-d * 6) * Math.cos(d * 20) - Math.exp(-d * 22) * 1.5); }
        heart.style.transform = `scale(${k})`;
      },
    };
  },
};

arrancar(SLIDES, { seam: [420, 1020, 300, 1100, 640] });
