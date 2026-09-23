from fastapi import Request, APIRouter, Response, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from datetime import timedelta
from app.model.user import UserModel
from app.enum.token_varients import TokenVarients
from app.services.jwt_handler import create_token
from fastapi.responses import RedirectResponse
from app.services.oauth import oauth
router = APIRouter(prefix="/auth",tags=["Auth"])

ACCESS_TOKEN_AGE=timedelta(days=1)
REFRESH_TOKEN_AGE=timedelta(days=2) #minutes_15
REFRESH_TOKEN_COOKIE_AGE=2 * 24 * 60 * 60
ACCESS_TOKEN_COOKIE_AGE=1 * 24 * 60 * 60

@router.get("/google/login")
async def google_login(
    request: Request
):
    redirect_uri = request.url_for(
        "google_callback"
    )

    return await oauth.google.authorize_redirect(
        request,
        redirect_uri
    )

PUBLIC_CALLBACK_URL = "http://127.0.0.1:8000/auth/google/callback"

@router.get("/google/callback")
async def google_callback(
    request: Request,
    db: Session = Depends(get_db)
):
    # Explicitly pass the redirect_uri expected by Google
    token = await oauth.google.authorize_access_token(
        request, 
    )

    user_info = token.get("userinfo")
    email = user_info["email"]

    user = db.query(UserModel).filter(UserModel.email == email).first()
    if not user:
        user = UserModel(email=email, name=user_info["name"])
        db.add(user)
        db.commit()
        db.refresh(user)

    access_token = create_token({"user_id": user.id}, ACCESS_TOKEN_AGE, TokenVarients.ACCESS_TOKEN.value)
    refresh_token = create_token({"user_id": user.id}, REFRESH_TOKEN_AGE, TokenVarients.REFRESH_TOKEN.value)

    response = RedirectResponse(url="http://127.0.0.1:3000/home", status_code=302)

    response.set_cookie(
        key=TokenVarients.ACCESS_TOKEN.value,
        value=access_token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=ACCESS_TOKEN_COOKIE_AGE
    )

    response.set_cookie(
        key=TokenVarients.REFRESH_TOKEN.value,
        value=refresh_token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=REFRESH_TOKEN_COOKIE_AGE
    )

    return response
    
# @router.get(
#     "/google/callback",
#     name="google_callback"
# )
# async def google_callback(
#     request: Request,
#     response: Response,
#     db: Session = Depends(get_db)
# ):
#     token = await oauth.google.authorize_access_token(
#         request
#     )

#     user_info = token["userinfo"]

#     email = user_info["email"]

#     user = db.query(UserModel).filter(
#         UserModel.email == email
#     ).first()

#     if not user:
#         user = UserModel(
#             email=email,
#             name=user_info["name"]
#         )

#         db.add(user)
#         db.commit()
#         db.refresh(user)

#     access_token = create_token(
#         {"user_id": user.id},
#         ACCESS_TOKEN_AGE,
#         TokenVarients.ACCESS_TOKEN.value
#         )
#     refresh_token = create_token(
#         {"user_id": user.id},
#         REFRESH_TOKEN_AGE,
#         TokenVarients.REFRESH_TOKEN.value
#     )
#     response = RedirectResponse(url="http://127.0.0.1:3000/home")

#     response.set_cookie(
#         key=TokenVarients.ACCESS_TOKEN.value,
#         value=access_token,
#         httponly=True,
#         secure=False,  # True in production
#         samesite="lax",
#         max_age=ACCESS_TOKEN_COOKIE_AGE
#     )

#     response.set_cookie(
#         key=TokenVarients.REFRESH_TOKEN.value,
#         value=refresh_token,
#         httponly=True,
#         secure=False,  # True in production
#         samesite="lax",
#         max_age=REFRESH_TOKEN_COOKIE_AGE
#     )

#     return response