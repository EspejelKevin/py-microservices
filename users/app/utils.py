from passlib.hash import pbkdf2_sha256


class Utils:
    @classmethod
    def hash_password(cls, password: str) -> str:
        return pbkdf2_sha256.hash(password)

    @classmethod
    def verify_password(cls, password: str, hashed_password: str) -> bool:
        try:
            return pbkdf2_sha256.verify(password, hashed_password)
        except Exception:
            return False
