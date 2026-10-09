
from datetime import datetime, timezone

from app import db


class TargetPlan(db.Model):
    __tablename__ = "target_plans"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    target_year = db.Column(db.Integer, nullable=False, index=True)
    target_date = db.Column(db.Date, nullable=True)
    status = db.Column(db.String(30), nullable=False, default="planned")
    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    def __repr__(self):
        return f"<TargetPlan {self.title} ({self.target_year})>"
