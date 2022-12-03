from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    # remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class ItemAddForm(FlaskForm):
    text = StringField('Description', validators=[DataRequired()])
    photo = FileField('Your Photo', validators=[FileRequired(),
                                                FileAllowed(['jpg', 'png', 'jpeg'], 'Images Only')])
    name = StringField("Item Name", validators=[DataRequired()])
    submit = SubmitField('Add')


class CreateCommunityForm(FlaskForm):
    name = StringField('Community Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Create')


class DeleteCommunityForm(FlaskForm):
    name = StringField('Community to Delete', validators=[DataRequired()])
    submit = SubmitField('Delete')


class CreateCollectionForm(FlaskForm):
    name = StringField('Name of collection', validators=[DataRequired()])
    desc = StringField('Description of collection', validators=[DataRequired()])
    submit = SubmitField('Create Collection')


class CreatePostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    body = TextAreaField('Body', validators=[DataRequired()])
    submit = SubmitField('Post!')


class EditPostForm(FlaskForm):
    body = TextAreaField('Body', validators=[DataRequired()])
    submit = SubmitField('Save')


# class EditItemForm(FlaskForm):

class DeletePostForm(FlaskForm):
    submitConfirm = SubmitField('Confirm')
    submitCancel = SubmitField('Cancel')


class DeleteItemForm(FlaskForm):
    submitConfirm = SubmitField('Confirm')
    submitCancel = SubmitField('Cancel')


class UserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    bio = StringField('Biography', validators=[DataRequired()])
    profile_picture = SelectField('Profile Picture', validators=[DataRequired()],
                                  choices=[('lion', 'Lion'), ('eagle', 'Eagle'), ('zebra', 'Zebra'), ('snake', 'Snake'),
                                           ('pony', 'Pony')])
    submit = SubmitField("Submit")


class CreateCommentForm(FlaskForm):
    text = TextAreaField('Leave a comment below...', validators=[DataRequired()])
    submit = SubmitField('Post!')
