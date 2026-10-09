
from app import create_app, db
from app import models

app = create_app()

with app.app_context():
    db.create_all()
    print("Database tables created successfully.")

    for table_name in sorted(db.metadata.tables):
        print(f"- {table_name}")
