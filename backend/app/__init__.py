from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from config.settings import Config

db = SQLAlchemy()


def create_app():
    """Crée et configure l'application Flask."""

    # 1. Créer l'app
    app = Flask(__name__)

    # 2. Charger la configuration
    app.config.from_object(Config)

    # 3. Connecter la base de données
    db.init_app(app)
    CORS(app, supports_credentials=True)

    # 4. Enregistrer les routes
    from app.controllers import api
    from app.controllers.actif_controller import actif_bp
    from app.controllers.watchlist_controller import watchlist_bp
    from app.controllers.alerte_controller import alerte_bp
    app.register_blueprint(api)
    app.register_blueprint(actif_bp, url_prefix="/api")
    app.register_blueprint(watchlist_bp, url_prefix="/api")
    app.register_blueprint(alerte_bp, url_prefix="/api")

    # 5. Créer les tables dans MySQL
    with app.app_context():
        from app.models.actif import Actif
        from app.models.cotation import Cotation
        from app.models.watchlist import Watchlist
        from app.models.alerte import Alerte
        from app.models.historique import Historique
        db.create_all()

    return app 