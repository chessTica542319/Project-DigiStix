
from datetime import datetime, timezone

from app import db


class Inventory(db.Model):
    __tablename__ = "inventory"

    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(150), nullable=False)
    category = db.Column(db.String(100), nullable=True)
    description = db.Column(db.Text, nullable=True)
    quantity = db.Column(db.Integer, nullable=False, default=0)
    condition = db.Column(db.String(50), nullable=True)
    reporting_year = db.Column(db.Integer, nullable=False, index=True)
    unit_cost = db.Column(db.Numeric(12, 2), nullable=True)
    remarks = db.Column(db.Text, nullable=True)
    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    def __repr__(self):
        return f"<Inventory {self.item_name} x{self.quantity}>"
