import unittest

from app import create_app, db
from app.models.user import User


class AuthenticationTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config.update(
            TESTING=True,
            SECRET_KEY="test-only-secret",
            SQLALCHEMY_DATABASE_URI="sqlite://",
        )

        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

            admin = User(
                username="test_admin",
                role=User.ROLE_ADMIN,
                is_active_account=True,
            )
            admin.set_password("test-password-123")

            editor = User(
                username="test_editor",
                role=User.ROLE_EDITOR,
                is_active_account=True,
            )
            editor.set_password("test-password-123")

            inactive = User(
                username="test_inactive",
                role=User.ROLE_EDITOR,
                is_active_account=False,
            )
            inactive.set_password("test-password-123")

            db.session.add_all([admin, editor, inactive])
            db.session.commit()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
            db.session.remove()

    def test_anonymous_user_redirected_to_login(self):
        response = self.client.get("/admin/")

        self.assertEqual(response.status_code, 302)
        self.assertIn("/login", response.headers["Location"])

    def test_admin_can_access_dashboard(self):
        response = self.client.post(
            "/login",
            data={
                "username": "test_admin",
                "password": "test-password-123",
            },
        )

        self.assertEqual(response.status_code, 302)

        response = self.client.get("/admin/")
        self.assertEqual(response.status_code, 200)

    def test_editor_can_access_dashboard(self):
        self.client.post(
            "/login",
            data={
                "username": "test_editor",
                "password": "test-password-123",
            },
        )

        response = self.client.get("/admin/")
        self.assertEqual(response.status_code, 200)

    def test_inactive_user_cannot_log_in(self):
        response = self.client.post(
            "/login",
            data={
                "username": "test_inactive",
                "password": "test-password-123",
            },
        )

        self.assertEqual(response.status_code, 200)

        response = self.client.get("/admin/")
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login", response.headers["Location"])

    def test_invalid_password_is_rejected(self):
        response = self.client.post(
            "/login",
            data={
                "username": "test_admin",
                "password": "wrong-password",
            },
        )

        self.assertEqual(response.status_code, 200)

        response = self.client.get("/admin/")
        self.assertEqual(response.status_code, 302)


if __name__ == "__main__":
    unittest.main()
