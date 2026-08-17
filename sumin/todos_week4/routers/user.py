from fastapi import APIRouter, status, HTTPException
from sqlalchemy import select

from database.db_connection import SessionFactory
from model import User
from auth.password import hash_password
from schema.request import UserSignUpRequest
from schema.response import UserSignUpResponse

router = APIRouter(tags=["User"])

#회원가입
@router.post(
    "/users/signup",
    status_code=status.HTTP_201_CREATED,
    response_model=UserSignUpResponse,
)
def signup_user_handler(body: UserSignUpRequest):
    session = SessionFactory()
    try:
        #이메일 중복 검사
        stmt = select(User).where(User.email == body.email)
        existing_user = session.execute(stmt).scalars().first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="이미 사용 중인 이메일입니다.",
            )

        #비밀번호 해시 후 저장
        user = User(
            email=str(body.email),
            hashed_password=hash_password(body.password),
        )
        session.add(user)
        session.commit()
        session.refresh(user)
        return user
    finally:
        session.close()
