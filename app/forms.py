from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, RadioField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class DeleteForm(FlaskForm):
    confirm1_1 = StringField('Confirm', validators=[DataRequired()])
    confirm1_2 = StringField(
        'Repeat confirm', validators=[DataRequired(), EqualTo('confirm')])
    submit = SubmitField('Delete')

class ChangeRoleForm(FlaskForm):
    radio_buttons = RadioField(
        'User role', choices=[('Member','Member'),('Admin','Admin')], validators=[DataRequired()])
    confirm2_1 = StringField('Confirm', validators=[DataRequired()])
    confirm2_2 = StringField(
        'Repeat confirm', validators=[DataRequired(), EqualTo('confirm2_1')])
    submit2 = SubmitField('Change role')

class MakePostForm(FlaskForm):
    body = TextAreaField('Body', validators=[DataRequired()])
    submit3 = SubmitField('Post')
