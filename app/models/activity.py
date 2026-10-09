
from datetime import datetime, timezone

from app import db


class Activity(db.Model):
    __tablename__ = "activities"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    activity_type = db.Column(db.String(100), nullable=True)
    location = db.Column(db.String(200), nullable=True)
    activity_date = db.Column(db.Date, nullable=False, index=True)
    photo_filename = db.Column(db.String(255), nullable=True)
    is_published = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    def __repr__(self):
        return f"<Activity {self.title}>"
