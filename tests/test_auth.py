# tests/test_auth.py

import re
import unittest

from app import create_app, db
from app.models.user import User


class AuthenticationTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app({
            "TESTING": True,
            "SECRET_KEY": "test-only-secret",
            "SQLALCHEMY_DATABASE_URI": "sqlite://",
        })

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

    def get_csrf_token(self, path="/login"):
        response = self.client.get(path)
        self.assertEqual(response.status_code, 200)

        match = re.search(
            rb'name="csrf_token"\s+value="([^"]+)"',
            response.data,
        )
        self.assertIsNotNone(
            match,
            f"No CSRF token found on {path}",
        )
        return match.group(1).decode()

    def login(self, username, password="test-password-123"):
        token = self.get_csrf_token()

        return self.client.post(
            "/login",
            data={
                "csrf_token": token,
                "username": username,
                "password": password,
            },
        )

    def test_anonymous_user_redirected_to_login(self):
        response = self.client.get("/admin/")

        self.assertEqual(response.status_code, 302)
        self.assertIn("/login", response.headers["Location"])

    def test_admin_can_access_dashboard(self):
        response = self.login("test_admin")
        self.assertEqual(response.status_code, 302)

        response = self.client.get("/admin/")
        self.assertEqual(response.status_code, 200)

    def test_editor_can_access_dashboard(self):
        response = self.login("test_editor")
        self.assertEqual(response.status_code, 302)

        response = self.client.get("/admin/")
        self.assertEqual(response.status_code, 200)

    def test_inactive_user_cannot_log_in(self):
        response = self.login("test_inactive")
        self.assertEqual(response.status_code, 200)

        response = self.client.get("/admin/")
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login", response.headers["Location"])

    def test_invalid_password_is_rejected(self):
        response = self.login(
            "test_admin",
            password="wrong-password",
        )
        self.assertEqual(response.status_code, 200)

        response = self.client.get("/admin/")
        self.assertEqual(response.status_code, 302)

    def test_login_rejects_missing_csrf_token(self):
        response = self.client.post(
            "/login",
            data={
                "username": "test_admin",
                "password": "test-password-123",
            },
        )

        self.assertEqual(response.status_code, 400)


if __name__ == "__main__":
    unittest.main()
