
from datetime import datetime, timezone

from app import db


class FoundingMember(db.Model):
    __tablename__ = "founding_members"

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(100), nullable=True)
    year_established = db.Column(db.Integer, nullable=True)
    biography = db.Column(db.Text, nullable=True)
    photo_filename = db.Column(db.String(255), nullable=True)
    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    def __repr__(self):
        return f"<FoundingMember {self.full_name}>"
