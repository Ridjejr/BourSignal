from flask import Blueprint, request, jsonify
from app.services.watchlist_service import WatchlistService
from app.utils.session_helper import get_session_id

watchlist_bp = Blueprint("watchlist", __name__)


@watchlist_bp.route("/watchlist")
def voir_watchlist():
    """GET /api/watchlist — Voir la watchlist."""
    session_id = get_session_id()
    items = WatchlistService.lister(session_id)
    count = WatchlistService.compter(session_id)
    return jsonify({"watchlist": items, "count": count}), 200


@watchlist_bp.route("/watchlist", methods=["POST"])
def ajouter_watchlist():
    """POST /api/watchlist — Ajouter un actif."""
    data = request.get_json()
    if not data or "ticker" not in data:
        return jsonify({"error": "Le ticker est requis."}), 400

    session_id = get_session_id()
    response = WatchlistService.ajouter(session_id, data["ticker"])

    if "error" in response:
        return jsonify(response), 400
    return jsonify(response), 201


@watchlist_bp.route("/watchlist/<ticker>", methods=["DELETE"])
def retirer_watchlist(ticker):
    """DELETE /api/watchlist/AAPL — Retirer un actif."""
    session_id = get_session_id()
    response = WatchlistService.retirer(session_id, ticker)

    if "error" in response:
        return jsonify(response), 404
    return jsonify(response), 200