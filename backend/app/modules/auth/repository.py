from sqlalchemy import select

from app.extensions import db
from app.models.user import User


def find_user_by_email(email: str) -> User | None:
    statement = select(User).where(User.email == email)

    return db.session.scalar(statement)

def create_user(
    name: str,
    email: str,
    password_hash: str,
) -> User:
    user = User()

    user.name = name
    user.email = email
    user.password_hash = password_hash

    db.session.add(user)
    db.session.flush()

    return user