import jwt
import bcrypt

from datetime import datetime, timedelta

SECRET_KEY = 'eyJJc3N1ZXIgKGlzcykiOiJJc3N1ZXIiLCJJc3N1ZWQgQXQgKGlhdCkiOiIyMDI0LTAxLTIyVDA5OjIyOjUxLjA5NVoiLCJFeHBpcmF0aW9uIFRpbWUgKGV4cCkiOiIyMDI0LTAxLTIyVDEwOjIyOjUxLjA5NVoiLCJTdWJqZWN0IChzdWIpIjoiU3ViamVjdCIsIlVzZXJuYW1lIChhdWQpIjoiSmF2YUd1aWRlcyIsIlJvbGUiOiJBRE1JTiJ9'
EXPIRATION_TIME = timedelta(minutes=30)


def create_jwt_token(payload: dict, algorithm: str):

    expiration = datetime.now() + EXPIRATION_TIME
    payload.update({"exp": expiration})
    token = jwt.encode(payload, SECRET_KEY, algorithm=algorithm)

    return token


def verify_jwt_token(token: str, algorithm: str):

    try:
        decode_data = jwt.decode(jwt=token, key=SECRET_KEY, algorithms=[algorithm])

        return decode_data

    except jwt.PyJWTError:
        return None


def hash_password(password: str):

    salt = bcrypt.gensalt()
    pwd = password.encode()

    return bcrypt.hashpw(pwd, salt)


def validate_password(password: str,  hashed_password: str):

    return bcrypt.checkpw(password=password.encode(), hashed_password=hashed_password.encode())

