from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, SubmitField, RadioField, IntegerField
from wtforms.validators import DataRequired, Length,  Regexp, EqualTo
from wtforms import ValidationError, validators
from ..models import User
from flask.ext.wtf import RecaptchaField


class RegistrationForm(Form):

    username = StringField('Username', validators=[
        DataRequired(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                          'Usernames must have only letters, '
                                          'numbers, dots or underscores')])
    password = PasswordField('Password', validators=[
        DataRequired(), EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    recaptcha = RecaptchaField('Are you human?',
        description="Type both words into the text box to prove that you are a human and not a computer program")

    welcomeM = StringField('Welcome Message', validators=[
        DataRequired(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                          'Usernames must have only letters, '
                                          'numbers, dots or underscores')])

    pin = IntegerField('Personal pin', validators=[Length(4, 4)])
    submit = SubmitField('Register')


    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')


        username = User.query.filter(User.username == self.username.data.lower()).first()
        if username:

            self.username.errors.append("That username is already taken.")
            return False
        else:
          return True




class LoginForm(Form):

    username = StringField('', validators=[
        DataRequired(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                          'Usernames must have only letters, '
                                          'numbers, dots or underscores')], description="test")
    password = PasswordField('', validators=[ DataRequired()])

    submit = SubmitField('Login')


    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        if not Form.validate(self):
            return False

        user = User.query.filter_by(username=self.username.data.lower()).first()
        if user and user.verify_password(self.password.data):
            return True

        else:
            self.username.errors.append("Invalid username or password")
            return False



class ChangePasswordForm(Form):
    old_password = PasswordField('Old password', validators=[DataRequired()])
    password = PasswordField('New password', validators=[
        DataRequired(), EqualTo('password2', message='Passwords must match')])
    password2 = PasswordField('Confirm new password', validators=[DataRequired()])
    welcomeM = StringField('Welcome Message', validators=[Length(1, 64)])
    submit = SubmitField('Update Password')





