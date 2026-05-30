// Bandeau ticker de la navbar — branché sur de vraies cotations.
//
// Structure d'un item (réutilisable) :
//   <div class="ticker-item" data-ticker="AAPL">
//     <span class="ticker-symbol">AAPL</span>
//     <span class="ticker-price">213.55</span>
//     <span class="ticker-change up|down">▲ +1.24%</span>
//   </div>
function majNavTicker(data) {
  const container = document.getElementById("nav-ticker");
  if (!container || !Array.isArray(data)) return;

  container.innerHTML = data
    .map((d) => {
      const hausse = d.variation_pourcent >= 0;
      const dir = hausse ? "up" : "down";
      const fleche = hausse ? "▲" : "▼";
      const signe = hausse ? "+" : "";
      return `<div class="ticker-item" data-ticker="${d.ticker}">
        <span class="ticker-symbol">${d.ticker}</span>
        <span class="ticker-price">${Number(d.prix).toFixed(2)}</span>
        <span class="ticker-change ${dir}">${fleche} ${signe}${Number(d.variation_pourcent).toFixed(2)}%</span>
      </div>`;
    })
    .join("");
}

// Mise à jour ciblée d'un seul actif déjà présent (par data-ticker).
function majNavTickerItem(ticker, prix, variation_pourcent) {
  const item = document.querySelector(
    `#nav-ticker .ticker-item[data-ticker="${ticker}"]`,
  );
  if (!item) return;
  const hausse = variation_pourcent >= 0;
  item.querySelector(".ticker-price").textContent = Number(prix).toFixed(2);
  const change = item.querySelector(".ticker-change");
  change.className = `ticker-change ${hausse ? "up" : "down"}`;
  change.textContent = `${hausse ? "▲" : "▼"} ${hausse ? "+" : ""}${Number(variation_pourcent).toFixed(2)}%`;
}

// Récupère les VRAIES cotations des symboles affichés dans le bandeau,
// puis met à jour le ticker. Si le backend est injoignable, on garde les
// valeurs statiques déjà présentes dans le HTML (repli silencieux).
async function chargerNavTicker() {
  const container = document.getElementById("nav-ticker");
  if (!container) return;

  // Symboles actuellement présents dans le HTML (data-ticker).
  const symboles = [...container.querySelectorAll(".ticker-item")]
    .map((el) => el.dataset.ticker)
    .filter(Boolean);
  if (symboles.length === 0) return;

  try {
    const resultats = await Promise.all(
      symboles.map(async (ticker) => {
        const res = await fetch(`/api/actifs/search?q=${ticker}`, {
          credentials: "include",
        });
        if (!res.ok) return null;
        const data = await res.json();
        if (!data.cotation) return null;
        return {
          ticker: data.actif.ticker,
          prix: data.cotation.prix_actuel,
          variation_pourcent: data.cotation.variation_pourcent,
        };
      }),
    );

    const valides = resultats.filter(Boolean);
    // On ne remplace que si on a récupéré de vraies données.
    if (valides.length) majNavTicker(valides);
  } catch (error) {
    console.error("Ticker navbar (backend injoignable) :", error);
  }
}

// Lancement : gère le cas où le DOM est déjà prêt (script en fin de body).
if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", chargerNavTicker);
} else {
  chargerNavTicker();
}
