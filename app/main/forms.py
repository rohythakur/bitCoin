from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField, BooleanField, SelectField,\
    SubmitField, PasswordField, FileField, RadioField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from wtforms import ValidationError, validators
from ..models import User
from flask.ext.wtf import RecaptchaField
from flask.ext.babel import gettext


class ProfileviewForm(Form):

    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')


class EditProfileForm(Form):

    location = StringField( 'Location', validators=[Length(0, 64), ], description="test")
    about_me = TextAreaField('About me')
    welcomeM = StringField('Welcome Message', validators=[Length(0, 64)])
    pgpkey = TextAreaField('Pgp Key')
    submit = SubmitField('Update')

class FindMoneyForm(Form):
    buyorsell = SelectField(("Buy or Sell"), validators=[validators.required()])
    payment_method = SelectField(("Select Payment Method"), validators=[validators.required()])

class CreateItemForm(Form):


    buyorsell = SelectField(("I want to Buy or Sell Bitcoins"), validators=[validators.optional()])
    location = SelectField(("Select location"), validators=[validators.optional()])
    item_description = TextAreaField('Description')
    payment_method = SelectField(("Select Payment Method"), validators=[validators.optional()])
    item_listed = BooleanField('Item Listed', default=False)
    price = StringField('Price',  [validators.NumberRange(min=0, max=10)])
    tradelimitmin = StringField('Trade Min',  [validators.NumberRange(min=0, max=10)])
    tradelimitmax = StringField('Trade Max',  [validators.NumberRange(min=0, max=10)])
    submit = SubmitField('Create item')

    def __init__(self, csrf_enabled=False, *args, **kwargs):
        super(CreateItemForm, self).__init__(csrf_enabled=False, *args, **kwargs)





