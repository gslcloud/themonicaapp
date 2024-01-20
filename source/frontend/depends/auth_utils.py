import json
from datetime import datetime, timedelta
from typing import Dict, Any, Optional

import jwt
import redis

from .session import store_user_session, retrieve_user_session, clear_user_session


SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 30


def generate_access_token(user_id: int) -> str:
    now = datetime.utcnow()
    expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    expire = now + expires_delta
    to_encode = {"user_id": user_id, "exp": expire}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def generate_refresh_token(user_id: int) -> str:
    now = datetime.utcnow()
    expires_delta = timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    expire = now + expires_delta
    to_encode = {"user_id": user_id, "exp": expire}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> Optional[int]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        return user_id
    except jwt.PyJWTError:
        return None


def set_user_session(user_id: int, session_data: Dict[str, Any]) -> None:
    store_user_session(user_id, json.dumps(session_data))


def get_user_session(user_id: int) -> Optional[Dict[str, Any]]:
    session_data = retrieve_user_session(user_id)
    if session_data:
        return json.loads(session_data)
    return None


def clear_user_session(user_id: int) -> None:
    clear_user_session(user_id)