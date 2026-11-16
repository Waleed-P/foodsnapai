from fastapi import APIRouter, Response
from app.enums.token_variants import TokenVariants
from app.schemas.user import MessageResponse

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/logout", response_model=MessageResponse)
def logout(response: Response):
    response.delete_cookie(key=TokenVariants.ACCESS_TOKEN.value, path="/")
    response.delete_cookie(key=TokenVariants.REFRESH_TOKEN.value, path="/")
    return MessageResponse(message="Logged out")
