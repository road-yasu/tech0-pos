import bcrypt

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
