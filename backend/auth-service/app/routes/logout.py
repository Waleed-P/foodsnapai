from fastapi import APIRouter,Response
from app.enum.token_varients import TokenVarients
router = APIRouter(prefix="/auth",tags=["Auth"])
@router.post("/logout")
def logout(response: Response):
    response.delete_cookie(key=TokenVarients.ACCESS_TOKEN.value, path="/")
    response.delete_cookie(key=TokenVarients.REFRESH_TOKEN.value, path="/")
    return {"message": "Logged out"}