from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired, ValidationError, EqualTo, Email, Length

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(max=256)], render_kw={"placeholder": "Username"})
    password = PasswordField('Password', validators=[DataRequired(), Length(max=36)], render_kw={"placeholder": "Password"})
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(max=256)], render_kw={"placeholder": "Username"})
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=256)], render_kw={"placeholder": "email"})
    password = PasswordField('Password', validators=[DataRequired(), Length(max=36)], render_kw={"placeholder": "Password"})
    # makes sure 2nd password is same as 1st password
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password'), Length(max=36)], render_kw={"placeholder": "Confirm Password"})
    submit = SubmitField('Register')

class CreateChatForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=256)], render_kw={"placeholder": "name"})
    image = StringField('Image', validators=[Length(max=256)], render_kw={"placeholder": "Image"})
    submit = SubmitField('Create Chat')

class SendMessageForm(FlaskForm):
    content = StringField('Username', validators=[DataRequired(), Length(max=256)], render_kw={"placeholder": "message"})
    reply_to = IntegerField('reply_to', validators=[Length(max=256)], render_kw={"placeholder": "reply_to"})
    submit = SubmitField('Send Message')
