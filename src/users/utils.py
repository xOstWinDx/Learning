import bcrypt


def hash_password(password: str) -> bytes:
    salt = bcrypt.gensalt()
    pwd_bytes = password.encode()
    return bcrypt.hashpw(pwd_bytes, salt)



