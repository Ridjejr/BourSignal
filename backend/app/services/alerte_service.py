import re
import secrets

from flask import current_app
from werkzeug.security import check_password_hash, generate_password_hash

from app import db
from app.models.alerte import Alerte
from app.services.email_service import EmailService


def _construire_email_creation(alerte, code, lien):
    """Construit le corps HTML du mail envoyé à la création d'une alerte."""
    return f"""
    <div style="font-family: sans-serif; max-width: 480px;">
      <h2>BourSignal — Alerte créée ✅</h2>
      <p>Ton alerte a bien été enregistrée :</p>
      <ul>
        <li><b>Actif :</b> {alerte.ticker}</li>
        <li><b>Condition :</b> {alerte.condition} {float(alerte.prix_cible)} $</li>
      </ul>
      <p><b>Ton code de gestion :</b></p>
      <p style="font-size: 18px; font-family: monospace; background:#f2f2f2;
                padding: 10px 14px; border-radius: 6px;">{code}</p>
      <p>Ce code est ta preuve d'appartenance. Garde-le : il permet de
         suspendre, réactiver ou annuler cette alerte depuis n'importe où,
         sans compte.</p>
      <p>
        <a href="{lien}"
           style="display:inline-block; background:#f5a623; color:#111;
                  text-decoration:none; padding:10px 18px; border-radius:6px;
                  font-weight:bold;">Gérer mon alerte</a>
      </p>
      <p style="color:#888; font-size:12px;">Ou copie ce lien : {lien}</p>
    </div>
    """

# Transitions d'état autorisées : état courant -> {action: état cible}.
# CANCELLED est absent en clé : c'est un état terminal.
TRANSITIONS = {
    Alerte.STATUS_ACTIVE: {
        "suspendre": Alerte.STATUS_SUSPENDED,
        "annuler": Alerte.STATUS_CANCELLED,
    },
    Alerte.STATUS_SUSPENDED: {
        "reactiver": Alerte.STATUS_ACTIVE,
        "annuler": Alerte.STATUS_CANCELLED,
    },
}


class AlerteService:

    @staticmethod
    def _generer_code():
        """Génère un code de gestion unique, lisible et URL-safe."""
        return secrets.token_urlsafe(9)

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

        # Génération du code de gestion : montré une seule fois, stocké hashé.
        code = AlerteService._generer_code()

        # Création
        alerte = Alerte(
            session_id=session_id,
            ticker=ticker,
            condition=condition,
            prix_cible=prix_cible,
            email=email,
            code_hash=generate_password_hash(code),
        )
        db.session.add(alerte)
        db.session.commit()

        # Envoi du mail (code + lien de gestion). Un échec d'envoi ne doit
        # PAS faire échouer la création : on logue et on continue.
        try:
            lien = (
                f"{current_app.config['FRONTEND_URL']}"
                f"/gerer-alerte.html?id={alerte.id}&code={code}"
            )
            EmailService.envoyer(
                destinataire=email,
                sujet=f"BourSignal — Alerte créée sur {ticker}",
                corps_html=_construire_email_creation(alerte, code, lien),
            )
        except Exception as exc:  # noqa: BLE001
            current_app.logger.error(
                "Échec de l'envoi du mail pour l'alerte %s : %s", alerte.id, exc
            )

        return {
            "success": f"Alerte créée sur {ticker} ({condition} {prix_cible})",
            "alerte": alerte.to_dict(),
            # Code en clair renvoyé UNE SEULE FOIS : preuve d'appartenance.
            "code_gestion": code,
        }

    @staticmethod
    def acceder(alerte_id, code):
        """Récupère une alerte via son id + code de gestion.

        Permet d'afficher l'alerte depuis n'importe quel navigateur
        (ex. lien reçu par email), sans dépendre de la session.
        """
        alerte = Alerte.query.filter_by(id=alerte_id).first()
        if not alerte:
            return {"error": "Cette alerte n'existe pas."}

        if not code or not check_password_hash(alerte.code_hash, code):
            return {"error": "Code de gestion invalide."}

        return {"alerte": alerte.to_dict()}

    @staticmethod
    def changer_etat(alerte_id, action, code):
        """Applique une transition d'état (suspendre/reactiver/annuler).

        Autorisée uniquement par le bon code de gestion — indépendamment
        de la session, ce qui règle le cas du PC partagé.
        """
        alerte = Alerte.query.filter_by(id=alerte_id).first()
        if not alerte:
            return {"error": "Cette alerte n'existe pas."}

        # Le code est la preuve d'appartenance.
        if not code or not check_password_hash(alerte.code_hash, code):
            return {"error": "Code de gestion invalide."}

        # La transition demandée est-elle permise depuis l'état courant ?
        transitions = TRANSITIONS.get(alerte.status, {})
        if action not in transitions:
            return {
                "error": (
                    f"Action '{action}' impossible depuis l'état "
                    f"'{alerte.status}'."
                )
            }

        alerte.status = transitions[action]
        db.session.commit()

        return {"success": "Alerte mise à jour.", "alerte": alerte.to_dict()}

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
