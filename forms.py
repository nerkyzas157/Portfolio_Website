from flask_wtf import FlaskForm  # type: ignore
from wtforms import StringField, PasswordField, SubmitField, EmailField  # type: ignore
from wtforms.validators import DataRequired, URL  # type: ignore


class CreatePostForm(FlaskForm):
    title = StringField("Blog Post Title", validators=[DataRequired()])
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    img_url = StringField("Blog Image URL", validators=[URL()])
    github_url = StringField(
        "GitHub Repository URL", validators=[DataRequired(), URL()]
    )
    submit = SubmitField("Submit Project")


class AuthForm(FlaskForm):
    key = PasswordField("Secret Key", validators=[DataRequired()])
    submit = SubmitField("Login")


class ContactForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = EmailField("Email Address", validators=[DataRequired()])
    message = StringField("Message", validators=[DataRequired()])
    submit = SubmitField("Submit")
