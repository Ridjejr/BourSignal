from app import db
from app.models.watchlist import Watchlist
from app.models.actif import Actif
from app.services.actif_service import ActifService

MAX_WATCHLIST_SIZE = 10


class WatchlistService:

    @staticmethod
    def lister(session_id):
        """Retourne la watchlist de l'utilisateur avec les cotations."""
        entries = (
            Watchlist.query
            .filter_by(session_id=session_id)
            .order_by(Watchlist.date_ajout.desc())
            .all()
        )

        result = []
        for entry in entries:
            actif = Actif.query.get(entry.ticker)
            if actif:
                result.append({
                    "actif": actif.to_dict(),
                    "cotation": actif.cotation.to_dict() if actif.cotation else None,
                    "date_ajout": entry.date_ajout.isoformat() if entry.date_ajout else None,
                })
        return result

    @staticmethod
    def ajouter(session_id, ticker):
        """Ajoute un actif à la watchlist."""
        ticker = ticker.upper().strip()

        # Vérifier que l'actif existe
        actif = Actif.query.get(ticker)
        if not actif:
            resultat = ActifService.rechercher(ticker)
            if not resultat:
                return {"error": "Oups, il semblerait que cet actif n'existe pas sur les marchés."}

        # Vérifier le doublon
        existe = Watchlist.query.filter_by(session_id=session_id, ticker=ticker).first()
        if existe:
            return {"error": "Cet actif est déjà dans ta liste de surveillance !"}

        # Vérifier la limite
        count = Watchlist.query.filter_by(session_id=session_id).count()
        if count >= MAX_WATCHLIST_SIZE:
            return {"error": f"Ta liste est pleine ({MAX_WATCHLIST_SIZE} actifs max)."}

        # Ajouter
        entry = Watchlist(session_id=session_id, ticker=ticker)
        db.session.add(entry)
        db.session.commit()

        return {"success": f"{ticker} ajouté à ta watchlist !"}

    @staticmethod
    def retirer(session_id, ticker):
        """Retire un actif de la watchlist."""
        ticker = ticker.upper().strip()

        entry = Watchlist.query.filter_by(session_id=session_id, ticker=ticker).first()
        if not entry:
            return {"error": "Action impossible, cet actif ne fait pas partie de ta liste."}

        db.session.delete(entry)
        db.session.commit()

        return {"success": f"{ticker} retiré de ta watchlist."}

    @staticmethod
    def compter(session_id):
        """Retourne le nombre d'actifs dans la watchlist."""
        return Watchlist.query.filter_by(session_id=session_id).count()