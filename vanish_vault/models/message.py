from sqlalchemy import Column, Integer, String, DateTime, Text

from vanish_vault.models.base import Base
from vanish_vault import login_manager


class Message(Base):
    __tablename__ = 'message'

    id = Column(Integer, primary_key=True, comment='消息ID')
    title = Column(String(50), nullable=False, comment='消息标题')
    content = Column(Text(5000), nullable=False, comment='消息内容')
    key = Column(String(10), unique=True, nullable=False, index=True, comment='消息唯一标识')
    user_id = Column(Integer, nullable=False, index=True, comment='用户ID')
    expire_at = Column(DateTime, nullable=False, comment='消息过期时间')
    