from typing import Annotated, Any, Dict
from fastapi import Depends, HTTPException, Request, status
from jose import JWTError, jwt
from app.core.config import settings
from app.enums.token_variants import TokenVariants


def verify_token(token: str, expected_type: str = TokenVariants.ACCESS_TOKEN.value) -> Dict[str, Any]:
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm],
        )
        token_type = payload.get("type")
        if token_type != expected_type:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type",
            )
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )


def get_current_user_id(request: Request) -> int:
    access_token = request.cookies.get(TokenVariants.ACCESS_TOKEN.value)
    
    # Also support Authorization: Bearer <token> header for API / agent clients
    if not access_token:
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            access_token = auth_header.split(" ", 1)[1]

    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access token missing",
        )

    payload = verify_token(access_token, TokenVariants.ACCESS_TOKEN.value)
    user_id = payload.get("user_id")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload: user_id missing",
        )
    return int(user_id)


# Type alias for dependency injection
CurrentUserId = Annotated[int, Depends(get_current_user_id)]
