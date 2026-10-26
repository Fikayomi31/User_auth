from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    # Convert plain text password into a secure hash.
    return pwd_context.hash(password)

def verify_password(plain_password: str, hash_password: str) -> bool:
    # Verify whether password matches its stored hash.
    return pwd_context.verify(plain_password, hash_password)