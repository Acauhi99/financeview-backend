from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from app.auth.verifier_auth import token_verify

router = APIRouter(prefix='/test', tags=['test'], dependencies=[Depends(token_verify)])

@router.get("/user_token")
def test_user_verify():
    return {
        "message": "User token verified successfully",
        "status_code": status.HTTP_200_OK
    }