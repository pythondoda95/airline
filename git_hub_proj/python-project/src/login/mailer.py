import smtplib
import secrets
import string
from email.mime.text import MIMEText

class Mailer:
    def __init__(self, sender_email, sender_password):
        self.sender_email = sender_email
        self.sender_password = sender_password

    def send_confirmation(self, receiver_email, action="Verification"):
        # Truly random 6-character token
        token = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(6))
        msg = MIMEText(f"Your security token for {action} is: {token}")
        msg['Subject'] = f"Security Token: {token}"
        msg['From'] = self.sender_email
        msg['To'] = receiver_email

        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                server.login(self.sender_email, self.sender_password)
                server.sendmail(self.sender_email, receiver_email, msg.as_string())
            return token 
        except Exception: return None