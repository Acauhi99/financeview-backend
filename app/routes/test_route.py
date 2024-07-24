from fastapi import APIRouter, Depends, status
from app.auth.verifier_auth import token_verify

router = APIRouter(prefix='/test', tags=['test'])

@router.get("/user_token", dependencies=[Depends(token_verify)])
def test_user_verify():
    return {
        "message": "User token verified successfully",
        "status_code": status.HTTP_200_OK
    }