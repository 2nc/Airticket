
from wtforms import StringField, PasswordField, Form
from wtforms.validators import Length, Email, ValidationError, EqualTo
from .base import DataRequired
from app.models.user import User


class LoginForm(Form):
    nickname = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[
        DataRequired(message='Please enter your password.')])


class RegisterForm(Form):
    nickname = StringField('Username', validators=[DataRequired(), Length(2, 10)])
    password = PasswordField('Password', validators=[DataRequired(),
                                               EqualTo('repeat_password'), Length(6, 20)])
    repeat_password = PasswordField('Confirm Password', validators=[DataRequired(), Length(6, 20)])
    name = StringField('Name', validators=[DataRequired(), Length(1, 10)])
    id_card = StringField('ID Number', validators=[DataRequired()])
    phone_number = StringField('Phone', validators=[DataRequired()])

    def validate_id_card(self, field):
        if User.query.filter_by(id_card=field.data).first():
            raise ValidationError('Your ID have been registered.')

    def validate_nickname(self, field):
        if User.query.filter_by(nickname=field.data).first():
            raise ValidationError('Username exists.')


class ChangeInfoForm(Form):
    nickname = StringField('Username', validators=[DataRequired(), Length(2, 10)])
    password = PasswordField('Password', validators=[DataRequired(), Length(6, 20)])
    name = StringField('Name', validators=[DataRequired(), Length(1, 10)])
    id_card = StringField('ID Number', validators=[DataRequired()])
    phone_number = StringField('Phone Number', validators=[DataRequired()])
