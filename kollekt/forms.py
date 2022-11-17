from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo

from flask import url_for, redirect, render_template
from flask_wtf.file import FileField
from werkzeug.utils import secure_filename
from kollekt.models import Communities, CollectionItem, Collections
from . import db


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def returnInfo(self):
        return self.username.data, self.email.data, self.password.data


class LoginForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    # remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class ItemAddForm(FlaskForm):
    community = StringField('Community', validators=[DataRequired()])
    text = StringField('Description', validators=[DataRequired()])
    photo = FileField('Your Photo')
    name = StringField("Item Name")
    submit = SubmitField('Add')


class createCommunityForm(FlaskForm):
    name = StringField('Community Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Create')


class deleteCommunityForm(FlaskForm):
    name = StringField('Community to Delete', validators=[DataRequired()])
    submit = SubmitField('Delete')


class createCollectionForm(FlaskForm):
    name = StringField('Name of collection', validators=[DataRequired()])
    desc = StringField('Description of collection', validators=[DataRequired()])
    submit = SubmitField('Create Collection')


class createPostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    body = TextAreaField('Body')
    item_id = StringField('Attach an Item (Optional)')
    submit = SubmitField('Post!')


class editPostForm(FlaskForm):
    body = TextAreaField('Body')
    item_id = StringField('Attach an Item (Optional)')
    submit = SubmitField('Save')


class deletePostForm(FlaskForm):
    submitConfirm = SubmitField('Confirm')
    submitCancel = SubmitField('Cancel')


class UserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    bio = StringField('Biography', validators=[DataRequired()])
    submit = SubmitField("Submit")


class createCommentForm(FlaskForm):
    text = TextAreaField('Leave a comment below...', validators=[DataRequired()])
    submit = SubmitField('Post!')


class joinLeaveCommunityForm(FlaskForm):
    submitJoin = SubmitField('Join')
    submitLeave = SubmitField('Leave')
