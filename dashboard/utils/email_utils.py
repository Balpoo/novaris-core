from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods
import smtplib
from email.mime.text import MIMEText


def send_email(subject, body, to_email="saimenscreation@gmail.com"):
    from_email = "bg6227@gmail.com"
    password = "vzzhvtsslpjp yqud"  # Use App Password if Gmail

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = from_email
    msg["To"] = to_email

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(from_email, password)
        server.send_message(msg)

    print(f"✅ Email sent to: {to_email}")
