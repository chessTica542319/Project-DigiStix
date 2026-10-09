from getpass import getpass

from sqlalchemy.exc import IntegrityError

from app import create_app, db
from app.models.user import User


def main():
    app = create_app()

    with app.app_context():
        existing_admin = User.query.filter_by(
            role=User.ROLE_ADMIN
        ).first()

        if existing_admin:
            print("An administrator already exists.")
            print("No account was created.")
            return

        username = input("Administrator username: ").strip()

        if not username or len(username) > 80:
            print("Username must be between 1 and 80 characters.")
            return

        if User.query.filter_by(username=username).first():
            print("That username already exists.")
            return

        password = getpass("Administrator password (12+ characters): ")
        confirmation = getpass("Confirm password: ")

        if len(password) < 12:
            print("Password must contain at least 12 characters.")
            return

        if password != confirmation:
            print("Passwords do not match.")
            return

        admin = User(
            username=username,
            role=User.ROLE_ADMIN,
            is_active_account=True,
        )
        admin.set_password(password)

        try:
            db.session.add(admin)
            db.session.commit()
            print("Administrator account created successfully.")
        except IntegrityError:
            db.session.rollback()
            print("Account creation failed. The username may already exist.")

        finally:
            db.session.remove()


if __name__ == "__main__":
    main()
