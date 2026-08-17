from database.orm import Base
from sqlalchemy import Integer, String, Text, DateTime,text
from sqlalchemy.orm import Mapped, mapped_column

class Blog(Base):
    __tablename__="blogs"

    id: Mapped["int"] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped["str"] = mapped_column(String(255), nullable=False)
    content: Mapped["str"] = mapped_column(Text(1000), nullable=False)
    created_at: Mapped["DateTime"] = mapped_column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
