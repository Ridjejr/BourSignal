from flask import Blueprint, request, jsonify
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


@alerte_bp.route("/alertes/<int:alerte_id>", methods=["DELETE"])
def supprimer_alerte(alerte_id):
    """DELETE /api/alertes/1 — Supprimer une alerte."""
    session_id = get_session_id()
    response = AlerteService.supprimer(session_id, alerte_id)

    if "error" in response:
        return jsonify(response), 404
    return jsonify(response), 200