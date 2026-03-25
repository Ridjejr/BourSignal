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
  const symboleVariation = isHausse ? "▲" : "▼";

  const carte = document.createElement("div");
  carte.id = `carte-${actif.ticker}`;
  carte.className =
    "bg-bg-card border border-border rounded-lg p-5 cursor-pointer hover:border-accent transition";
  carte.onclick = () =>
    (window.location.href = `details.html?ticker=${actif.ticker}`);
  carte.innerHTML = `
        <div class="flex justify-between items-start mb-3">
            <div>
                <span class="font-mono font-bold text-text-1">${actif.ticker}</span>
                <span class="text-xs bg-bg-surface text-text-2 px-2 py-0.5 rounded ml-2">${actif.type}</span>
            </div>
        </div>
        <p class="text-text-2 text-sm mb-3">${actif.nom}</p>
        <div class="flex items-end justify-between">
            <div>
                <span class="font-mono text-2xl font-bold text-text-1">${cotation ? cotation.prix_actuel.toFixed(2) : "N/A"}</span>
                <span class="text-text-2 text-sm ml-1">${actif.devise}</span>
            </div>
            <span class="${couleurVariation} text-sm font-mono">
                ${symboleVariation} ${variation >= 0 ? "+" : ""}${variation.toFixed(2)}%
            </span>
        </div>
        <div class="flex gap-2 mt-4">
            <button onclick="event.stopPropagation(); ajouterWatchlist('${actif.ticker}')" class="text-xs bg-accent text-bg-deep font-semibold px-3 py-1.5 rounded hover:opacity-90">
                + Watchlist
            </button>
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
}

// Charger les actifs populaires au démarrage
chargerActifsPopulaires();
