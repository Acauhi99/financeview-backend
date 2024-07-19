from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from app.auth.verifier_auth import token_verify

router = APIRouter(prefix='/test', tags=['test'], dependencies=[Depends(token_verify)])

@router.get("/user_token")
def test_user_verify() -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": "User is verified"}
    )