import requests
from flask import current_app


class FinnhubService:
    """Gère tous les appels vers l'API Finnhub."""

    @staticmethod
    def get_profil(ticker):
        """
        Récupère le profil d'un actif (nom, secteur, pays...).
        Endpoint Finnhub : /stock/profile2?symbol=AAPL
        """
        api_key = current_app.config.get("FINNHUB_API_KEY")
        base_url = current_app.config.get("FINNHUB_BASE_URL")

        try:
            response = requests.get(
                f"{base_url}/stock/profile2",
                params={"symbol": ticker.upper(), "token": api_key},
                timeout=10,
            )
            response.raise_for_status()
            data = response.json()

            # Finnhub renvoie {} si le ticker n'existe pas
            if not data or "name" not in data:
                return None

            return {
                "ticker": data.get("ticker", ticker.upper()),
                "nom": data.get("name", ""),
                "type": "ETF" if not data.get("finnhubIndustry") else "ACTION",
                "devise": data.get("currency", "USD"),
                "pays": data.get("country", ""),
                "secteur": data.get("finnhubIndustry", ""),
                "exchange": data.get("exchange", ""),
            }

        except requests.RequestException as e:
            current_app.logger.error(f"Erreur Finnhub profil {ticker}: {e}")
            return None

    @staticmethod
    def get_cotation(ticker):
        """
        Récupère le prix en temps réel d'un actif.
        Endpoint Finnhub : /quote?symbol=AAPL

        Réponse Finnhub :
        c = current price, o = open, h = high, l = low,
        pc = previous close, d = change, dp = percent change
        """
        api_key = current_app.config.get("FINNHUB_API_KEY")
        base_url = current_app.config.get("FINNHUB_BASE_URL")

        try:
            response = requests.get(
                f"{base_url}/quote",
                params={"symbol": ticker.upper(), "token": api_key},
                timeout=10,
            )
            response.raise_for_status()
            data = response.json()

            # Finnhub renvoie c=0 si le ticker n'existe pas
            if not data or data.get("c", 0) == 0:
                return None

            return {
                "prix_actuel": data.get("c", 0),
                "ouverture": data.get("o", 0),
                "plus_haut": data.get("h", 0),
                "plus_bas": data.get("l", 0),
                "cloture_precedente": data.get("pc", 0),
                "variation": data.get("d", 0),
                "variation_pourcent": data.get("dp", 0),
                "volume": 0,
            }

        except requests.RequestException as e:
            current_app.logger.error(f"Erreur Finnhub cotation {ticker}: {e}")
            return None
        
    
    @staticmethod
    def rechercher_symbole(query):
        """
        Recherche un actif par nom ou ticker.
        Endpoint Finnhub : /search?q=apple
        Retourne une liste de résultats [{ticker, nom}, ...]
        """
        api_key = current_app.config.get("FINNHUB_API_KEY")
        base_url = current_app.config.get("FINNHUB_BASE_URL")

        try:
            response = requests.get(
                f"{base_url}/search",
                params={"q": query, "token": api_key},
                timeout=10,
            )
            response.raise_for_status()
            data = response.json()

            if not data or "result" not in data:
                return []

            resultats = []
            for item in data["result"][:10]:
                resultats.append({
                    "ticker": item.get("symbol", ""),
                    "nom": item.get("description", ""),
                    "type": item.get("type", ""),
                })
            return resultats

        except requests.RequestException as e:
            current_app.logger.error(f"Erreur Finnhub search {query}: {e}")
            return []