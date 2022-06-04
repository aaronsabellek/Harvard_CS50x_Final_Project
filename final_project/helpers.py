import os
import secrets
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer
from PIL import Image

from final_project import app, mail


# Confirm token with expiration time of 1h
def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        email = serializer.loads(token, salt=app.config['SECURITY_PASSWORD_SALT'], max_age=expiration)
    except:
        return False
    return email

# Generate confirmation token
def generate_confirmation_token(email):
    s = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return s.dumps(email, salt=app.config['SECURITY_PASSWORD_SALT'])

# Save uploaded profile image
def save_picture(form_picture):
    # Upload image
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    
    # Resize image
    output_size = (400,400)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    
    # Save image
    i.save(picture_path)
    return picture_fn

# Send email
def send_email(to, subject, template):
    msg = Message(subject, recipients=[to], html=template, sender=app.config['MAIL_DEFAULT_SENDER'])
    mail.send(msg)