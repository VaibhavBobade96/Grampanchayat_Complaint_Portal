from flask_wtf import FlaskForm
from wtforms import (
    StringField, PasswordField, SubmitField,
    TextAreaField, SelectField, IntegerField
)
from wtforms.validators import DataRequired, Length, EqualTo, NumberRange, Email
from flask_wtf.file import FileField, FileAllowed

# =========================
# LOGIN FORM
# =========================
class LoginForm(FlaskForm):
    username = StringField(
        'Username',
        validators=[DataRequired(), Length(min=3, max=80)]
    )
    password = PasswordField(
        'Password',
        validators=[DataRequired()]
    )
    role = SelectField(
        'Login As',
        choices=[
            ('citizen', 'Citizen'),
            ('officer', 'Officer'),
            ('admin', 'Admin')
        ],
        validators=[DataRequired()]
    )
    submit = SubmitField('Login')


# =========================
# REGISTER FORM (CITIZEN)
# =========================
class RegisterForm(FlaskForm):
    name = StringField(
        'Full Name',
        validators=[DataRequired(), Length(min=3, max=100)]
    )
    email = StringField(
        'Email Address',
        validators=[DataRequired(), Email(message='Enter a valid email')]
    )
    username = StringField(
        'Username',
        validators=[DataRequired(), Length(min=3, max=80)]
    )
    password = PasswordField(
        'Password',
        validators=[DataRequired(), Length(min=6)]
    )
    confirm_password = PasswordField(
        'Confirm Password',
        validators=[DataRequired(), EqualTo('password', message='Passwords must match')]
    )
    role = SelectField(
        'Register As',
        choices=[('citizen', 'Citizen')],
        validators=[DataRequired()]
    )
    submit = SubmitField('Register')


# =========================
# ADD OFFICER FORM (ADMIN FEATURE)
# =========================
class AddOfficerForm(FlaskForm):
    name = StringField(
        'Full Name',
        validators=[DataRequired(), Length(min=3, max=100)]
    )
    email = StringField(
        'Email Address',
        validators=[DataRequired(), Email(message='Enter a valid email')]
    )
    username = StringField(
        'Username',
        validators=[DataRequired(), Length(min=3, max=80)]
    )
    password = PasswordField(
        'Password',
        validators=[DataRequired(), Length(min=6)]
    )
    role = SelectField(
        'Role',
        choices=[('officer', 'Officer'), ('admin', 'Admin')],
        validators=[DataRequired()]
    )
    submit = SubmitField('Add Officer')


# =========================
# COMPLAINT FORM (Updated Categories & Length)
# =========================
class ComplaintForm(FlaskForm):
    category = SelectField(
        'Complaint Category',
        choices=[
            ('Water Supply', 'Water Supply'),
            ('Electricity', 'Electricity'),
            ('Roads', 'Roads'),
            ('Sanitation', 'Sanitation'),
            ('Street Lights', 'Street Lights'),
            ('Others', 'Others')
        ],
        validators=[DataRequired()]
    )
    ward_no = IntegerField(
        'Ward Number',
        validators=[
            DataRequired(),
            NumberRange(min=1, max=50, message="Enter a valid ward number")
        ]
    )
    description = TextAreaField(
        'Complaint Description',
        validators=[DataRequired(), Length(min=5)]
    )
    photo = FileField(
        'Upload Photo (optional)',
        validators=[FileAllowed(['jpg', 'jpeg', 'png'], 'Images only!')]
    )
    submit = SubmitField('Submit Complaint')

# =========================
# NOTICE FORM (NEW)
# =========================
class NoticeForm(FlaskForm):
    title = StringField(
        'Notice Title', 
        validators=[DataRequired(), Length(min=2, max=200)]
    )
    content = TextAreaField(
        'Notice Content', 
        validators=[DataRequired()]
    )
    submit = SubmitField('Publish Notice')