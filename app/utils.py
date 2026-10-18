from passlib.context import CryptContext

# 1. Configure the context to use bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(password: str):
    return pwd_context.hash(password)


def verify(plain_pswrd: str, hashed_paswrd: str):
    return pwd_context.verify(plain_pswrd, hashed_paswrd)
