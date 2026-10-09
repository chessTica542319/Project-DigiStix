
from datetime import datetime, timezone

from app import db


class Officer(db.Model):
    __tablename__ = "officers"

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(150), nullable=False)
    position = db.Column(db.String(100), nullable=False)
    academic_year = db.Column(db.String(20), nullable=False)
    photo_filename = db.Column(db.String(255), nullable=True)
    biography = db.Column(db.Text, nullable=True)
    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    def __repr__(self):
        return f"<Officer {self.full_name} - {self.position}>"
