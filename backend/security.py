import os
from datetime import datetime, timedelta, timezone

import bcrypt
import jwt

from dotenv import load_dotenv

load_dotenv()

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
if not JWT_SECRET_KEY:
    raise RuntimeError("JWT_SECRETが設定されていません")
JWT_ALGORITHM = "HS256"
JWT_EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRE_MINUTES", "60"))

def hash_password(password: str) -> str:
    """
    登録時に使用する。
    平文のパスワードを、データベース保存用の文字列に変換する。
    """
    password_bytes = password.encode("utf-8")

    hashed_bytes = bcrypt.hashpw(
        password_bytes,
        bcrypt.gensalt(),
    )

    return hashed_bytes.decode("utf-8")

def verify_password(
    plain_password: str,
    hashed_password: str,
) -> bool:
    """
    ログイン時に使用する。
    入力されたパスワードと保存済みのハッシュ値を照合する。
    """
    return bcrypt.checkpw(
        plain_password.encode("utf-8"),
        hashed_password.encode("utf-8"),
    )

def create_access_token(user_id: int) -> str:
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=JWT_EXPIRE_MINUTES)

    payload = {
        "sub": str(user_id),
        "exp": expires_at,
    }

    return jwt.encode(
        payload,
        JWT_SECRET_KEY, 
        algorithm=JWT_ALGORITHM
        )

