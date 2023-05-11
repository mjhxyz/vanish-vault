from wtforms import Form, StringField, PasswordField, IntegerField
from wtforms.validators import DataRequired, Length, EqualTo, Email, ValidationError, NumberRange

from vanish_vault.models.user import User


class ShareForm(Form):
    secret_key = StringField(
        validators=[DataRequired(message='密码不能为空'), Length(3, 32, message='密钥长度在3到32个字符之间')])
    content = StringField(
        validators=[DataRequired(message='内容不能为空'), Length(1, 5000, message='内容长度在1到5000个字符之间')])
    valid_time = IntegerField(
        validators=[DataRequired(message='过期时间不能为空'), NumberRange(min=1, max=60 * 24 * 7, message='过期时间在1到10080分钟之间')])
