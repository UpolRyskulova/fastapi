from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas, database, models
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

# SECRET_KEY
# Algorithm
# Expiration Time

# SECRET_KEY = 'ec3634fa9ce54df336d2f6a2255a78076be327e02a9e16dd3a1015c2e2522bae'
# ALGORITHM = 'HS256'
# ACCESS_TOKEN_EXPIRES_MINUTES = 60


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expires_minutes)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)

    return encoded_jwt


def verify_access_token(token: str, credentials_exceptions):
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])

        id: str = payload.get("user_id")

        if id is None:
            raise credentials_exceptions

        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exceptions

    return token_data


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exceptions = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                           detail=f"Could not validate credentials",
                                           headers={"WWW-Authenticate": "Bearer"})

    token = verify_access_token(token, credentials_exceptions)

    user = db.query(models.User).filter(models.User.id == token.id).first()

    if not user:
        raise credentials_exceptions

    return token
