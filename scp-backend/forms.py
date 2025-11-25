from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, IntegerField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional

# Canonical SCP classification choices (value, label) in Ukrainian
SCP_CLASS_CHOICES = [
    ('Unspecified', 'Непозначений (сірий)'),
    ('Safe', 'Безпечний (зелений)'),
    ('Euclid', 'Евклід (жовтий)'),
    ('Keter', 'Кетер (червоний)'),
    ('Thaumiel', 'Тауміель (чорний)'),
    ('Exotic', 'Екзотичний (синій)'),
    ('Metaclass', 'Метаклас (рожевий)'),
]

# Basic camera type choices  can be adjusted later
CAMERA_TYPE_CHOICES = [
    ('Surveillance', 'Surveillance'),
    ('Containment', 'Containment Unit'),
    ('Laboratory', 'Laboratory'),
    ('Mobile', 'Mobile Camera'),
    ('External', 'External/Perimeter'),
    ('SecureVault', 'Secure Vault Camera'),
]


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(3, 120)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(6, 128)])
    confirm = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    username = StringField('Username or Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class CameraForm(FlaskForm):
    name = StringField('Camera Name', validators=[DataRequired(), Length(1, 128)])
    type = SelectField('Type', choices=CAMERA_TYPE_CHOICES, validators=[Optional()])
    max_capacity = IntegerField('Max Capacity', validators=[DataRequired()])
    security_level = IntegerField('Security Level', validators=[DataRequired()])
    equipment_list = TextAreaField('Equipment List', validators=[Optional()])
    cleaning_schedule = TextAreaField('Cleaning Schedule', validators=[Optional()])
    maintenance_schedule = TextAreaField('Maintenance Schedule', validators=[Optional()])
    submit = SubmitField('Save Camera')


class ObjectForm(FlaskForm):
    name = StringField('Object Name', validators=[DataRequired(), Length(1, 256)])
    classification = SelectField('Classification', choices=SCP_CLASS_CHOICES, validators=[DataRequired()])
    description = TextAreaField('Description', validators=[Optional()])
    storage_requirements = TextAreaField('Storage Requirements', validators=[Optional()])
    # camera_id is still handled as an integer; templates supply the select options
    camera_id = IntegerField('Camera ID', validators=[Optional()])
    submit = SubmitField('Save Object')


class EventForm(FlaskForm):
    type = StringField('Event Type', validators=[DataRequired(), Length(1, 64)])
    notes = TextAreaField('Notes', validators=[Optional()])
    submit = SubmitField('Log Event')


class AdminUserForm(FlaskForm):
    role = SelectField('Role', choices=[('user','User'), ('admin','Admin')], validators=[DataRequired()])
    access_level = IntegerField('Access Level (0-5)', validators=[DataRequired()])
    submit = SubmitField('Save User')
