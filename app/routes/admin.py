from flask import (
    Blueprint,
    abort,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import current_user

from app import db
from app.models.user import User
from app.security import roles_required


admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/")
@roles_required(User.ROLE_ADMIN, User.ROLE_EDITOR)
def dashboard():
    return render_template("admin/dashboard.html")


@admin_bp.route("/staff", methods=["GET", "POST"])
@roles_required(User.ROLE_ADMIN)
def staff():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        role = request.form.get("role", User.ROLE_EDITOR).strip()

        if not username or len(username) > 80:
            abort(400, description="Username must be between 1 and 80 characters.")

        if role not in User.VALID_ROLES:
            abort(400, description="Invalid staff role.")

        if len(password) < 12:
            abort(400, description="Password must contain at least 12 characters.")

        if User.query.filter_by(username=username).first():
            abort(409, description="Username already exists.")

        staff_user = User(
            username=username,
            role=role,
            is_active_account=True,
        )
        staff_user.set_password(password)

        try:
            db.session.add(staff_user)
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise

        flash("Staff account created successfully.", "success")
        return redirect(url_for("admin.staff"))

    users = User.query.order_by(User.username.asc()).all()
    return render_template("admin/staff.html", users=users)
