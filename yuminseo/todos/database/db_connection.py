from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

#데이터베이스 연결 정보 설정
DATABASE_URL = "mysql+pymysql://root:fastapi@localhost:3306/fastapi_db"

#엔진 생성
engine = create_engine(DATABASE_URL, echo=True) #echo=True: 실행되는 SQL 쿼리가 로그로 출력되어 디버깅 시 도움

#세션 팩토리 생성
SessionFactory = sessionmaker(
    autocommit=False, #세션에서 수행한 변경 사항을 자동으로 DB에 반영하지 않음
    autoflush=False, #세션의 변경 내용을 자동으로 DB에 반영하지 않음
    expire_on_commit=False, #commit 이후에도 세션에 있는 객체 값 유지
    bind=engine #세션에 사용할 DB 엔진을 지정
)
