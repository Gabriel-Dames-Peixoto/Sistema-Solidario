const API_BASE = "http://127.0.0.1:8000";

const api = {
  login: `${API_BASE}/api/auth/login`,
  dashboard: `${API_BASE}/api/dashboard`,
  users: `${API_BASE}/api/users`,
  items: `${API_BASE}/api/items`,
  requests: `${API_BASE}/api/requests`,
  matches: `${API_BASE}/api/matches`,
  reportPdf: `${API_BASE}/api/reports/export.pdf`,
  reportXlsx: `${API_BASE}/api/reports/export.xlsx`,
};

const session = {
  token: localStorage.getItem("solidario_token") || "",
  user: JSON.parse(localStorage.getItem("solidario_user") || "null"),
};

function $(id) {
  return document.getElementById(id);
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;");
}

async function fetchJson(url) {
  const response = await fetch(url);
  if (!response.ok) {
    throw new Error(`Erro ao carregar ${url}`);
  }
  return response.json();
}

async function sendJson(url, method, payload, needsAuth = false) {
  const headers = { "Content-Type": "application/json" };
  if (needsAuth && session.token) {
    headers.Authorization = `Bearer ${session.token}`;
  }

  const response = await fetch(url, {
    method,
    headers,
    body: JSON.stringify(payload),
  });

  const data = await response.json();
  if (!response.ok) {
    throw new Error(data.error || "Falha na requisicao.");
  }
  return data;
}

function metricCard(label, value) {
  return `
    <article class="metric">
      <span>${escapeHtml(label)}</span>
      <strong>${escapeHtml(value)}</strong>
    </article>
  `;
}

function renderList(target, items, renderer, emptyLabel) {
  const root = $(target);
  if (!items.length) {
    root.innerHTML = `<div class="list-card">${escapeHtml(emptyLabel)}</div>`;
    return;
  }
  root.innerHTML = items.map(renderer).join("");
}

function setActionStatus(message, tone = "default") {
  const box = $("actionStatus");
  box.textContent = message;
  box.style.background =
    tone === "error" ? "rgba(191, 40, 40, 0.12)" : "rgba(33, 88, 63, 0.08)";
  box.style.color = tone === "error" ? "#8c1f1f" : "";
}

function updateAuthStatus() {
  const box = $("authStatus");
  if (!session.user) {
    box.textContent = "Nenhum usuario autenticado.";
    return;
  }
  box.textContent = `${session.user.name} autenticado como ${session.user.role}.`;
}

function syncExportLinks() {
  $("pdfLink").href = api.reportPdf;
  $("xlsxLink").href = api.reportXlsx;
}

function buildQuery() {
  const params = new URLSearchParams();
  const region = $("regionFilter").value.trim();
  const maxDistance = $("distanceFilter").value.trim();

  if (region) params.set("region", region);
  if (maxDistance) params.set("max_distance", maxDistance);

  return params.toString() ? `?${params.toString()}` : "";
}

async function loadData() {
  const query = buildQuery();

  const [dashboard, users, items, requests, matches] = await Promise.all([
    fetchJson(api.dashboard + query),
    fetchJson(api.users + query),
    fetchJson(api.items + query),
    fetchJson(api.requests + query),
    fetchJson(api.matches + query),
  ]);

  const dashboardData = dashboard.data;
  $("dashboard").innerHTML = [
    metricCard("Usuarios cadastrados", dashboardData.total_users),
    metricCard("Itens registrados", dashboardData.total_items),
    metricCard("Itens disponiveis", dashboardData.available_items),
    metricCard("Itens entregues", dashboardData.delivered_items),
    metricCard("Solicitacoes abertas", dashboardData.open_requests),
    metricCard("Beneficiarios atendidos", dashboardData.beneficiaries_served),
    metricCard("Matches sugeridos", dashboardData.total_matches),
  ].join("");

  renderList(
    "usersList",
    users.data,
    (user) => `
      <article class="list-card">
        <strong>${escapeHtml(user.name)}</strong>
        <div>${escapeHtml(user.email)}</div>
        <div>Perfil: ${escapeHtml(user.role)}</div>
        <div>Coordenadas: (${escapeHtml(user.x)}, ${escapeHtml(user.y)})</div>
        <span class="pill">${escapeHtml(user.region)}</span>
      </article>
    `,
    "Nenhum usuario encontrado."
  );

  renderList(
    "itemsList",
    items.data,
    (item) => `
      <article class="list-card">
        <strong>${escapeHtml(item.title)}</strong>
        <div>Categoria: ${escapeHtml(item.category)}</div>
        <div>Quantidade: ${escapeHtml(item.quantity)}</div>
        <div>Coordenadas: (${escapeHtml(item.x)}, ${escapeHtml(item.y)})</div>
        <span class="pill">${escapeHtml(item.status)} - ${escapeHtml(item.region)}</span>
      </article>
    `,
    "Nenhum item encontrado."
  );

  renderList(
    "requestsList",
    requests.data,
    (request) => `
      <article class="list-card">
        <strong>${escapeHtml(request.category)}</strong>
        <div>${escapeHtml(request.description)}</div>
        <div>Quantidade necessaria: ${escapeHtml(request.needed_quantity)}</div>
        <div>Coordenadas: (${escapeHtml(request.x)}, ${escapeHtml(request.y)})</div>
        <span class="pill">${escapeHtml(request.status)} - ${escapeHtml(request.region)}</span>
      </article>
    `,
    "Nenhuma solicitacao encontrada."
  );

  renderList(
    "matchesList",
    matches.data,
    (match) => `
      <article class="list-card">
        <strong>Item ${escapeHtml(match.item_id)} x Solicitacao ${escapeHtml(match.request_id)}</strong>
        <div>Categoria: ${escapeHtml(match.category)}</div>
        <div>Quantidade alocada: ${escapeHtml(match.allocated_quantity)}</div>
        <div>Distancia estimada: ${escapeHtml(match.distance)}</div>
        <span class="pill">Score ${escapeHtml(match.score)}</span>
      </article>
    `,
    "Nenhum casamento sugerido."
  );
}

