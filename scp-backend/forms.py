from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional

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
    type = StringField('Type', validators=[Optional()])
    max_capacity = IntegerField('Max Capacity', validators=[DataRequired()])
    security_level = IntegerField('Security Level', validators=[DataRequired()])
    equipment_list = TextAreaField('Equipment List', validators=[Optional()])
    cleaning_schedule = TextAreaField('Cleaning Schedule', validators=[Optional()])
    maintenance_schedule = TextAreaField('Maintenance Schedule', validators=[Optional()])
    submit = SubmitField('Save Camera')

class ObjectForm(FlaskForm):
    name = StringField('Object Name', validators=[DataRequired(), Length(1, 256)])
    description = TextAreaField('Description', validators=[Optional()])
    storage_requirements = TextAreaField('Storage Requirements', validators=[Optional()])
    camera_id = IntegerField('Camera ID', validators=[Optional()])
    submit = SubmitField('Save Object')

class EventForm(FlaskForm):
    type = StringField('Event Type', validators=[DataRequired(), Length(1, 64)])
    notes = TextAreaField('Notes', validators=[Optional()])
    submit = SubmitField('Log Event')
