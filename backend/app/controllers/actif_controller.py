from flask import Blueprint, jsonify, request

from app.services.actif_service import ActifService

actif_bp = Blueprint("actifs", __name__)


@actif_bp.route("/actifs/search")
def rechercher_actif():
    """GET /api/actifs/search?q=AAPL ou ?q=Apple"""
    query = request.args.get("q", "").strip()

    if not query:
        return jsonify({"error": "Il manque un symbole par ici !"}), 400

    data = ActifService.rechercher(query)
    if not data:
        return jsonify({"error": "Oups, il semblerait que cet actif n'existe pas sur les marchés."}), 404

    return jsonify(data), 200


@actif_bp.route("/actifs/<ticker>")
def consulter_details(ticker):
    """GET /api/actifs/AAPL"""
    if not ticker or not ticker.strip():
        return jsonify({"error": "Il manque un symbole par ici !"}), 400

    data = ActifService.rechercher(ticker)
    if not data:
        return jsonify({"error": "Es-tu sûr du symbole ? Nous ne le trouvons pas."}), 404

    return jsonify(data), 200
