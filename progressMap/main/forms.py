from flask_wtf import Form
from wtforms.fields import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Regexp, ValidationError, Length
from flask_login import login_user
from ..models import User, db


class LoginForm(Form):
    username = StringField(validators=[DataRequired()])
    password = PasswordField(validators=[DataRequired()])
    remember_me = BooleanField('Remember me')

    def login_user(self):
        user = User.get_by_username(self.username.data)
        if user is not None and user.check_password(self.password.data):
            login_user(user, self.remember_me.data)
            return user
        return None


class SignupForm(Form):
    username = StringField(validators=[DataRequired(), Length(3, 40), Regexp(
        '^[A-Za-z0-9_]{3,}$', message='Usernames consist of numbers, letters, and underscores.')])
    email = StringField(validators=[DataRequired(), Email(), Length(1, 120)])
    password = PasswordField(validators=[DataRequired(), EqualTo(
        'confirmPassword', message='Passwords must match.')])
    confirmPassword = PasswordField(validators=[DataRequired()])
    remember_me = BooleanField('Remember me')

    def validate_email(self, email_field):
        if User.query.filter_by(email=email_field.data).first():
            raise ValidationError(
                'There\'s aready a user with this email address.')

    def validate_username(self, username_field):
        if User.query.filter_by(username=username_field.data).first():
            raise ValidationError('This username is already taken.')

    def save(self):
        user = User(username=self.username.data,
                    email=self.email.data, password=self.password.data)
        db.session.add(user)
        db.session.commit()
