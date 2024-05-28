from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, SelectField, FloatField
from wtforms.validators import DataRequired, Length, ValidationError, NumberRange

from BigfootSightings.queries import get_user_by_user_name
from BigfootSightings.utils.choices import SightingNumber, SightingTitle, SightingLat, SightingLong
from wtforms.validators import NumberRange


class UserLoginForm(FlaskForm):
    username = StringField('Username',
                            validators=[DataRequired(), Length(min=2, max=50)],
                            render_kw=dict(placeholder='Username'))
    password = PasswordField('Password',
                             validators=[DataRequired()],
                             render_kw=dict(placeholder='Password'))
    submit = SubmitField('Login')

    def validate_password(self, field):
        user = get_user_by_user_name(self.username.data)
        if user is None:
            raise ValidationError(f'User name "{self.username.data}" does not exist.')
        if user.password != self.password.data:
            raise ValidationError(f'User name or password are incorrect.')


class UserSignupForm(FlaskForm):
    username = StringField('Username',
                            validators=[DataRequired(), Length(min=2, max=50)],
                            render_kw=dict(placeholder='Username'))
    password = PasswordField('Password',
                             validators=[DataRequired()],
                             render_kw=dict(placeholder='Password'))
    password_repeat = PasswordField('Repeat Password',
                                    validators=[DataRequired()],
                                    render_kw=dict(placeholder='Password'))
    submit = SubmitField('Sign up')

    def validate_username(self, field):
        user = get_user_by_user_name(self.username.data)
        if user:
            raise ValidationError('Username is already taken.')

    def validate_password(self, field):
        if self.password.data != self.password_repeat.data:
            raise ValidationError('Passwords do not match.')


class AddSightingForm(FlaskForm):
    title = StringField('Title',
                            validators=[DataRequired(), Length(min=0, max=5000)],
                            render_kw=dict(placeholder='Title'))
    latitude = StringField('Latitude',
                            validators=[DataRequired(), Length(min=0, max=5000)],
                            render_kw=dict(placeholder='Latitude'))
    longitude = StringField('Longitude',
                            validators=[DataRequired(), Length(min=0, max=5000)],
                            render_kw=dict(placeholder='Longitude'))

    submit = SubmitField('Add Sighting')
    def validate_latitude(self, field):
        try:
            latitude = float(field.data)
        except ValueError:
            raise ValidationError('Latitude must be a number.')
        if latitude < -90 or latitude > 90:
                raise ValidationError('Latitude must be between -90 and 90.')

    def validate_longitude(self, field):
        try:
            longitude = float(field.data)
        except ValueError:
            raise ValidationError('Longitude must be a number.')
        if longitude < -180 or longitude > 180:
                raise ValidationError('Longitude must be between -180 and 180.')


class SearchSightingForm(FlaskForm):
    search_text = StringField('Search Text',
                            validators=[DataRequired(), Length(min=0, max=5000)],
                            render_kw=dict(placeholder='Search Text'))
    submit = SubmitField('Search Sighting')
    reset = SubmitField('Show All Sightings')


class BackToMainForm(FlaskForm): submit = SubmitField('Main Menu')