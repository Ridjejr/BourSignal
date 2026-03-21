from datetime import datetime, timezone
from app import db
from app.models.actif import Actif
from app.models.cotation import Cotation
from app.services.finnhub_service import FinnhubService


class ActifService:
    """Logique métier de recherche et consultation des actifs."""

    @staticmethod
    def rechercher(ticker):
        """
        Recherche un actif par ticker.
        Si pas en base → appelle Finnhub → stocke en base.
        Gère les actions ET les ETF.
        """
        ticker = ticker.upper().strip()

        # 1. Chercher en base
        actif = Actif.query.get(ticker)

        if not actif:
            # 2. Pas en base → demander le profil à Finnhub
            profil = FinnhubService.get_profil(ticker)

            if profil:
                # C'est une action classique
                actif = Actif(
                    ticker=profil["ticker"],
                    nom=profil["nom"],
                    type=profil["type"],
                    devise=profil["devise"],
                    pays=profil["pays"],
                    secteur=profil["secteur"],
                    exchange=profil["exchange"],
                )
            else:
                # Pas de profil → vérifier si la cotation existe (ETF)
                cotation_data = FinnhubService.get_cotation(ticker)
                if not cotation_data:
                    return None  # Ni profil ni cotation → n'existe pas

                actif = Actif(
                    ticker=ticker,
                    nom=ticker,
                    type="ETF",
                    devise="USD",
                )

            db.session.add(actif)

        # 3. Mettre à jour la cotation
        cotation_data = FinnhubService.get_cotation(ticker)
        if cotation_data:
            if actif.cotation:
                for key, value in cotation_data.items():
                    setattr(actif.cotation, key, value)
                actif.cotation.date_mise_a_jour = datetime.now(timezone.utc)
            else:
                cotation = Cotation(ticker=ticker, **cotation_data)
                db.session.add(cotation)

        db.session.commit()

        actif = Actif.query.get(ticker)
        return {
            "actif": actif.to_dict(),
            "cotation": actif.cotation.to_dict() if actif.cotation else None,
        }