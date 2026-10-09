import os
import uuid
from datetime import date

from flask import (
    Blueprint, abort, current_app, flash, redirect,
    render_template, request, url_for
)
from werkzeug.utils import secure_filename

from app import db
from app.content import sanitize_description
from app.models.activity import Activity
from app.models.activity_attachment import ActivityAttachment
from app.models.user import User
from app.security import roles_required

admin_bp = Blueprint("admin", __name__)

IMAGE_EXTENSIONS = {
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".gif": "image/gif",
    ".webp": "image/webp",
}
DOCUMENT_EXTENSIONS = {
    ".pdf": "application/pdf",
    ".doc": "application/msword",
    ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    ".txt": "text/plain",
}
VIDEO_EXTENSIONS = {
    ".mp4": "video/mp4",
    ".webm": "video/webm",
}
ALLOWED_FILES = {**IMAGE_EXTENSIONS, **DOCUMENT_EXTENSIONS, **VIDEO_EXTENSIONS}
MAX_IMAGE_DOCUMENT_BYTES = 10 * 1024 * 1024
MAX_VIDEO_BYTES = 100 * 1024 * 1024

def validate_attachments():
    """Validate every selected file before saving any of them."""
    uploads = []
    total_limit = current_app.config.get(
        "MAX_CONTENT_LENGTH", 110 * 1024 * 1024
    )

    for file in request.files.getlist("attachments"):
        if not file or not file.filename:
            continue

        original_name = secure_filename(file.filename)
        if not original_name:
            return None, "One uploaded file has an invalid filename."

        extension = os.path.splitext(original_name)[1].lower()
        if extension not in ALLOWED_FILES:
            return None, f"File type not allowed: {original_name}"

        stream = file.stream
        stream.seek(0, os.SEEK_END)
        size = stream.tell()
        stream.seek(0)

        limit = (
            MAX_VIDEO_BYTES
            if extension in VIDEO_EXTENSIONS
            else MAX_IMAGE_DOCUMENT_BYTES
        )
        if size <= 0 or size > limit:
            return None, f"File is empty or too large: {original_name}"

        # Check common file signatures instead of trusting the browser MIME.
        header = stream.read(16)
        stream.seek(0)

        valid = True
        if extension == ".png":
            valid = header.startswith(b"\x89PNG\r\n\x1a\n")
        elif extension in {".jpg", ".jpeg"}:
            valid = header.startswith(b"\xff\xd8\xff")
        elif extension == ".gif":
            valid = header.startswith((b"GIF87a", b"GIF89a"))
        elif extension == ".webp":
            valid = header.startswith(b"RIFF") and header[8:12] == b"WEBP"
        elif extension == ".pdf":
            valid = header.startswith(b"%PDF-")
        elif extension == ".mp4":
            valid = len(header) >= 8 and header[4:8] == b"ftyp"
        elif extension == ".webm":
            valid = header.startswith(b"\x1a\x45\xdf\xa3")
        elif extension == ".txt":
            content = stream.read(4096)
            stream.seek(0)
            valid = b"\x00" not in content

        if not valid:
            return None, f"File content does not match its extension: {original_name}"

        category = (
            "image" if extension in IMAGE_EXTENSIONS
            else "video" if extension in VIDEO_EXTENSIONS
            else "document"
        )
        uploads.append({
            "file": file,
            "original_name": original_name,
            "extension": extension,
            "size": size,
            "category": category,
            "mime_type": ALLOWED_FILES[extension],
        })

    return uploads, None


def save_attachments(activity, uploads):
    upload_dir = current_app.config["UPLOAD_FOLDER"]
    os.makedirs(upload_dir, exist_ok=True)
    saved_paths = []

    try:
        for item in uploads:
            stored_name = f"{uuid.uuid4().hex}{item['extension']}"
            destination = os.path.join(upload_dir, stored_name)
            item["file"].save(destination)
            saved_paths.append(destination)

            attachment = ActivityAttachment(
                activity_id=activity.id,
                original_filename=item["original_name"],
                stored_filename=stored_name,
                media_type=item["category"],
                mime_type=item["mime_type"],
                file_size=item["size"],
            )
            db.session.add(attachment)

        return saved_paths
    except Exception:
        for path in saved_paths:
            try:
                os.remove(path)
            except OSError:
                pass
        raise


def remove_activity_files(activity):
    """Schedule attachment records for deletion and return their file paths."""
    attachments = ActivityAttachment.query.filter_by(
        activity_id=activity.id
    ).all()
    upload_dir = current_app.config["UPLOAD_FOLDER"]
    paths = []

    for attachment in attachments:
        paths.append(os.path.join(upload_dir, attachment.stored_filename))
        db.session.delete(attachment)

    return paths


@admin_bp.route("/")
@roles_required(User.ROLE_ADMIN, User.ROLE_EDITOR)
def dashboard():
    activity_count = Activity.query.count()
    published_count = Activity.query.filter_by(is_published=True).count()
    return render_template(
        "admin/dashboard.html",
        activity_count=activity_count,
        published_count=published_count,
        draft_count=activity_count - published_count,
    )


