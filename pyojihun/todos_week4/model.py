from sqlalchemy import Integer, String, Boolean, ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column , relationship
from database.orm import Base

#model.py라는 파일에는 일반적으로 ORM을 정의함.
#ORM은 테이블과 1대1로 대응되는 클래스임.
#(소웨공, 데베 수업 중) 클래스 다이어그램과 ERD를 합치는 과정은 ORM을 사용하는 것을 전제로 한 것이었던 듯..!
class Todo(Base):
    __tablename__ = 'todo'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    title: Mapped[String] = mapped_column(
        String(255),
        nullable=False,
    )
    is_done: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey('user.id'),
        nullable=True,
    )
    user: Mapped[User] = relationship(
        back_populates="todos",
    )

class User(Base):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[String] = mapped_column(
        String(255),
        unique=True, # 고유키로 설정
        nullable=False,
        index=True,
    )
    hashed_password: Mapped[String] = mapped_column(
        String(255),
        nullable=False,
    )
    created_at: Mapped[DateTime] = mapped_column(
        DateTime,
        server_default=func.now(),
        nullable=False,
    )
    todos: Mapped[list["Todo"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )