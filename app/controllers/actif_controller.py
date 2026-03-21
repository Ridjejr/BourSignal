from flask import Blueprint, request, jsonify
from app.services.actif_service import ActifService
import re

actif_bp = Blueprint("actifs", __name__)


def valider_ticker(ticker):
    """Vérifie le format du ticker (1 à 6 lettres, pas de caractères spéciaux)."""
    if not ticker or not ticker.strip():
        return False, "Il manque un symbole par ici !"
    ticker = ticker.strip().upper()
    if not re.match(r"^[A-Z]{1,6}$", ticker):
        return False, "Les symboles boursiers ne contiennent pas de caractères spéciaux."
    return True, ticker


@actif_bp.route("/actifs/search")
def rechercher_actif():
    """
    GET /api/actifs/search?q=AAPL
    Recherche un actif par ticker.
    """
    ticker = request.args.get("q", "")

    is_valid, result = valider_ticker(ticker)
    if not is_valid:
        return jsonify({"error": result}), 400

    data = ActifService.rechercher(result)
    if not data:
        return jsonify({"error": "Oups, il semblerait que cet actif n'existe pas sur les marchés."}), 404

    return jsonify(data), 200


@actif_bp.route("/actifs/<ticker>")
def consulter_details(ticker):
    """
    GET /api/actifs/AAPL
    Consulte les détails d'un actif.
    """
    is_valid, result = valider_ticker(ticker)
    if not is_valid:
        return jsonify({"error": result}), 400

    data = ActifService.rechercher(result)
    if not data:
        return jsonify({"error": "Es-tu sûr du symbole ? Nous ne le trouvons pas."}), 404

    return jsonify(data), 200