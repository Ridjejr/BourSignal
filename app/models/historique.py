from datetime import datetime, timezone
from app import db


class Historique(db.Model):
    """Table 'historiques' — journal des alertes déclenchées."""

    __tablename__ = "historiques"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    alerte_id = db.Column(
        db.Integer,
        db.ForeignKey("alertes.id", ondelete="CASCADE"),
        nullable=False,
    )
    prix_declenchement = db.Column(db.Numeric(12, 2), nullable=False)
    date_envoi = db.Column(
        db.DateTime, default=lambda: datetime.now(timezone.utc)
    )
    status_envoi = db.Column(db.String(20), default="ENVOYE")

    def to_dict(self):
        return {
            "id": self.id,
            "alerte_id": self.alerte_id,
            "prix_declenchement": float(self.prix_declenchement) if self.prix_declenchement else 0,
            "date_envoi": self.date_envoi.isoformat() if self.date_envoi else None,
            "status_envoi": self.status_envoi,
        }