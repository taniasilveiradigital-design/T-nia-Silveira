// Portal FIBRA · áreas bloqueadas por produto (Revenda, Marca do Zero, Combo) + Imersão
(function () {
  const C = window.APP_CONFIG || {};
  const $ = (s, r) => (r || document).querySelector(s);
  const esc = s => String(s == null ? "" : s).replace(/[&<>"]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
  const show = (el, on) => { if (el) el.hidden = !on; };
  const dia = d => d ? new Date(d).toLocaleDateString("pt-PT", { day: "2-digit", month: "long", year: "numeric" }) : "—";
  const SITE = location.origin + location.pathname.replace(/index\.html$/, "");
  const NOMES = { revenda: "Revenda", "marca-zero": "Marca do Zero", combo: "Experiência" };

  if (!window.supabase || !C.SUPABASE_URL) {
    $("#loading").innerHTML = '<div class="auth-card"><h2>Falta configurar</h2><p>Preenche o ficheiro <b>config.js</b>.</p></div>';
    return;
  }
  const sb = window.supabase.createClient(C.SUPABASE_URL, C.SUPABASE_ANON_KEY);

  const codigoUrl = (new URLSearchParams(location.search).get("c") || "").trim();
  let me = { email: "", isAdmin: false, isAluna: false };
  let acessos = [];
  let cfg = { marcacao_link: "" };
  let tab = "areas";

  const tem = p => acessos.some(a => a.produto === p && new Date(a.expira_em) > new Date());
  const desbloqueada = {
    imersao: () => me.isAdmin || me.isAluna,
    revenda: () => me.isAdmin || tem("revenda") || tem("combo"),
    zero: () => me.isAdmin || tem("marca-zero") || tem("combo"),
    combo: () => me.isAdmin || tem("combo")
  };

  // ---------- Entrada ----------
  function showAuth(modo) {
    show($("#loading"), false); show($("#app"), false); show($("#auth"), true);
    const ativar = modo === "ativar";
    show($("#entrarForm"), !ativar); show($("#ativarForm"), ativar); show($("#novaPassForm"), false);
    $("#swEntrar").setAttribute("aria-selected", String(!ativar));
    $("#swAtivar").setAttribute("aria-selected", String(ativar));
  }
  $("#swEntrar").onclick = () => showAuth("entrar");
  $("#swAtivar").onclick = () => showAuth("ativar");
  if (codigoUrl) $("#aCod").value = codigoUrl;

  $("#entrarForm").onsubmit = async e => {
    e.preventDefault();
    const msg = $("#entrarMsg"); msg.textContent = "";
    const { error } = await sb.auth.signInWithPassword({ email: $("#eEmail").value.trim(), password: $("#ePass").value });
    if (error) { msg.textContent = "Email ou password incorretos."; return; }
    await abrir();
  };
  $("#forgotBtn").onclick = async () => {
    const msg = $("#entrarMsg"), email = $("#eEmail").value.trim();
    if (!email) { msg.textContent = "Escreve primeiro o teu email."; return; }
    await sb.auth.resetPasswordForEmail(email, { redirectTo: SITE });
    msg.textContent = "Se este email tiver conta, vais receber um link para escolher uma nova password.";
  };
  $("#novaPassForm").onsubmit = async e => {
    e.preventDefault();
    const msg = $("#novaPassMsg");
    const { error } = await sb.auth.updateUser({ password: $("#nPass").value });
    if (error) { msg.textContent = "Não foi possível guardar. Tenta outra password (mínimo 8 caracteres)."; return; }
    await abrir();
  };

  async function chamarAtivar(corpo) {
    const { data, error } = await sb.functions.invoke("ativar-acesso", { body: corpo });
    if (error) {
      let m = "Não foi possível ativar. Tenta outra vez.";
      try { const j = await error.context.json(); if (j && j.erro) m = j.erro; } catch (_) {}
      return { erro: m };
    }
    return data || {};
  }

  $("#ativarForm").onsubmit = async e => {
    e.preventDefault();
    const msg = $("#ativarMsg"); msg.textContent = "A ativar…";
    const email = $("#aEmail").value.trim(), password = $("#aPass").value, codigo = $("#aCod").value.trim();
    if (password.length < 8) { msg.textContent = "A password tem de ter pelo menos 8 caracteres."; return; }
    const r = await chamarAtivar({ email, password, codigo });
    if (r.erro) { msg.textContent = r.erro; return; }
    if (r.contaExistente) {
      msg.textContent = "Já tinhas conta com este email. O acesso foi acrescentado: entra com a tua password habitual.";
      $("#eEmail").value = email; setTimeout(() => showAuth("entrar"), 2500); return;
    }
    const { error } = await sb.auth.signInWithPassword({ email, password });
    if (error) { msg.textContent = "Conta criada. Entra com o teu email e password."; showAuth("entrar"); return; }
    history.replaceState(null, "", location.pathname);
    await abrir();
  };

  $("#logoutBtn").onclick = async () => { await sb.auth.signOut(); location.href = location.pathname; };
  $("#ativarOutro").onclick = async () => {
    const c = (prompt("Cola aqui o código do produto que compraste (vem no link que recebeste, depois de «?c=»).") || "").trim();
    if (!c) return;
    const r = await chamarAtivar({ codigo: c });
    if (r.erro) { alert(r.erro); return; }
    await abrir();
  };

  // ---------- Dados ----------
  async function abrir() {
    const { data: { session } } = await sb.auth.getSession();
    if (!session) { showAuth(codigoUrl ? "ativar" : "entrar"); return; }
    me.email = (session.user.email || "").toLowerCase();

    // Se entrou com sessão e há código no link, acrescenta o acesso.
    if (codigoUrl) {
      const r = await chamarAtivar({ codigo: codigoUrl });
      history.replaceState(null, "", location.pathname);
      if (r.erro) alert(r.erro);
    }

    const [adm, alu, ace, conf] = await Promise.all([
      sb.from("admins").select("email"),
      sb.from("alunas").select("email").eq("email", me.email),
      sb.from("acessos").select("*").order("criado_em", { ascending: false }),
      sb.from("portal_config").select("marcacao_link").eq("id", 1).maybeSingle()
    ]);
    me.isAdmin = !!(adm.data && adm.data.length);
    me.isAluna = !!(alu.data && alu.data.length);
    acessos = ace.data || [];
    cfg = conf.data || { marcacao_link: "" };

    $("#whoEmail").textContent = me.email;
    $$(".tab.admin").forEach(b => show(b, me.isAdmin));
    show($("#loading"), false); show($("#auth"), false); show($("#app"), true);
    tab = "areas"; desenhar();
  }
  const $$ = (s, r) => Array.from((r || document).querySelectorAll(s));

  $$("#tabs .tab").forEach(b => b.onclick = () => { tab = b.dataset.tab; desenhar(); });

  function desenhar() {
    $$("#tabs .tab").forEach(b => b.setAttribute("aria-selected", String(b.dataset.tab === tab)));
    if (tab === "acessos") return desenharAcessos();
    if (tab === "experiencia") return desenharExperiencia();
    desenharAreas();
  }

  // ---------- As minhas áreas ----------
  function botaoDesbloquear(k) {
    const l = (C.LINKS_VENDA || {})[k];
    return l ? '<a class="btn ghost" href="' + esc(l) + '" target="_blank" rel="noopener">Desbloquear</a>' : "";
  }
  function validade(p) {
    const a = acessos.filter(x => (x.produto === p || x.produto === "combo") && lower(x.email) === me.email)
      .sort((x, y) => new Date(y.expira_em) - new Date(x.expira_em))[0];
    return a ? '<span class="tag ok">Acesso até ' + dia(a.expira_em) + "</span>" : "";
  }
  const lower = s => String(s || "").toLowerCase();

  let filtro = "todos", busca = "";
  const norm = x => String(x || "").normalize("NFD").replace(/[̀-ͯ]/g, "").toLowerCase();

  function desenharAreas() {
    const comboAcesso = acessos.find(a => a.produto === "combo" && lower(a.email) === me.email);
    const horaUsada = comboAcesso && comboAcesso.hora_usada;
    const A = [
      { k: "imersao", nome: "Imersão FIBRA | Black Friday", img: "img/ia-decides.png", titulo: "Imersão FIBRA",
        txt: "A gravação da aula, o painel de prompts, o exemplo e os materiais em PDF, para decidires a tua Black Friday com dados.",
        on: desbloqueada.imersao(), href: C.IMERSAO_URL || "#", ext: true, cta: "Abrir a Imersão", val: "" },
      { k: "revenda", nome: "Fornecedores | Revenda", img: "img/stock.png", titulo: "Revenda",
        txt: "Contactos de fornecedores de roupa pronta, mais embalagem, para a tua loja.",
        on: desbloqueada.revenda(), href: "catalogo.html?p=revenda", cta: "Abrir a lista", val: validade("revenda") },
      { k: "marca-zero", nome: "Fornecedores | Marca do Zero", img: "img/capa.png", titulo: "Marca do Zero",
        txt: "Confeção, tecidos e malhas, acessórios, bordados e estampados para criares a tua coleção.",
        on: desbloqueada.zero(), href: "catalogo.html?p=zero", cta: "Abrir a lista", val: validade("marca-zero") },
      { k: "combo", nome: "Experiência | Marca do Zero + Revenda + 1 hora comigo", img: "img/oferta.png", titulo: "Experiência",
        txt: "As duas listas de fornecedores e uma hora comigo para decidirmos o que faz sentido para o teu negócio.",
        on: desbloqueada.combo(), href: "#experiencia", cta: "Entrar na Experiência", val: validade("combo") }
    ];
    const vis = A.filter(a => (filtro === "todos" || (filtro === "on" ? a.on : !a.on)) &&
      (!busca || norm(a.nome + " " + a.txt).includes(norm(busca))));
    const cartao = a => {
      const capa = '<img src="' + a.img + '" alt="">' + (a.on ? "" : '<span class="lk" aria-label="Bloqueado">🔒</span>') + '<span class="tit">' + esc(a.titulo) + "</span>";
      const cover = a.on && a.href
        ? '<a class="cover" href="' + esc(a.href) + '"' + (a.ext ? ' target="_blank" rel="noopener"' : "") + ">" + capa + "</a>"
        : '<div class="cover">' + capa + "</div>";
      const acao = a.on
        ? (a.href ? '<a class="btn" href="' + esc(a.href) + '"' + (a.ext ? ' target="_blank" rel="noopener"' : "") + ">" + esc(a.cta) + "</a>" : "")
        : botaoDesbloquear(a.k);
      return '<article class="pc' + (a.on ? "" : " locked") + '">' + cover + "<h3>" + esc(a.nome) + "</h3><p>" + esc(a.txt) + "</p>" +
        '<div class="meta">' + (a.on ? a.val : '<span class="tag">Bloqueado</span>') + acao + "</div>" + (a.on && a.extra ? a.extra : "") + "</article>";
    };
    const chip = (f, t) => '<button class="chip" data-f="' + f + '" aria-pressed="' + (filtro === f) + '">' + t + "</button>";
    $("#view").innerHTML = '<div class="chips">' + chip("todos", "Início") + chip("on", "Disponíveis") + chip("off", "Bloqueados") + "</div>" +
      '<div class="sec-h"><h2>Conteúdos</h2></div>' +
      (vis.length ? '<div class="cards">' + vis.map(cartao).join("") + "</div>" : '<p class="empty-c">Nada encontrado.</p>');
    $$("[data-f]").forEach(c => c.onclick = () => { filtro = c.dataset.f; desenharAreas(); });
    $$("a[href=\"#experiencia\"]").forEach(a => a.onclick = e => { e.preventDefault(); tab = "experiencia"; desenhar(); window.scrollTo(0, 0); });
  }

  // ---------- Experiência: as duas listas + marcar a hora ----------
  function desenharExperiencia() {
    const comboAcesso = acessos.find(a => a.produto === "combo" && lower(a.email) === me.email);
    const horaUsada = comboAcesso && comboAcesso.hora_usada;
    $("#view").innerHTML =
      '<a class="pvoltar" href="#" id="expVoltar">← Voltar aos conteúdos</a>' +
      '<div class="sec-h"><h2>Experiência</h2></div>' +
      '<p class="small muted">Marca do Zero + Revenda + 1 hora comigo. Tens aqui as duas listas de fornecedores e a marcação da tua hora.</p>' +
      '<div class="cards">' +
      '<article class="pc"><a class="cover" href="catalogo.html?p=zero"><img src="img/capa.png" alt=""><span class="tit">Marca do Zero</span></a><h3>Fornecedores | Marca do Zero</h3><p>Confeção, tecidos e malhas, acessórios, bordados e estampados para criares a tua coleção.</p><div class="meta"><a class="btn" href="catalogo.html?p=zero">Abrir a lista</a></div></article>' +
      '<article class="pc"><a class="cover" href="catalogo.html?p=revenda"><img src="img/stock.png" alt=""><span class="tit">Revenda</span></a><h3>Fornecedores | Revenda</h3><p>Contactos de fornecedores de roupa pronta, mais embalagem, para a tua loja.</p><div class="meta"><a class="btn" href="catalogo.html?p=revenda">Abrir a lista</a></div></article>' +
      '</div>' +
      '<div class="sec-h" style="margin-top:26px"><h2>A tua hora comigo</h2></div>' + comboHTML(horaUsada);
    $("#expVoltar").onclick = e => { e.preventDefault(); tab = "areas"; desenhar(); };
  }
  function comboHTML(horaUsada) {
    if (horaUsada) return '<div class="hora-box">A tua hora comigo já foi usada. Obrigada!</div>';
    const l = cfg.marcacao_link;
    if (!l) return '<div class="hora-box">A tua hora está incluída. Em breve vais ter aqui o botão para marcares o dia e a hora.</div>';
    return '<div class="hora-box">A tua hora está incluída. Escolhe o dia e a hora que te servem.<br><br><a class="btn" href="' + esc(l) + '" target="_blank" rel="noopener">Marcar a minha hora</a></div>';
  }

  // ---------- Administradora ----------
  async function desenharAcessos() {
    const [ace, cod] = await Promise.all([
      sb.from("acessos").select("*").order("criado_em", { ascending: false }),
      sb.from("codigos_acesso").select("*").order("produto")
    ]);
    const A = ace.data || [], K = cod.data || [];
    const linhas = A.map(a =>
      "<tr><td>" + esc(a.email) + "</td><td>" + esc(NOMES[a.produto] || a.produto) + "</td><td>" + dia(a.criado_em) + "</td><td>" + dia(a.expira_em) + "</td>" +
      "<td>" + (a.produto === "combo" ? '<input type="checkbox" data-hora="' + a.id + '"' + (a.hora_usada ? " checked" : "") + ' aria-label="Hora usada">' : "") + "</td>" +
      '<td><button class="btn ghost small" data-del="' + a.id + '">Retirar</button></td></tr>').join("");
    const cods = K.map(k =>
      "<tr><td>" + esc(NOMES[k.produto]) + "</td><td><code class=\"l\">" + esc(SITE + "?c=" + k.codigo) + "</code></td>" +
      "<td>" + (k.ativo ? "Ativo" : "Desativado") + "</td>" +
      '<td><button class="btn ghost small" data-copy="' + esc(SITE + "?c=" + k.codigo) + '">Copiar link</button> ' +
      '<button class="btn ghost small" data-ativo="' + esc(k.codigo) + '" data-val="' + (k.ativo ? "0" : "1") + '">' + (k.ativo ? "Desativar" : "Ativar") + "</button></td></tr>").join("");
    $("#view").innerHTML =
      '<div class="card"><h2>Hora da Experiência</h2><p class="small muted">O link da tua página de marcações (por exemplo do Google Calendar). Só quem tem a Experiência o vê, dentro da área Experiência.</p>' +
      '<div class="row"><div><label class="f" for="marc">Link de marcação</label><input type="url" id="marc" value="' + esc(cfg.marcacao_link) + '" placeholder="https://calendar.app.google/…"></div><button class="btn" id="marcSave" type="button">Guardar</button></div><div class="msg" id="marcMsg"></div></div>' +
      '<div class="card"><h2>Links para o Sales Park</h2><p class="small muted">Cada produto manda ao comprador o seu link. Se um link circular fora das compras, desativa-o e cria um novo código na base de dados.</p>' +
      '<div class="tbl-wrap"><table class="tbl"><thead><tr><th>Produto</th><th>Link</th><th>Estado</th><th></th></tr></thead><tbody>' + cods + "</tbody></table></div></div>" +
      '<div class="card"><h2>Acessos (' + A.length + ')</h2>' +
      '<div class="tbl-wrap"><table class="tbl"><thead><tr><th>Email</th><th>Produto</th><th>Desde</th><th>Até</th><th>Hora usada</th><th></th></tr></thead><tbody>' + (linhas || '<tr><td colspan="6" class="muted">Ainda ninguém.</td></tr>') + "</tbody></table></div>" +
      '<h3 style="margin-top:22px">Dar acesso à mão</h3><div class="row"><div><label class="f" for="nEmail">Email</label><input type="email" id="nEmail"></div>' +
      '<div><label class="f" for="nProd">Produto</label><select id="nProd"><option value="revenda">Revenda</option><option value="marca-zero">Marca do Zero</option><option value="combo">Experiência</option></select></div>' +
      '<button class="btn" id="nAdd" type="button">Dar acesso</button></div><div class="msg" id="nMsg"></div></div>';

    $("#marcSave").onclick = async () => {
      const v = $("#marc").value.trim();
      const { error } = await sb.from("portal_config").update({ marcacao_link: v }).eq("id", 1);
      $("#marcMsg").textContent = error ? "Não foi possível guardar." : "Guardado.";
      if (!error) cfg.marcacao_link = v;
    };
    $$("[data-hora]").forEach(c => c.onchange = async () => {
      await sb.from("acessos").update({ hora_usada: c.checked }).eq("id", c.dataset.hora);
    });
    $$("[data-del]").forEach(b => b.onclick = async () => {
      if (!confirm("Retirar este acesso?")) return;
      await sb.from("acessos").delete().eq("id", b.dataset.del); desenharAcessos();
    });
    $$("[data-copy]").forEach(b => b.onclick = async () => {
      try { await navigator.clipboard.writeText(b.dataset.copy); b.textContent = "Copiado"; } catch (_) { prompt("Copia o link:", b.dataset.copy); }
    });
    $$("[data-ativo]").forEach(b => b.onclick = async () => {
      await sb.from("codigos_acesso").update({ ativo: b.dataset.val === "1" }).eq("codigo", b.dataset.ativo); desenharAcessos();
    });
    $("#nAdd").onclick = async () => {
      const email = $("#nEmail").value.trim().toLowerCase();
      if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) { $("#nMsg").textContent = "Email inválido."; return; }
      const { error } = await sb.from("acessos").upsert({ email, produto: $("#nProd").value, origem: "manual" }, { onConflict: "email,produto" });
      if (error) { $("#nMsg").textContent = "Não foi possível dar acesso."; return; }
      desenharAcessos();
    };
  }

  $("#q").oninput = e => { busca = e.target.value; if (tab !== "areas") { tab = "areas"; } desenhar(); };
  $("#burger").onclick = () => $("#side").classList.toggle("open");
  $("#side").addEventListener("click", e => { if (e.target.closest(".side-item")) $("#side").classList.remove("open"); });

  // ---------- Arranque ----------
  sb.auth.onAuthStateChange((ev) => {
    if (ev === "PASSWORD_RECOVERY") {
      show($("#loading"), false); show($("#app"), false); show($("#auth"), true);
      show($("#entrarForm"), false); show($("#ativarForm"), false); show($("#novaPassForm"), true);
    }
  });
  abrir();
})();
