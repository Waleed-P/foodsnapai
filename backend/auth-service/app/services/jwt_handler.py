from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
import os
from fastapi import HTTPException
SECRET_KEY = os.environ["JWT_SECRET_KEY"]
ALGORITHM = os.environ["JWT_ALGORITHM"]


def create_token( data: dict, expires_delta: timedelta, token_type: str ): 
    payload = data.copy() 
    expire_time = datetime.now(timezone.utc) + expires_delta 
    print(f"Token Type: {token_type}") 
    print(f"Token Lifetime: {expires_delta}") 
    print(f"Expires At: {expire_time}") 
    payload.update({ "exp": expire_time, "type": token_type }) 
    return jwt.encode( payload, SECRET_KEY, algorithm=ALGORITHM )

def verify_token(token: str, expected_type: str):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        token_type = payload.get("type")
        if token_type != expected_type:
            print("token type = ",token_type,"expected type = ",expected_type)
            raise HTTPException(
                status_code=401,
                detail="Invalid token type"
            )

        return payload

    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )