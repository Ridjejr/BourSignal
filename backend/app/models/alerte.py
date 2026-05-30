from datetime import UTC, datetime

from app import db


class Alerte(db.Model):
    """Table 'alertes' — surveillance de seuil de prix."""

    __tablename__ = "alertes"

    # États possibles d'une alerte (machine à états).
    # CANCELLED est terminal : aucune transition n'en sort.
    STATUS_ACTIVE = "ACTIVE"
    STATUS_SUSPENDED = "SUSPENDED"
    STATUS_CANCELLED = "CANCELLED"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    session_id = db.Column(db.String(255), nullable=False, index=True)
    ticker = db.Column(
        db.String(10),
        db.ForeignKey("actifs.ticker", ondelete="CASCADE"),
        nullable=False,
    )
    condition = db.Column(db.String(20), nullable=False)
    prix_cible = db.Column(db.Numeric(12, 2), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(20), default=STATUS_ACTIVE, index=True)
    # Hash du code de gestion : preuve d'appartenance rattachée à l'alerte.
    # Le code en clair n'est montré qu'une fois, à la création.
    code_hash = db.Column(db.String(255), nullable=False)
    date_creation = db.Column(
        db.DateTime, default=lambda: datetime.now(UTC)
    )
    date_declenchement = db.Column(db.DateTime, nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "ticker": self.ticker,
            "condition": self.condition,
            "prix_cible": float(self.prix_cible) if self.prix_cible else 0,
            "email": self.email,
            "status": self.status,
            "date_creation": self.date_creation.isoformat() if self.date_creation else None,
            "date_declenchement": self.date_declenchement.isoformat() if self.date_declenchement else None,
        }
