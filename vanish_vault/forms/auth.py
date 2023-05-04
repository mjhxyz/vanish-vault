from wtforms import Form, StringField, PasswordField
from wtforms.validators import DataRequired, Length, EqualTo, Email, ValidationError

from vanish_vault.models.user import User


class LoginForm(Form):
    username = StringField(
        validators=[DataRequired(message='用户名不能为空'), Length(2, 10, message='昵称至少需要两个字符，最多10个字符')])
    password = PasswordField(
        validators=[DataRequired(message='密码不能为空'), Length(6, 32, message='密码长度至少需要6到32个字符之间')])

    def validate_username(self, field):
        # 验证用户名是否存在
        if not User.query.filter_by(username=field.data).first():
            raise ValidationError('电子邮箱不存在')


class RegisterForm(Form):
    email = StringField(
        validators=[DataRequired(message='电子邮件不能为空'), Length(6, 64, message='电子邮箱长度在6到64个字符'), Email(message='电子邮箱不符合规范')])

    password = PasswordField(
        validators=[DataRequired(message='密码不能为空'), Length(6, 32, message='密码长度至少需要6到32个字符之间')])
    repassword = PasswordField(
        validators=[DataRequired(message='密码不能为空'), Length(6, 32, message='密码长度至少需要6到32个字符之间'),
                    EqualTo('password', message='两次输入的密码不相同')])

    username = StringField(
        validators=[DataRequired(message='用户昵称不能为空'), Length(2, 10, message='昵称至少需要两个字符，最多10个字符')])

    def validate_email(self, field):
        # 邮箱地址保证唯一性
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('电子邮箱已被注册')

    def validate_username(self, field):
        # 用户名保证唯一性
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已存在')
