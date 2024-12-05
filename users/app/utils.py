from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


class Utils:
    @classmethod
    def hash_password(cls, password: str) -> str:
        return pwd_context.hash(password)

    @classmethod
    def verify_password(cls, password: str, hashed_password: str) -> bool:
        try:
            return pwd_context.verify(password, hashed_password)
        except Exception:
            return False
