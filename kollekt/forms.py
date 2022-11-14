from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from flask_login import current_user

from kollekt.models import Communities
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
    # photo = ...
    text = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Add')


class createCommunityForm(FlaskForm):
    name = StringField('Community Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Create')


class deleteCommunityForm(FlaskForm):
    name = StringField('Community to Delete', validators=[DataRequired()])
    submit = SubmitField('Delete')


class createPostForm(FlaskForm):
    valid_communities = []
    option = ()
    title = StringField('Title', validators=[DataRequired()])
    body = TextAreaField('Body')
    item_id = StringField('Attach an Item (Optional)')
    # community = SelectField('Community', valid_communities)
    community = StringField('Community', validators=[DataRequired()])
    submit = SubmitField('Post!')


class UserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    bio = StringField('Biography', validators=[DataRequired()])
    submit = SubmitField("Submit")
