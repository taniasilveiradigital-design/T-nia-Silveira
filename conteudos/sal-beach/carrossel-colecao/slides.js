// Sal Beach: lançamento de coleção. 5 slides, motion sem fotos.

// Ondas em canvas: cada camada dá voltas inteiras em 8 s, por isso o fim encaixa no início.
function ondas(g, t, base, cores, amp) {
  cores.forEach((cor, i) => {
    const y0 = base + i * 70;
    const dir = i % 2 ? -1 : 1;
    g.fillStyle = cor;
    g.beginPath();
    g.moveTo(0, 1350);
    for (let x = 0; x <= 1080; x += 12) {
      const fase = (x / 1080) * Math.PI * 2 * (1 + i);
      const y = y0 + amp * Math.sin(fase + dir * Math.PI * 2 * (t / 8) * (i + 1)) + 0.35 * amp * Math.sin(fase * 2 + i - dir * Math.PI * 2 * (t / 8) * 2);
      g.lineTo(x, y);
    }
    g.lineTo(1080, 1350);
    g.closePath();
    g.fill();
  });
}

const SLIDES = {
  // 1 PARAR: o mar mexe por baixo, o título quieto.
  1: () => {
    const g = tela();
    el('abs etiqueta', { left: '64px', top: '140px', fontSize: '30px', letterSpacing: '.14em', color: 'var(--ac)' }, 'NOVA COLEÇÃO');
    el('abs titulo', { left: '58px', top: '200px', fontSize: '210px', lineHeight: 0.9 }, 'Sabe<br><i class="ac">a sal.</i>');
    handle();
    const seta = el('seta', {}, 'Desliza <b>&gt;</b>').querySelector('b');
    return {
      seek(t) {
        g.clearRect(0, 0, 1080, 1350);
        const r = 120 + 6 * wave(t, 2);
        g.fillStyle = COR.destaque;
        g.beginPath(); g.arc(800, 760, r, 0, 7); g.fill();
        g.globalAlpha = 0.18;
        g.beginPath(); g.arc(800, 760, r + 40 + 10 * wave(t, 2), 0, 7); g.fill();
        g.globalAlpha = 1;
        ondas(g, t, 820, ['rgba(246,185,156,.35)', 'rgba(251,246,238,.22)', 'rgba(232,103,60,.55)', COR.escuro], 26);
        seta.style.transform = `translateX(${8 + 8 * wave(t, 2, -Math.PI / 2)}px)`;
      },
    };
  },

  // 2 PROMESSA: o sol faz o dia inteiro. Na capa está no alto; a meio desaparece e nasce outra vez.
  2: () => {
    const g = tela();
    el('abs titulo', { left: '60px', top: '150px', fontSize: '150px', lineHeight: 0.92 }, 'Do primeiro<br>mergulho<br><i class="ac">ao pôr do sol.</i>');
    el('abs texto', { left: '64px', top: '1100px', width: '860px', fontSize: '42px', lineHeight: 1.3, fontWeight: 500 }, 'Peças para o dia inteiro na praia.');
    handle();
    const CX = 540, CY = 1040, R = 340;
    return {
      theme: 'destaque',
      seek(t) {
        g.clearRect(0, 0, 1080, 1350);
        let ang = 0.5, op = 1;
        if (t >= 1.5 && t < 1.75) op = 1 - (t - 1.5) / 0.25;
        else if (t >= 1.75 && t < 2) op = 0;
        else if (t >= 2) { ang = 0.5 * outCubic(clamp((t - 2) / 3.5)); op = clamp((t - 2) / 0.4); }
        const a = Math.PI * (1 - ang);
        const sx = CX + R * Math.cos(a), sy = CY - R * Math.sin(a);
        g.strokeStyle = 'rgba(12,36,48,.25)'; g.lineWidth = 3; g.setLineDash([10, 14]);
        g.beginPath(); g.arc(CX, CY, R, Math.PI, 0); g.stroke(); g.setLineDash([]);
        g.globalAlpha = op;
        g.fillStyle = COR.creme;
        g.beginPath(); g.arc(sx, sy, 70, 0, 7); g.fill();
        g.globalAlpha = 1;
        g.fillStyle = COR.escuro; g.fillRect(64, CY, 952, 6);
      },
    };
  },

  // 3 REVELAÇÃO: a coleção passa como uma montra. Avança 5 cartões em 8 s, por isso o loop encaixa.
  3: () => {
    el('abs titulo', { left: '60px', top: '150px', fontSize: '170px', lineHeight: 0.9 }, 'Do mar<br><i class="ac">ao jantar.</i>');
    const PECAS = ['Biquíni', 'Fato de banho', 'Saída de praia', 'Vestido', 'Acessórios'];
    const W = 400, GAP = 40, PASSO = W + GAP, N = PECAS.length;
    const fita = el('abs', { left: '0', top: '600px', width: '1080px', height: '440px', overflow: 'hidden' });
    const cards = [];
    for (let k = 0; k < N * 2; k++) {
      const i = k % N;
      const c = el('abs', { left: '0', top: '0', width: px(W), height: '420px', borderRadius: '28px', background: i % 2 ? COR.destaque : COR.claro, color: COR.escuro, willChange: 'transform' }, '', fita);
      el('abs etiqueta', { left: '34px', top: '34px', fontSize: '28px', letterSpacing: '.1em' }, String(i + 1).padStart(2, '0'), c);
      el('abs titulo', { left: '32px', bottom: '30px', fontSize: '64px', lineHeight: 0.95, width: '340px' }, PECAS[i], c);
      cards.push(c);
    }
    el('abs texto', { left: '64px', top: '1100px', width: '860px', fontSize: '42px', lineHeight: 1.3, fontWeight: 500 }, 'Uma coleção para o dia todo.');
    handle();
    return {
      seek(t) {
        const off = (t / 8) * N * PASSO;
        cards.forEach((c, k) => {
          const x = mod(k * PASSO - off, N * 2 * PASSO) - PASSO + 64;
          c.style.transform = `translateX(${x}px)`;
        });
      },
    };
  },

  // 4 GUARDAR: papel. Os tamanhos acendem um a um.
  4: () => {
    el('abs etiqueta', { left: '64px', top: '140px', fontSize: '30px', letterSpacing: '.1em', color: 'var(--ac)' }, 'GUARDA ESTE SLIDE');
    el('abs titulo', { left: '60px', top: '200px', fontSize: '170px', lineHeight: 0.9 }, 'Do XS<br><i class="ac">ao XXL.</i>');
    el('abs texto', { left: '64px', top: '600px', width: '860px', fontSize: '44px', lineHeight: 1.3, fontWeight: 500 }, 'Seis tamanhos. Escolhe o teu e, se tiveres dúvidas, fala connosco.');
    const T = ['XS', 'S', 'M', 'L', 'XL', 'XXL'];
    const AT = [2, 2.5, 3, 3.5, 4, 4.5];
    const bolas = T.map((s, i) => el('abs', { left: px(64 + (i % 3) * 300), top: px(820 + Math.floor(i / 3) * 190), width: '160px', height: '160px', borderRadius: '50%', display: 'flex', alignItems: 'center', justifyContent: 'center', font: '600 48px Texto', willChange: 'transform' }, s));
    handle();
    return {
      theme: 'papel',
      seek(t) {
        bolas.forEach((b, i) => {
          const on = t < 1.25 || t >= AT[i];
          b.style.background = on ? COR.destaquePapel : 'transparent';
          b.style.color = on ? COR.creme : COR.escuro;
          b.style.boxShadow = on ? 'none' : `inset 0 0 0 3px ${COR.escuro}`;
          const d = t - AT[i];
          b.style.transform = `scale(${1 + 0.22 * (d >= 0 && d < 0.5 ? Math.exp(-d * 9) : 0)})`;
        });
      },
    };
  },

  // 5 AGIR: o comentário escreve-se e o coração salta.
  5: () => {
    el('abs titulo', { left: '60px', top: '170px', fontSize: '180px', lineHeight: 0.9 }, 'Queres<br><i class="ac">ver tudo?</i>');
    el('abs titulo', { left: '64px', top: '600px', width: '860px', fontSize: '88px', lineHeight: 1 }, 'Comenta <i class="ac">SAL</i><br>e <span style="white-space:nowrap">envio-te</span> o catálogo.');
    const caixa = el('caixa', { top: '980px' });
    const txt = el('abs', { left: '46px', top: '32px', font: '600 44px Texto', whiteSpace: 'nowrap', letterSpacing: '.02em' }, '', caixa);
    const heart = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    heart.setAttribute('viewBox', '0 0 24 24'); heart.setAttribute('width', '68'); heart.setAttribute('height', '68');
    heart.style.cssText = 'position:absolute;left:846px;top:24px;transform-origin:50% 50%;will-change:transform;transform:scale(1)';
    heart.innerHTML = `<path fill="${COR.destaquePapel}" d="M12 21s-7.5-4.6-9.8-9.2C.6 8.5 2.4 4.6 6.2 4.3c2.3-.2 4.3 1 5.8 3.1 1.5-2.1 3.5-3.3 5.8-3.1 3.8.3 5.6 4.2 4 7.5C19.5 16.4 12 21 12 21z"/>`;
    caixa.appendChild(heart);
    handle();
    const PALAVRA = 'SAL';
    return {
      theme: 'destaque',
      seek(t) {
        const done = t < 1.75 ? 1 : clamp((t - 2) / 1);
        const n = Math.floor(PALAVRA.length * done);
        txt.style.opacity = salto(t, 1.75);
        txt.innerHTML = PALAVRA.slice(0, n) + (done > 0 && done < 1 ? '<span class="caret"></span>' : '');
        let k = 1;
        if (t >= 1.5 && t < 1.75) k = 1 - inOut((t - 1.5) / 0.25);
        else if (t >= 1.75 && t < 3.5) k = 0;
        else if (t >= 3.5 && t < 4.4) { const d = t - 3.5; k = Math.max(0, 1 + 0.5 * Math.exp(-d * 6) * Math.cos(d * 20) - Math.exp(-d * 22) * 1.5); }
        heart.style.transform = `scale(${k})`;
      },
    };
  },
};

arrancar(SLIDES, { seam: [520, null, 760, 470] });
