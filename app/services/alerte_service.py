import re
from app import db
from app.models.alerte import Alerte
from app.models.historique import Historique
from app.services.finnhub_service import FinnhubService


class AlerteService:

    @staticmethod
    def creer(session_id, ticker, condition, prix_cible, email):
        """Crée une nouvelle alerte."""
        ticker = ticker.upper().strip()

        # Validation du prix
        try:
            prix_cible = float(prix_cible)
            if prix_cible <= 0:
                return {"error": "Le prix cible doit être supérieur à 0."}
        except (ValueError, TypeError):
            return {"error": "Le prix cible doit être un nombre valide."}

        # Validation de l'email
        if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email):
            return {"error": "Ce format d'email semble incorrect. Vérifie ta saisie."}

        # Validation de la condition
        conditions_valides = ["Supérieur à", "Inférieur à"]
        if condition not in conditions_valides:
            return {"error": "Condition invalide. Choisis 'Supérieur à' ou 'Inférieur à'."}

        # Création
        alerte = Alerte(
            session_id=session_id,
            ticker=ticker,
            condition=condition,
            prix_cible=prix_cible,
            email=email,
        )
        db.session.add(alerte)
        db.session.commit()

        return {
            "success": f"Alerte créée sur {ticker} ({condition} {prix_cible})",
            "alerte": alerte.to_dict(),
        }

    @staticmethod
    def supprimer(session_id, alerte_id):
        """Supprime une alerte."""
        alerte = Alerte.query.filter_by(id=alerte_id, session_id=session_id).first()

        if not alerte:
            return {"error": "Cette alerte n'existe plus ou a déjà été exécutée."}

        alerte.status = "INACTIVE"
        db.session.commit()

        return {"success": "Alerte supprimée."}

    @staticmethod
    def lister(session_id):
        """Retourne toutes les alertes d'un utilisateur."""
        alertes = (
            Alerte.query
            .filter_by(session_id=session_id)
            .order_by(Alerte.date_creation.desc())
            .all()
        )
        return [a.to_dict() for a in alertes]