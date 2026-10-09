import os

from flask import (
    Blueprint, abort, current_app, render_template, send_from_directory
)
from flask_login import current_user

from app.content import sanitize_description
from app.models.activity import Activity
from app.models.activity_attachment import ActivityAttachment
from app.models.user import User

public_bp = Blueprint("public", __name__)


@public_bp.route("/")
def index():
    return render_template("index.html")


@public_bp.route("/organization")
def organization():
    return render_template("organization.html")


@public_bp.route("/plans")
def plans():
    return render_template("plans.html")


@public_bp.route("/accomplishments")
def accomplishments():
    return render_template("accomplishments.html")


@public_bp.route("/inventory")
def inventory():
    return render_template("inventory.html")


@public_bp.route("/activities")
def activities():
    published_activities = (
        Activity.query.filter_by(is_published=True)
        .order_by(Activity.activity_date.desc(), Activity.id.desc())
        .all()
    )
    for activity in published_activities:
        activity.safe_description = sanitize_description(activity.description)

    published_ids = [activity.id for activity in published_activities]
    attachments = (
        ActivityAttachment.query.filter(
            ActivityAttachment.activity_id.in_(published_ids)
        ).order_by(ActivityAttachment.id.asc()).all()
        if published_ids else []
    )
    attachments_by_activity = {}
    for item in attachments:
        attachments_by_activity.setdefault(item.activity_id, []).append(item)

    return render_template(
        "activities.html",
        activities=published_activities,
        attachments_by_activity=attachments_by_activity,
    )


@public_bp.route("/activity-attachments/<int:attachment_id>")
def activity_attachment(attachment_id):
    attachment = ActivityAttachment.query.get_or_404(attachment_id)
    activity = Activity.query.get_or_404(attachment.activity_id)

    staff_access = (
        current_user.is_authenticated
        and current_user.has_role(User.ROLE_ADMIN, User.ROLE_EDITOR)
    )
    if not activity.is_published and not staff_access:
        abort(404)

    # Use only the server-generated stored filename, never the submitted name.
    response = send_from_directory(
        current_app.config["UPLOAD_FOLDER"],
        attachment.stored_filename,
        mimetype=attachment.mime_type,
        as_attachment=attachment.media_type == "document",
        download_name=attachment.original_filename,
        conditional=True,
    )
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Content-Security-Policy"] = "default-src 'none'; sandbox"
    return response
