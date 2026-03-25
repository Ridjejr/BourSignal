from datetime import datetime, timezone
from app import db


class Actif(db.Model):
    """Table 'actifs' — une action ou un ETF (AAPL, SPY, MSFT...)"""

    __tablename__ = "actifs"

    ticker = db.Column(db.String(10), primary_key=True)
    nom = db.Column(db.String(255), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    devise = db.Column(db.String(10), default="USD")
    pays = db.Column(db.String(100), default="")
    secteur = db.Column(db.String(100), default="")
    exchange = db.Column(db.String(50), default="")
    date_creation = db.Column(
        db.DateTime, default=lambda: datetime.now(timezone.utc)
    )

    # Relations
    cotation = db.relationship("Cotation", backref="actif", uselist=False, cascade="all, delete-orphan")
    watchlists = db.relationship("Watchlist", backref="actif", cascade="all, delete-orphan")
    alertes = db.relationship("Alerte", backref="actif", cascade="all, delete-orphan")

    def to_dict(self):
        """Transforme l'objet en dictionnaire pour les réponses JSON."""
        return {
            "ticker": self.ticker,
            "nom": self.nom,
            "type": self.type,
            "devise": self.devise,
            "pays": self.pays,
            "secteur": self.secteur,
            "exchange": self.exchange,
            "date_creation": self.date_creation.isoformat() if self.date_creation else None,
        }