@admin_bp.route("/staff", methods=["GET", "POST"])
@roles_required(User.ROLE_ADMIN)
def staff():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        role = request.form.get("role", User.ROLE_EDITOR).strip()

        if role != User.ROLE_EDITOR:
            abort(400, description="Only editor accounts can be created here.")
        if not username or len(username) > 80:
            abort(400, description="Username must be between 1 and 80 characters.")
        if len(password) < 12:
            abort(400, description="Password must contain at least 12 characters.")
        if User.query.filter_by(username=username).first():
            abort(409, description="Username already exists.")

        staff_user = User(
            username=username, role=role, is_active_account=True
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


@admin_bp.route("/activities")
@roles_required(User.ROLE_ADMIN, User.ROLE_EDITOR)
def activities():
    all_activities = Activity.query.order_by(
        Activity.activity_date.desc(), Activity.id.desc()
    ).all()
    attachments = ActivityAttachment.query.order_by(
        ActivityAttachment.id.asc()
    ).all()
    attachments_by_activity = {}
    for item in attachments:
        attachments_by_activity.setdefault(item.activity_id, []).append(item)

    return render_template(
        "admin/activities.html",
        activities=all_activities,
        attachments_by_activity=attachments_by_activity,
    )


def activity_form_values():
    title = request.form.get("title", "").strip()
    date_text = request.form.get("activity_date", "").strip()

    if not title or len(title) > 200:
        return None, "Title is required and must be at most 200 characters."

    try:
        parsed_date = date.fromisoformat(date_text)
    except ValueError:
        return None, "Enter a valid activity date."

    activity_type = request.form.get("activity_type", "").strip()
    location = request.form.get("location", "").strip()
    photo_filename = request.form.get("photo_filename", "").strip()

    if len(activity_type) > 100:
        return None, "Activity type must be at most 100 characters."
    if len(location) > 200:
        return None, "Location must be at most 200 characters."
    if len(photo_filename) > 255:
        return None, "Photo filename must be at most 255 characters."

    return {
        "title": title,
        "description": sanitize_description(request.form.get("description", "")) or None,
        "activity_type": activity_type or None,
        "location": location or None,
        "activity_date": parsed_date,
        "photo_filename": photo_filename or None,
    }, None


def render_activity_form(activity, page_title, status=200):
    return render_template(
        "admin/activity_form.html",
        activity=activity,
        form_data=request.form if request.method == "POST" else {},
        page_title=page_title,
        attachments=(
            ActivityAttachment.query.filter_by(activity_id=activity.id).all()
            if activity else []
        ),
    ), status


def handle_activity_form(activity=None):
    values, error = activity_form_values()
    if error:
        flash(error, "error")
        return render_activity_form(
            activity, "Edit Activity" if activity else "Create Activity", 400
        )

    uploads, upload_error = validate_attachments()
    if upload_error:
        flash(upload_error, "error")
        return render_activity_form(
            activity, "Edit Activity" if activity else "Create Activity", 400
        )

    created_new = activity is None
    if created_new:
        activity = Activity(**values)
        db.session.add(activity)
    else:
        for field, value in values.items():
            setattr(activity, field, value)

    saved_paths = []
    try:
        # Obtain the new activity ID before adding its attachments.
        db.session.flush()
        saved_paths = save_attachments(activity, uploads)
        db.session.commit()
    except Exception:
        db.session.rollback()
        for path in saved_paths:
            try:
                os.remove(path)
            except OSError:
                pass
        raise

    flash(
        "Activity created as an unpublished draft."
        if created_new else "Activity updated successfully.",
        "success",
    )
    return redirect(url_for("admin.activities"))


@admin_bp.route("/activities/new", methods=["GET", "POST"])
@roles_required(User.ROLE_ADMIN, User.ROLE_EDITOR)
def create_activity():
    if request.method == "POST":
        return handle_activity_form()
    return render_template(
        "admin/activity_form.html",
        activity=None, form_data={}, page_title="Create Activity", attachments=[]
    )


@admin_bp.route("/activities/<int:activity_id>/edit", methods=["GET", "POST"])
@roles_required(User.ROLE_ADMIN, User.ROLE_EDITOR)
def edit_activity(activity_id):
    activity = db.get_or_404(Activity, activity_id)
    if request.method == "POST":
        return handle_activity_form(activity)
    return render_template(
        "admin/activity_form.html",
        activity=activity, form_data={}, page_title="Edit Activity",
        attachments=ActivityAttachment.query.filter_by(
            activity_id=activity.id
        ).all(),
    )


@admin_bp.route("/attachments/<int:attachment_id>/delete", methods=["POST"])
@roles_required(User.ROLE_ADMIN, User.ROLE_EDITOR)
def delete_attachment(attachment_id):
    attachment = db.get_or_404(ActivityAttachment, attachment_id)
    activity_id = attachment.activity_id
    path = os.path.join(
        current_app.config["UPLOAD_FOLDER"], attachment.stored_filename
    )

    try:
        db.session.delete(attachment)
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise

    try:
        if os.path.isfile(path):
            os.remove(path)
    except OSError:
        current_app.logger.exception("Could not remove attachment file")

    flash("Attachment removed.", "success")
    return redirect(url_for("admin.edit_activity", activity_id=activity_id))


@admin_bp.route("/activities/<int:activity_id>/publish", methods=["POST"])
@roles_required(User.ROLE_ADMIN, User.ROLE_EDITOR)
def toggle_activity_publication(activity_id):
    activity = db.get_or_404(Activity, activity_id)
    activity.is_published = not activity.is_published
    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise

    status = "published" if activity.is_published else "unpublished"
    flash(f"Activity {status}.", "success")
    return redirect(url_for("admin.activities"))


@admin_bp.route("/activities/<int:activity_id>/delete", methods=["POST"])
@roles_required(User.ROLE_ADMIN, User.ROLE_EDITOR)
def delete_activity(activity_id):
    activity = db.get_or_404(Activity, activity_id)
    paths = remove_activity_files(activity)

    try:
        db.session.delete(activity)
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise

    # Remove physical files only after the database commit succeeds.
    for path in paths:
        try:
            if os.path.isfile(path):
                os.remove(path)
        except OSError:
            current_app.logger.exception(
                "Could not remove an activity attachment file"
            )

    flash("Activity deleted.", "success")
    return redirect(url_for("admin.activities"))
