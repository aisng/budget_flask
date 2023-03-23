import os
import secrets
from PIL import Image
from flask import current_app, url_for
from . import mail
from flask_mail import Message


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(
        current_app.root_path, "static/profile_pics", picture_fn
    )

    output_size = (125, 125)
    i = Image.open(form_picture)
    i = i.resize(output_size)
    i.save(picture_path)

    return picture_fn


def amount_conversion(amount_data, amount_type_data=None):
    """if amount_type_data is not None, converts the user input amount (float) to cents (int)
    and returns positive or negative amount value based on amount_type_data.
    if amount_type_data is None, converts the value in cents (int) stored in the database to display to the user as a float
    """
    if type(amount_data) is float and amount_type_data:
        amount_data = int(amount_data * 100)
        if amount_type_data == "expense":
            amount_data = -abs(amount_data)
        elif amount_type_data == "income":
            amount_data = abs(amount_data)
    elif type(amount_data) is int and not amount_type_data:
        amount_data = float(round(amount_data / 100, 2))
        if amount_data < 0:
            amount_data = abs(amount_data)
    return amount_data


def send_reset_email(user):
    token = user.get_reset_token()
    print(current_app.config["MAIL_USERNAME"])
    msg = Message(
        "Password reset request",
        sender=current_app.config["MAIL_USERNAME"],
        recipients=[user.email],
    )
    msg.body = f"""To reset your password, go to: {url_for('auth.reset_password', token=token, _external=True)}
    If you didn't request a password reset, ignore this message."""
    mail.send(msg)
