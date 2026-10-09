# tests/test_staff.py

import re
import unittest

from app import create_app, db
from app.models.user import User


class StaffManagementTests(unittest.TestCase):
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

            db.session.add_all([admin, editor])
            db.session.commit()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
            db.session.remove()
            db.engine.dispose()

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

    def login(self, username):
        token = self.get_csrf_token()

        return self.client.post(
            "/login",
            data={
                "csrf_token": token,
                "username": username,
                "password": "test-password-123",
            },
        )

    def test_anonymous_user_cannot_view_staff(self):
        response = self.client.get("/admin/staff")

        self.assertEqual(response.status_code, 302)
        self.assertIn("/login", response.headers["Location"])

    def test_editor_cannot_view_staff(self):
        self.login("test_editor")

        response = self.client.get("/admin/staff")
        self.assertEqual(response.status_code, 403)

    def test_admin_can_view_staff(self):
        self.login("test_admin")

        response = self.client.get("/admin/staff")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Staff Management", response.data)

    def test_admin_can_create_editor(self):
        self.login("test_admin")
        token = self.get_csrf_token("/admin/staff")

        response = self.client.post(
            "/admin/staff",
            data={
                "csrf_token": token,
                "username": "new_editor",
                "password": "new-editor-password",
                "role": User.ROLE_EDITOR,
            },
        )

        self.assertEqual(response.status_code, 302)

        with self.app.app_context():
            created = User.query.filter_by(
                username="new_editor"
            ).first()

            self.assertIsNotNone(created)
            self.assertEqual(created.role, User.ROLE_EDITOR)
            self.assertTrue(
                created.check_password("new-editor-password")
            )

    def test_staff_creation_rejects_missing_csrf_token(self):
        self.login("test_admin")

        response = self.client.post(
            "/admin/staff",
            data={
                "username": "forged_editor",
                "password": "new-editor-password",
                "role": User.ROLE_EDITOR,
            },
        )

        self.assertEqual(response.status_code, 400)

        with self.app.app_context():
            created = User.query.filter_by(
                username="forged_editor"
            ).first()
            self.assertIsNone(created)

    def test_duplicate_username_is_rejected(self):
        self.login("test_admin")
        token = self.get_csrf_token("/admin/staff")

        response = self.client.post(
            "/admin/staff",
            data={
                "csrf_token": token,
                "username": "test_editor",
                "password": "new-editor-password",
                "role": User.ROLE_EDITOR,
            },
        )

        self.assertEqual(response.status_code, 409)

    def test_invalid_role_is_rejected(self):
        self.login("test_admin")
        token = self.get_csrf_token("/admin/staff")

        response = self.client.post(
            "/admin/staff",
            data={
                "csrf_token": token,
                "username": "invalid_role_user",
                "password": "new-editor-password",
                "role": "superuser",
            },
        )

        self.assertEqual(response.status_code, 400)

    def test_short_password_is_rejected(self):
        self.login("test_admin")
        token = self.get_csrf_token("/admin/staff")

        response = self.client.post(
            "/admin/staff",
            data={
                "csrf_token": token,
                "username": "short_password_user",
                "password": "short",
                "role": User.ROLE_EDITOR,
            },
        )

        self.assertEqual(response.status_code, 400)


if __name__ == "__main__":
    unittest.main()
