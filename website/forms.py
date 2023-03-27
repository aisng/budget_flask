from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import (
    StringField,
    FloatField,
    PasswordField,
    RadioField,
    SubmitField,
    BooleanField,
)
from wtforms.validators import (
    DataRequired,
    ValidationError,
    EqualTo,
    NumberRange,
    Email,
)
from website.models import User
from flask_login import current_user


class RegistrationForm(FlaskForm):
    username = StringField(
        "Username", validators=[DataRequired(message="Required field.")]
    )
    email = StringField("E-mail", validators=[DataRequired(message="Required field.")])
    password = PasswordField(
        "Password", validators=[DataRequired(message="Required field.")]
    )
    password_confirm = PasswordField(
        "Confirm password", validators=[EqualTo("password", "Passwords must match.")]
    )
    submit = SubmitField("Signup")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("Username already taken.")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("E-mail already taken.")


class LoginForm(FlaskForm):
    email = StringField("E-mail", validators=[DataRequired(message="Required field.")])
    password = PasswordField(
        "Password", validators=[DataRequired(message="Required field.")]
    )
    remember_me = BooleanField("Remember me")
    submit = SubmitField("Login")


class UpdateProfileForm(FlaskForm):
    username = StringField(
        "Username", validators=[DataRequired(message="Required field.")]
    )
    email = StringField("E-mail", validators=[DataRequired(message="Required field.")])
    picture = FileField(
        "Update profile picture",
        validators=[
            FileAllowed(["jpg", "png"], message="Only .jpg or .png files accepted.")
        ],
    )

    submit = SubmitField("Update")

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError("Username already taken.")

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError("E-mail already taken.")


class EntryForm(FlaskForm):
    amount = FloatField(
        "Amount",
        validators=[DataRequired(message="Required field."), NumberRange(min=0.01)],
    )
    entry_type = RadioField(
        "Type", choices=[("income", "Income"), ("expense", "Expense")], default="income"
    )

    submit = SubmitField("Submit")


class RequestResetForm(FlaskForm):
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    submit = SubmitField("Send")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError("No profile for this E-mail")


class ResetPasswordForm(FlaskForm):
    password = PasswordField("Password", validators=[DataRequired()])
    password_confirm = PasswordField(
        "Confirm password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Reset password")
