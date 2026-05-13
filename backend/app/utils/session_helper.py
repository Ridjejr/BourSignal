import uuid

from flask import session


def get_session_id():
    """Retourne un ID unique pour l'utilisateur courant."""
    if "user_session_id" not in session:
        session["user_session_id"] = str(uuid.uuid4())
    return session["user_session_id"]
