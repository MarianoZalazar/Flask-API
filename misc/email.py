from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer
from flask import request, url_for, render_template
from apiproject import app, mail

def generate_confirmation_token(email):
    serialized_email = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return serialized_email.dumps(email, salt=app.config['SECURITY_PASSWORD_SALT'])


def validate_token(token, expiration=6600):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        email = serializer.loads(
            token,
            salt=app.config['SECURITY_PASSWORD_SALT'],
            max_age=expiration
        )
    except:
        return False
    return email


def send_mail_confirmation(user):
    token_confirm = generate_confirmation_token(user.email)
    msg = Message(
        "Please Confirm Your Email",
        sender="noreply@demo.com",
        recipients=[user.email],
    )
    url = url_for('app.confirm_email', token=token_confirm, _external=True)
    msg.html = render_template("mail_confirm.html", confirm_url=url)
    mail.send(msg)