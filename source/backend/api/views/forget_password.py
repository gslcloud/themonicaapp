import random
import string
import smtplib
from email.message import EmailMessage

from flask import Flask, request
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

def validate_email(email):
    # Validate the format and existence of the email address
    # Implement the email validation logic here

def generate_token(length=8):
    chars = string.ascii_letters + string.digits
    token = ''.join(random.choice(chars) for _ in range(length))
    return token

def send_password_reset_email(email, token):
    subject = "Password Reset"
    body = f"Click the link below to reset your password: \n\n{request.url_root}/reset/{token}"

    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['From'] = os.getenv('EMAIL_USERNAME')
    msg['To'] = email

    try:
        with smtplib.SMTP(os.getenv('EMAIL_SERVER'), os.getenv('EMAIL_PORT')) as server:
            server.starttls()
            server.login(os.getenv('EMAIL_USERNAME'), os.getenv('EMAIL_PASSWORD'))
            server.send_message(msg)
        return True
    except Exception as e:
        # Log the error
        app.logger.error(f"Error sending email: {str(e)}")
        return False

@app.route('/forget_password', methods=['POST'])
def forget_password():
    email = request.json.get('email')

    if validate_email(email):
        token = generate_token()
        if send_password_reset_email(email, token):
            return "Password reset email sent"
        else:
            return "Failed to send password reset email", 500
    else:
        return "Invalid email address", 400

if __name__ == '__main__':
    app.run()