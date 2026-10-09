import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")

    if not SECRET_KEY:
        raise RuntimeError(
            "SECRET_KEY must be configured in .env or the environment."
        )

    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg://u0_a344@localhost/digistix"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Uploaded activity attachments
    UPLOAD_FOLDER = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "instance",
        "uploads",
    )

    # Maximum HTTP request size: 110 MiB
    MAX_CONTENT_LENGTH = 110 * 1024 * 1024
