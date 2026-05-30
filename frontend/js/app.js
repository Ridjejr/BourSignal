const API_URL = "/api";

async function apiFetch(url, options = {}) {
  options.credentials = "include";
  if (options.body) {
    options.headers = {
      "Content-Type": "application/json",
      ...options.headers,
    };
  }
  return fetch(url, options);
}

const searchInput = document.getElementById("search-input");
const searchBtn = document.getElementById("search-btn");
const searchError = document.getElementById("search-error");
const actifsGrid = document.getElementById("actifs-grid");

searchBtn.addEventListener("click", () => {
  rechercher();
});

searchInput.addEventListener("keypress", (e) => {
  if (e.key === "Enter") {
    rechercher();
  }
});

async function rechercher() {
  const query = searchInput.value.trim();

  if (!query) {
    afficherErreur("Il manque un symbole par ici !");
    return;
  }

  cacherErreur();
  searchBtn.textContent = "Chargement...";
  searchBtn.disabled = true;

  try {
    const response = await apiFetch(`${API_URL}/actifs/search?q=${query}`);
    const data = await response.json();

    if (!response.ok) {
      afficherErreur(data.error);
      return;
    }

    ajouterCarte(data.actif, data.cotation);
    searchInput.value = "";
  } catch (error) {
    afficherErreur(
      "Impossible de contacter le serveur. Vérifie que le backend tourne.",
    );
  } finally {
    searchBtn.textContent = "Rechercher";
    searchBtn.disabled = false;
  }
}

function ajouterCarte(actif, cotation) {
  const existante = document.getElementById(`carte-${actif.ticker}`);
  if (existante) {
    existante.remove();
  }

  const variation = cotation ? cotation.variation_pourcent : 0;
  const isHausse = variation >= 0;
  const couleurVariation = isHausse ? "text-green-400" : "text-danger";
  const bgVariation = isHausse
    ? "bg-green-400/10 border-green-400/20"
    : "bg-danger/10 border-danger/20";
  const symboleVariation = isHausse ? "▲" : "▼";

  const carte = document.createElement("div");
  carte.id = `carte-${actif.ticker}`;
  carte.className =
    "group relative bg-bg-card border border-border rounded-2xl p-5 cursor-pointer transition duration-200 hover:border-accent/40 hover:shadow-glow-accent hover:-translate-y-0.5";
  carte.onclick = () =>
    (window.location.href = `details.html?ticker=${actif.ticker}`);
  carte.innerHTML = `
        <div class="flex justify-between items-start mb-4">
            <div class="flex items-center gap-3 min-w-0">
                <div class="shrink-0 w-10 h-10 rounded-xl bg-bg-surface border border-border flex items-center justify-center font-mono font-bold text-[11px] text-text-1 transition duration-200 group-hover:border-accent/40">
                    ${actif.ticker.slice(0, 4)}
                </div>
                <div class="min-w-0">
                    <span class="font-mono font-bold text-text-1 block leading-tight">${actif.ticker}</span>
                    <span class="text-text-2 text-xs truncate block">${actif.nom}</span>
                </div>
            </div>
            <span class="shrink-0 text-[10px] uppercase tracking-wider bg-bg-surface text-text-3 border border-border px-2 py-0.5 rounded-md">${actif.type}</span>
        </div>
        <div class="flex items-end justify-between">
            <div class="flex items-baseline gap-1">
                <span class="font-mono text-2xl font-bold text-text-1">${cotation ? cotation.prix_actuel.toFixed(2) : "N/A"}</span>
                <span class="text-text-3 text-sm">${actif.devise}</span>
            </div>
            <span class="${couleurVariation} ${bgVariation} text-xs font-mono font-bold px-2 py-1 rounded-lg border">
                ${symboleVariation} ${variation >= 0 ? "+" : ""}${variation.toFixed(2)}%
            </span>
        </div>
        <div class="flex gap-2 mt-4 pt-4 border-t border-border/60">
            <button onclick="event.stopPropagation(); ajouterWatchlist('${actif.ticker}')" class="text-xs font-medium text-text-2 border border-border px-3 py-1.5 rounded-lg transition duration-200 hover:text-accent hover:border-accent/50 hover:bg-accent/5">
                + Watchlist
            </button>
            <span class="ml-auto text-text-3 text-xs flex items-center gap-1 opacity-0 group-hover:opacity-100 transition">
                Détails →
            </span>
        </div>
    `;

  actifsGrid.prepend(carte);
}

async function ajouterWatchlist(ticker) {
  try {
    const response = await apiFetch(`${API_URL}/watchlist`, {
      method: "POST",
      body: JSON.stringify({ ticker: ticker }),
    });
    const data = await response.json();

    if (data.error) {
      alert(data.error);
    } else {
      alert(data.success);
    }
  } catch (error) {
    alert("Erreur de connexion au serveur.");
  }
}

function afficherErreur(message) {
  searchError.textContent = message;
  searchError.classList.remove("hidden");
}

function cacherErreur() {
  searchError.classList.add("hidden");
}

// Actifs populaires affichés au chargement
const ACTIFS_POPULAIRES = ["AAPL", "MSFT", "NVDA", "TSLA", "SPY", "QQQ"];

async function chargerActifsPopulaires() {
  for (const ticker of ACTIFS_POPULAIRES) {
    try {
      const response = await apiFetch(`${API_URL}/actifs/search?q=${ticker}`);
      const data = await response.json();

      if (response.ok) {
        ajouterCarte(data.actif, data.cotation);
      }
    } catch (error) {
      console.error(`Erreur chargement ${ticker}:`, error);
    }
  }

  // Fallback PREVIEW uniquement : si aucune carte n'a pu être chargée
  // (backend injoignable), on affiche des données de démonstration pour
  // visualiser le design. En production ce bloc ne s'exécute jamais.
  if (actifsGrid && actifsGrid.children.length === 0) {
    DEMO_ACTIFS.forEach((d) => ajouterCarte(d.actif, d.cotation));
  }
}

// Données de démonstration (preview sans backend uniquement).
const DEMO_ACTIFS = [
  { actif: { ticker: "AAPL", nom: "Apple Inc.", type: "Action", devise: "USD" }, cotation: { prix_actuel: 213.55, variation_pourcent: 1.24 } },
  { actif: { ticker: "MSFT", nom: "Microsoft Corp.", type: "Action", devise: "USD" }, cotation: { prix_actuel: 432.18, variation_pourcent: 0.62 } },
  { actif: { ticker: "NVDA", nom: "NVIDIA Corp.", type: "Action", devise: "USD" }, cotation: { prix_actuel: 121.4, variation_pourcent: -2.13 } },
  { actif: { ticker: "TSLA", nom: "Tesla Inc.", type: "Action", devise: "USD" }, cotation: { prix_actuel: 248.9, variation_pourcent: 3.41 } },
  { actif: { ticker: "SPY", nom: "SPDR S&P 500 ETF", type: "ETF", devise: "USD" }, cotation: { prix_actuel: 533.27, variation_pourcent: 0.18 } },
  { actif: { ticker: "QQQ", nom: "Invesco QQQ Trust", type: "ETF", devise: "USD" }, cotation: { prix_actuel: 461.05, variation_pourcent: -0.74 } },
];

// Charger les actifs populaires au démarrage
chargerActifsPopulaires();
