import os
import secrets

SECRET_KEY = os.getenv("JWT_SECRET_KEY")

if not SECRET_KEY:
    raise RuntimeError(
        "JWT_SECRET_KEY environment variable is not set. Please set."
        "Set it before starting the application."

    )
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30