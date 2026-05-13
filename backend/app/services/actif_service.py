import re
from datetime import UTC, datetime

from app import db
from app.models.actif import Actif
from app.models.cotation import Cotation
from app.services.finnhub_service import FinnhubService


class ActifService:
    """Logique métier de recherche et consultation des actifs."""

    @staticmethod
    def rechercher(query):
        query = query.strip()

        # 1. Essayer comme ticker d'abord
        if re.match(r"^[A-Za-z]{1,6}$", query):
            resultat = ActifService._rechercher_par_ticker(query.upper())
            if resultat:
                return resultat

        # 2. Si pas trouvé comme ticker, essayer comme nom
        return ActifService._rechercher_par_nom(query)

    @staticmethod
    def _rechercher_par_nom(nom):
        resultats = FinnhubService.rechercher_symbole(nom)
        if not resultats:
            return None

        for resultat in resultats:
            ticker = resultat["ticker"]
            if "." not in ticker:
                return ActifService._rechercher_par_ticker(ticker)

        return ActifService._rechercher_par_ticker(resultats[0]["ticker"])

    @staticmethod
    def _rechercher_par_ticker(ticker):
        ticker = ticker.upper().strip()

        actif = Actif.query.get(ticker)

        if not actif:
            profil = FinnhubService.get_profil(ticker)

            if profil:
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
                cotation_data = FinnhubService.get_cotation(ticker)
                if not cotation_data:
                    return None

                actif = Actif(
                    ticker=ticker,
                    nom=ticker,
                    type="ETF",
                    devise="USD",
                )

            db.session.add(actif)

        cotation_data = FinnhubService.get_cotation(ticker)
        if cotation_data:
            if actif.cotation:
                for key, value in cotation_data.items():
                    setattr(actif.cotation, key, value)
                actif.cotation.date_mise_a_jour = datetime.now(UTC)
            else:
                cotation = Cotation(ticker=ticker, **cotation_data)
                db.session.add(cotation)

        db.session.commit()

        actif = Actif.query.get(ticker)
        return {
            "actif": actif.to_dict(),
            "cotation": actif.cotation.to_dict() if actif.cotation else None,
        }
