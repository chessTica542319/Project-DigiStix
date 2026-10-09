
from datetime import datetime, timezone

from app import db


class Adviser(db.Model):
    __tablename__ = "advisers"

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(150), nullable=False)
    designation = db.Column(db.String(150), nullable=True)
    academic_year = db.Column(db.String(20), nullable=False)
    photo_filename = db.Column(db.String(255), nullable=True)
    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    def __repr__(self):
        return f"<Adviser {self.full_name}>"
