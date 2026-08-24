from sqlalchemy import Integer, String, Boolean #칼럼 타입 임포트
from sqlalchemy.orm import Mapped, mapped_column #ORM 칼럼 매핑 도구 임포트
from database.orm import Base #ORM 기준 클래스 임포트

#Todo 모델 정의(ORM 모델)
class Todo(Base): #Base를 상속함로써 DB 테이블과 매핑됨
    __tablename__ = "todo" #테이블 이름 지정

    id: Mapped[int] = mapped_column( #아이디 컬럼
        Integer,
        primary_key=True,
        autoincrement=True, #id 값이 자동으로 증가
    )

    title: Mapped[str] = mapped_column( #제목 컬럼
        String(255),
        nullable=False, #반드시 존재해야 함
    )

    is_done: Mapped[bool] = mapped_column( #완료 여부 컬럼
        Boolean,
        nullable=False,
        default=False,
    )