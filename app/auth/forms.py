from flask_wtf import FlaskForm as Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import Required, Email, Length, EqualTo, DataRequired


class LoginForm(Form):
    email = StringField('email', validators=[Required(), Length(1, 64)], render_kw={"placeholder": "email"})
    password = PasswordField('Password', validators=[Required()], render_kw={"placeholder": "Password"})
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')

class ResetRequestForm(Form):
    email = StringField('email', validators=[Required(), Length(1, 64)], render_kw={"placeholder": "email"})
    submit = SubmitField('Request new Password')

class ResetPasswordForm(Form):
    password = PasswordField('New Password',
                             validators=[
                                DataRequired(message="Die Angabe ist erforderlich"),
                                Length(min=8, message="Die Mindestlänge beträgt 8 Zeichen")],
                             render_kw={"placeholder": "Password"})
    confirm = PasswordField('Repeat Password',
                            validators=[
                                DataRequired(message="Die Angabe ist erforderlich"),
                                EqualTo('password', message='Die Eingaben müssen übereinstimmen')],
                            render_kw={"placeholder": "Password"})
    submit = SubmitField('Change Password')