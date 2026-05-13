from flask import Blueprint, jsonify

# Un Blueprint c'est un "groupe de routes"
# Toutes les routes ici commenceront par /api
api = Blueprint("api", __name__, url_prefix="/api")


@api.route("/health")
def health():
    return jsonify({
        "status": "UP",
        "service": "boursignal-api"
    })
