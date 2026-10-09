
from datetime import datetime, timezone

from app import db


class Accomplishment(db.Model):
    __tablename__ = "accomplishments"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    accomplishment_year = db.Column(db.Integer, nullable=False, index=True)
    accomplishment_date = db.Column(db.Date, nullable=True)
    evidence_filename = db.Column(db.String(255), nullable=True)
    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    def __repr__(self):
        return (
            f"<Accomplishment {self.title} "
            f"({self.accomplishment_year})>"
        )
