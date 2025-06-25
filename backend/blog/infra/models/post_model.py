from sqlalchemy import Column, String, Text, DateTime
from blog.infra.database import Base
from datetime import datetime

class PostModel(Base):
    __tablename__ = "posts"

    id = Column(String, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(String(300), nullable=False)
    content = Column(Text, nullable=False)
    user_id = Column(String, nullable=False)
    date = Column(DateTime, default=datetime.now, nullable=False)
