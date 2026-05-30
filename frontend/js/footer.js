// Footer commun à toutes les pages — défini une seule fois ici.
// S'injecte automatiquement en bas du <body>. Année mise à jour dynamiquement.
(function () {
  const annee = new Date().getFullYear();

  const footer = document.createElement("footer");
  footer.className = "border-t border-border bg-bg-surface mt-16";
  footer.innerHTML = `
    <div class="max-w-6xl mx-auto px-6 md:px-12 py-12">
      <div class="grid grid-cols-1 md:grid-cols-3 gap-10 mb-10">
        <!-- Marque -->
        <div>
          <a href="index.html" class="flex items-center gap-2.5 mb-3">
            <svg width="24" height="20" viewBox="0 0 27 22" fill="none" class="overflow-visible">
              <polyline points="1,18 7.5,18 7.5,12 14,12 14,7 20.5,7 20.5,2.5 26,2.5"
                stroke="#A78BFA" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"></polyline>
              <circle cx="26" cy="2.5" r="2.6" fill="#A78BFA"></circle>
            </svg>
            <span class="font-mono font-bold text-base tracking-tight"><span class="text-text-1">BOUR</span><span class="text-accent">SIGNAL</span></span>
          </a>
          <p class="text-text-3 text-sm max-w-[230px] leading-relaxed">
            Surveillez vos actifs et soyez alerté dès qu'un seuil de prix est franchi.
          </p>
        </div>

        <!-- Navigation -->
        <div>
          <p class="text-text-2 text-xs font-semibold uppercase tracking-[0.14em] mb-4">Navigation</p>
          <ul class="space-y-2.5 text-sm">
            <li><a href="index.html" class="text-text-2 hover:text-text-1 transition">Accueil</a></li>
            <li><a href="watchlist.html" class="text-text-2 hover:text-text-1 transition">Watchlist</a></li>
            <li><a href="alertes.html" class="text-text-2 hover:text-text-1 transition">Alertes</a></li>
          </ul>
        </div>

        <!-- Légal -->
        <div>
          <p class="text-text-2 text-xs font-semibold uppercase tracking-[0.14em] mb-4">Légal</p>
          <ul class="space-y-2.5 text-sm">
            <li><a href="#" class="text-text-2 hover:text-text-1 transition">Mentions légales</a></li>
            <li><a href="#" class="text-text-2 hover:text-text-1 transition">Politique de confidentialité</a></li>
            <li><a href="#" class="text-text-2 hover:text-text-1 transition">Conditions d'utilisation</a></li>
          </ul>
        </div>
      </div>

      <!-- Avertissement financier -->
      <p class="text-text-3 text-xs leading-relaxed border-t border-border/60 pt-6 max-w-3xl">
        Les informations affichées sur BourSignal sont fournies à titre indicatif et ne
        constituent pas un conseil en investissement. Les cours peuvent être différés.
        BourSignal décline toute responsabilité quant aux décisions d'investissement prises
        sur la base de ces données.
      </p>

      <!-- Bas de page -->
      <div class="flex flex-col sm:flex-row items-center justify-between gap-3 mt-6 pt-6 border-t border-border/60">
        <p class="text-text-3 text-xs">&copy; ${annee} BourSignal. Tous droits réservés.</p>
        <p class="text-text-3 text-xs">Ce site utilise un cookie de session strictement nécessaire.</p>
      </div>
    </div>
  `;

  document.body.appendChild(footer);
})();
