
from flask import Blueprint, render_template

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
    return render_template("activities.html")
