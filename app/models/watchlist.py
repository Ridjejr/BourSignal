from datetime import datetime, timezone
from app import db


class Watchlist(db.Model):
    """Table 'watchlists' — les actifs surveillés par l'utilisateur."""

    __tablename__ = "watchlists"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    session_id = db.Column(db.String(255), nullable=False, index=True)
    ticker = db.Column(
        db.String(10),
        db.ForeignKey("actifs.ticker", ondelete="CASCADE"),
        nullable=False,
    )
    date_ajout = db.Column(
        db.DateTime, default=lambda: datetime.now(timezone.utc)
    )

    # Un même actif ne peut pas apparaître 2 fois dans la même watchlist
    __table_args__ = (
        db.UniqueConstraint("session_id", "ticker", name="uq_session_ticker"),
    )

    def to_dict(self):
        return {
            "id": self.id,
            "ticker": self.ticker,
            "date_ajout": self.date_ajout.isoformat() if self.date_ajout else None,
        }