const api = {
  dashboard: "/api/dashboard",
  items: "/api/items",
  requests: "/api/requests",
  matches: "/api/matches",
};

async function fetchJson(url) {
  const response = await fetch(url);
  if (!response.ok) {
    throw new Error(`Erro ao carregar ${url}`);
  }
  return response.json();
}

function metricCard(label, value) {
  return `<article class="metric"><span>${label}</span><strong>${value}</strong></article>`;
}

function renderList(target, items, renderer, emptyLabel) {
  const root = document.getElementById(target);
  if (!items.length) {
    root.innerHTML = `<div class="list-card">${emptyLabel}</div>`;
    return;
  }
  root.innerHTML = items.map(renderer).join("");
}

async function loadData() {
  const region = document.getElementById("regionFilter").value;
  const maxDistance = document.getElementById("distanceFilter").value;
  const query = new URLSearchParams();
  if (region) query.set("region", region);
  if (maxDistance) query.set("max_distance", maxDistance);

  const [dashboard, items, requests, matches] = await Promise.all([
    fetchJson(api.dashboard + (query.toString() ? `?${query}` : "")),
    fetchJson(api.items + (query.toString() ? `?${query}` : "")),
    fetchJson(api.requests + (query.toString() ? `?${query}` : "")),
    fetchJson(api.matches + (query.toString() ? `?${query}` : "")),
  ]);

  const dashboardData = dashboard.data;
  document.getElementById("dashboard").innerHTML = [
    metricCard("Usuarios", dashboardData.total_users),
    metricCard("Itens", dashboardData.total_items),
    metricCard("Disponiveis", dashboardData.available_items),
    metricCard("Entregues", dashboardData.delivered_items),
    metricCard("Solicitacoes abertas", dashboardData.open_requests),
    metricCard("Beneficiarios atendidos", dashboardData.beneficiaries_served),
    metricCard("Matches", dashboardData.total_matches),
  ].join("");

  renderList(
    "itemsList",
    items.data,
    (item) => `
      <article class="list-card">
        <strong>${item.title}</strong>
        <div>Categoria: ${item.category}</div>
        <div>Quantidade: ${item.quantity}</div>
        <div>Coordenadas: (${item.x}, ${item.y})</div>
        <span class="pill">${item.status} - ${item.region}</span>
      </article>
    `,
    "Nenhum item encontrado."
  );

  renderList(
    "requestsList",
    requests.data,
    (request) => `
      <article class="list-card">
        <strong>${request.category}</strong>
        <div>${request.description}</div>
        <div>Quantidade necessaria: ${request.needed_quantity}</div>
        <div>Coordenadas: (${request.x}, ${request.y})</div>
        <span class="pill">${request.status} - ${request.region}</span>
      </article>
    `,
    "Nenhuma solicitacao encontrada."
  );

  renderList(
    "matchesList",
    matches.data,
    (match) => `
      <article class="list-card">
        <strong>Item ${match.item_id} x Solicitacao ${match.request_id}</strong>
        <div>Categoria: ${match.category}</div>
        <div>Quantidade alocada: ${match.allocated_quantity}</div>
        <div>Distancia estimada: ${match.distance}</div>
        <span class="pill">Score ${match.score}</span>
      </article>
    `,
    "Nenhum casamento sugerido."
  );
}

document.getElementById("refreshDashboard").addEventListener("click", loadData);
document.getElementById("applyFilters").addEventListener("click", loadData);

loadData().catch((error) => {
  console.error(error);
  document.getElementById("dashboard").innerHTML = `<div class="list-card">Nao foi possivel carregar os dados da API.</div>`;
});

