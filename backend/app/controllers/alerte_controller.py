from flask import Blueprint, jsonify, request

from app.services.alerte_service import AlerteService
from app.utils.session_helper import get_session_id

alerte_bp = Blueprint("alertes", __name__)


@alerte_bp.route("/alertes")
def lister_alertes():
    """GET /api/alertes — Lister les alertes."""
    session_id = get_session_id()
    alertes = AlerteService.lister(session_id)
    return jsonify({"alertes": alertes}), 200


@alerte_bp.route("/alertes", methods=["POST"])
def creer_alerte():
    """POST /api/alertes — Créer une alerte."""
    data = request.get_json()
    if not data:
        return jsonify({"error": "Données manquantes."}), 400

    champs_requis = ["ticker", "condition", "prix_cible", "email"]
    for champ in champs_requis:
        if champ not in data:
            return jsonify({"error": f"Le champ '{champ}' est requis."}), 400

    session_id = get_session_id()
    response = AlerteService.creer(
        session_id=session_id,
        ticker=data["ticker"],
        condition=data["condition"],
        prix_cible=data["prix_cible"],
        email=data["email"],
    )

    if "error" in response:
        return jsonify(response), 400
    return jsonify(response), 201


@alerte_bp.route("/alertes/<int:alerte_id>/acces", methods=["POST"])
def acceder_alerte(alerte_id):
    """POST /api/alertes/1/acces — Récupérer une alerte via son code.

    Corps attendu : { "code": "..." }
    Permet d'afficher l'alerte depuis n'importe quel navigateur (lien email).
    """
    data = request.get_json()
    code = (data or {}).get("code")
    if not code:
        return jsonify({"error": "Le code de gestion est requis."}), 400

    response = AlerteService.acceder(alerte_id, code)

    if "error" in response:
        return jsonify(response), 403
    return jsonify(response), 200


@alerte_bp.route("/alertes/<int:alerte_id>", methods=["PATCH"])
def changer_etat_alerte(alerte_id):
    """PATCH /api/alertes/1 — Suspendre / réactiver / annuler une alerte.

    Corps attendu : { "action": "suspendre|reactiver|annuler", "code": "..." }
    L'autorisation repose sur le code de gestion, pas sur la session.
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "Données manquantes."}), 400

    action = data.get("action")
    code = data.get("code")

    actions_valides = ["suspendre", "reactiver", "annuler"]
    if action not in actions_valides:
        return jsonify({"error": "Action invalide."}), 400
    if not code:
        return jsonify({"error": "Le code de gestion est requis."}), 400

    response = AlerteService.changer_etat(alerte_id, action, code)

    if "error" in response:
        return jsonify(response), 400
    return jsonify(response), 200
