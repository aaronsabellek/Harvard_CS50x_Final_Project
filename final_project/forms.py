from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, TextAreaField
from wtforms.validators import  InputRequired, Length, Email, EqualTo, ValidationError

from final_project.routes import flash, current_user
from final_project.models import User


# Create Forms
class LoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), Length(min=1, max=20)])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=8, max=30)])
    remember = BooleanField("Remember me")
    submit = SubmitField("Login")

class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), Length(min=1, max=15)])
    email = StringField("Email", validators=[InputRequired(), Email(message="Invalid email"), Length(max=50)])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=8, max=30)])
    confirm_password = PasswordField("Confirm Password", validators=[InputRequired(), EqualTo('password', message='Passwords must match!')])
    submit = SubmitField("Register")

    def validate_username(seld, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            flash("Username is already taken", "warning")
            raise ValidationError('Username is already taken')

    def validate_email(seld, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            flash("Email is already taken", "warning")
            raise ValidationError('Email is already taken')

class UpdateAccountForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), Length(min=1, max=15)])
    email = StringField("Email", validators=[InputRequired(), Email(message="Invalid email"), Length(max=50)])
    info = StringField("About you", validators=[Length(max=500)])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(seld, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                flash("Username is already taken", "warning")
                raise ValidationError('Username is already taken')

class PostForm(FlaskForm):
    task = SelectField('Task', choices=[('Search'), ('Recommend')], validators=[InputRequired()])
    title = StringField('Title', validators=[InputRequired()])
    content = TextAreaField('Content', validators=[InputRequired()])
    submit = SubmitField('Post')

class ContactForm(FlaskForm):
    recipient = StringField('Recipient', validators=[InputRequired()])
    post = StringField('Post', validators=[InputRequired()])
    message = TextAreaField('Message', validators=[InputRequired()])
    submit = SubmitField('Contact')

class EmptyForm(FlaskForm):
    submit = SubmitField('Submit')

class RequestResetForm(FlaskForm):
    email = StringField("Email", validators=[InputRequired(), Email(message="Invalid email"), Length(max=50)])
    submit = SubmitField('Reset Password')

    def validate_email(seld, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            flash("Email is already taken", "warning")
            raise ValidationError('There is no account with that email')

class ResetPasswordForm(FlaskForm):
    password = PasswordField("Password", validators=[InputRequired(), Length(min=8, max=30)])
    confirm_password = PasswordField("Confirm Password", validators=[InputRequired(), EqualTo('password', message='Passwords must match!')])
    submit = SubmitField('Reset Password')