$("loginForm").addEventListener("submit", async (event) => {
  event.preventDefault();
  const form = new FormData(event.currentTarget);

  try {
    const data = await sendJson(api.login, "POST", {
      email: form.get("email"),
      password: form.get("password"),
    });
    session.token = data.token;
    session.user = data.user;
    localStorage.setItem("solidario_token", data.token);
    localStorage.setItem("solidario_user", JSON.stringify(data.user));
    updateAuthStatus();
    setActionStatus("Login realizado com sucesso.");
  } catch (error) {
    setActionStatus(error.message, "error");
  }
});

$("itemForm").addEventListener("submit", async (event) => {
  event.preventDefault();
  if (!session.user) {
    setActionStatus("Faca login antes de cadastrar um item.", "error");
    return;
  }

  const form = new FormData(event.currentTarget);
  try {
    await sendJson(
      api.items,
      "POST",
      {
        donor_id: session.user.id,
        title: form.get("title"),
        category: form.get("category"),
        quantity: Number(form.get("quantity")),
        region: form.get("region"),
        x: Number(form.get("x")),
        y: Number(form.get("y")),
      },
      true
    );
    setActionStatus("Item cadastrado com sucesso.");
    event.currentTarget.reset();
    await loadData();
  } catch (error) {
    setActionStatus(error.message, "error");
  }
});

$("requestForm").addEventListener("submit", async (event) => {
  event.preventDefault();
  if (!session.user) {
    setActionStatus("Faca login antes de registrar uma solicitacao.", "error");
    return;
  }

  const form = new FormData(event.currentTarget);
  try {
    await sendJson(
      api.requests,
      "POST",
      {
        beneficiary_id: session.user.id,
        category: form.get("category"),
        description: form.get("description"),
        needed_quantity: Number(form.get("needed_quantity")),
        region: form.get("region"),
        x: Number(form.get("x")),
        y: Number(form.get("y")),
      },
      true
    );
    setActionStatus("Solicitacao registrada com sucesso.");
    event.currentTarget.reset();
    await loadData();
  } catch (error) {
    setActionStatus(error.message, "error");
  }
});

$("statusForm").addEventListener("submit", async (event) => {
  event.preventDefault();
  if (!session.user) {
    setActionStatus("Faca login antes de atualizar status.", "error");
    return;
  }

  const form = new FormData(event.currentTarget);
  try {
    await sendJson(
      `${API_BASE}/api/items/${form.get("item_id")}/status`,
      "PATCH",
      { status: form.get("status") },
      true
    );
    setActionStatus("Status do item atualizado.");
    event.currentTarget.reset();
    await loadData();
  } catch (error) {
    setActionStatus(error.message, "error");
  }
});

$("refreshDashboard").addEventListener("click", () => {
  loadData().catch((error) => {
    setActionStatus(error.message, "error");
  });
});

$("applyFilters").addEventListener("click", () => {
  loadData().catch((error) => {
    setActionStatus(error.message, "error");
  });
});

syncExportLinks();
updateAuthStatus();
loadData().catch((error) => {
  $("dashboard").innerHTML = `<div class="list-card">${escapeHtml(error.message)}</div>`;
  setActionStatus("Nao foi possivel carregar os dados da API.", "error");
});
