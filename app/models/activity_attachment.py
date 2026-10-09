from datetime import datetime, timezone

from app import db


class ActivityAttachment(db.Model):
    __tablename__ = "activity_attachments"

    id = db.Column(db.Integer, primary_key=True)

    activity_id = db.Column(
        db.Integer,
        db.ForeignKey("activities.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    original_filename = db.Column(db.String(255), nullable=False)
    stored_filename = db.Column(db.String(100), nullable=False, unique=True)
    media_type = db.Column(db.String(20), nullable=False)
    mime_type = db.Column(db.String(100), nullable=False)
    file_size = db.Column(db.BigInteger, nullable=False)

    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    def __repr__(self):
        return f"<ActivityAttachment {self.id}: {self.original_filename}>"
