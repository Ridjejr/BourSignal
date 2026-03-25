from datetime import datetime, timezone
from app import db


class Cotation(db.Model):
    """Table 'cotations' — le prix en temps réel d'un actif."""

    __tablename__ = "cotations"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ticker = db.Column(
        db.String(10),
        db.ForeignKey("actifs.ticker", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )
    prix_actuel = db.Column(db.Numeric(12, 2), nullable=False)
    ouverture = db.Column(db.Numeric(12, 2), default=0)
    plus_haut = db.Column(db.Numeric(12, 2), default=0)
    plus_bas = db.Column(db.Numeric(12, 2), default=0)
    cloture_precedente = db.Column(db.Numeric(12, 2), default=0)
    variation = db.Column(db.Numeric(12, 2), default=0)
    variation_pourcent = db.Column(db.Numeric(8, 2), default=0)
    volume = db.Column(db.BigInteger, default=0)
    date_mise_a_jour = db.Column(
        db.DateTime, default=lambda: datetime.now(timezone.utc)
    )

    def to_dict(self):
        return {
            "ticker": self.ticker,
            "prix_actuel": float(self.prix_actuel) if self.prix_actuel else 0,
            "ouverture": float(self.ouverture) if self.ouverture else 0,
            "plus_haut": float(self.plus_haut) if self.plus_haut else 0,
            "plus_bas": float(self.plus_bas) if self.plus_bas else 0,
            "cloture_precedente": float(self.cloture_precedente) if self.cloture_precedente else 0,
            "variation": float(self.variation) if self.variation else 0,
            "variation_pourcent": float(self.variation_pourcent) if self.variation_pourcent else 0,
            "volume": self.volume or 0,
            "date_mise_a_jour": self.date_mise_a_jour.isoformat() if self.date_mise_a_jour else None,
        }