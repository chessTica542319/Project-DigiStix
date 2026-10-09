from functools import wraps

from flask import abort
from flask_login import current_user, login_required


def roles_required(*allowed_roles):
    """Require an authenticated user with one of the specified roles."""

    def decorator(view_function):
        @wraps(view_function)
        @login_required
        def wrapped_view(*args, **kwargs):
            if not current_user.has_role(*allowed_roles):
                abort(403)

            return view_function(*args, **kwargs)

        return wrapped_view

    return decorator
