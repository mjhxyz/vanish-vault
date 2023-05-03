
from sqlalchemy import Column, Integer, String
from werkzeug.security import generate_password_hash

from vanish_vault.models.base import Base


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, comment='用户ID')
    username = Column(String(24), nullable=False, comment='用户昵称')
    phone_number = Column(String(18), unique=True, comment='手机号')
    email = Column(String(50), unique=True, nullable=False, comment='邮箱')
    confirmed = Column(Integer, default=0, comment='是否验证邮箱')
    wx_open_id = Column(String(50), comment='微信open_id')
    wx_name = Column(String(32), comment='微信昵称')

    # 定义一个 _password 属性, 用于存储密码
    # 使用 @property 装饰器, password 成为属性
    # 这样设置 password 属性的时候，就可以先加密再赋值给 _password
    _password = Column('password', String(128), comment='密码')

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw):
        self._password = generate_password_hash(raw)
