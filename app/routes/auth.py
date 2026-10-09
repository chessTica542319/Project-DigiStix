from urllib.parse import urlsplit

from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import current_user, login_user, logout_user

from app.models.user import User


auth_bp = Blueprint("auth", __name__)


def is_safe_next_url(target):
    """Allow only local absolute paths as post-login destinations."""
    if not target or not target.startswith("/"):
        return False

    if target.startswith("//") or "\\" in target:
        return False

    parsed = urlsplit(target)

    return not parsed.scheme and not parsed.netloc


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("admin.dashboard"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password) and user.is_active:
            login_user(user)

            next_page = request.args.get("next")

            if is_safe_next_url(next_page):
                return redirect(next_page)

            return redirect(url_for("admin.dashboard"))

        flash("Invalid username or password.", "error")

    return render_template("admin/login.html")


@auth_bp.route("/logout", methods=["POST"])
def logout():
    if current_user.is_authenticated:
        logout_user()
        flash("You have been logged out.", "success")

    return redirect(url_for("public.index"))
