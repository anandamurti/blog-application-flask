from flask_wtf import FlaskForm
from wtforms import validators, StringField, PasswordField, TextAreaField
from flask_wtf.file import FileField, FileAllowed
from author.form import RegisterForm
from author.form import EmailField
from home.models import Category
from wtforms_sqlalchemy.fields import QuerySelectField 
 


class SetupForm(RegisterForm):
    name = StringField('Blog name', [
         validators.DataRequired(),
         validators.Length(min=1, max=100)
    ])

    image = FileField('Upload Image (optional)', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Images only!')
    ])

    class Meta:
        csrf = False  # Needed to allow testing via test client


def categories():
    return Category.query


class PostForm(FlaskForm):
    title = StringField('Title', [
        validators.DataRequired(),
        validators.Length(max=80)
    ])
    body = TextAreaField('Content', validators=[validators.DataRequired()])
    category = QuerySelectField(
        'Category',
        query_factory=categories,
        get_label='name',
        allow_blank=True
    )
    new_category = StringField('New Category')
    
    image = FileField('Upload Image (optional)', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Images only!')
    ])

    class Meta:
        csrf = False  # Optional: disable for testing
