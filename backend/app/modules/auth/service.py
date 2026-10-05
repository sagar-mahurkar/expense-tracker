from app.errors.exceptions import UnauthorizedError, ValidationError
from app.extensions import db
from app.modules.auth.repository import create_user, find_user_by_email
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash, generate_password_hash


def hash_password(password: str) -> str:
    return generate_password_hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    return check_password_hash(password_hash, password)


def register_user(
    name: str,
    email: str,
    password: str,
):
    existing_user = find_user_by_email(email)

    if existing_user is not None:
        raise ValidationError("Email is already registered")

    password_hash = hash_password(password)

    try:
        user = create_user(
            name=name,
            email=email,
            password_hash=password_hash,
        )

        db.session.commit()

        return user

    except Exception:
        db.session.rollback()
        raise
    
def login_user(
    email: str,
    password: str,
):
    user = find_user_by_email(email)

    if user is None:
        raise UnauthorizedError("Invalid email or password")

    if not verify_password(password, user.password_hash):
        raise UnauthorizedError("Invalid email or password")

    access_token = create_access_token(
        identity=str(user.id),
    )

    return user, access_token

