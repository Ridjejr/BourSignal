from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

from config.settings import Config

db = SQLAlchemy()


def create_app(config_object=Config):
    """Crée et configure l'application Flask."""

    # 1. Créer l'app
    app = Flask(__name__)

    # 2. Charger la configuration
    app.config.from_object(config_object)

    # 3. Connecter la base de données
    db.init_app(app)
    CORS(app, supports_credentials=True)

    # 4. Enregistrer les routes
    from app.controllers import api
    from app.controllers.actif_controller import actif_bp
    from app.controllers.alerte_controller import alerte_bp
    from app.controllers.watchlist_controller import watchlist_bp
    app.register_blueprint(api)
    app.register_blueprint(actif_bp, url_prefix="/api")
    app.register_blueprint(watchlist_bp, url_prefix="/api")
    app.register_blueprint(alerte_bp, url_prefix="/api")

    # 5. Créer les tables (imports nécessaires pour la découverte SQLAlchemy)
    with app.app_context():
        from app.models import actif, alerte, cotation, historique, watchlist  # noqa: F401
        db.create_all()

    return app
