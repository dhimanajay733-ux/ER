import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from src.core.config import settings


# SEND OTP EMAIL
def send_otp_email(
    receiver_email: str,
    otp_code: str
):

    # EMAIL SUBJECT
    subject = "Your OTP Verification Code"

    # EMAIL BODY
    body = f"""
Hello,

Your OTP verification code is:

{otp_code}

This OTP will expire in 5 minutes.

If you did not request this, please ignore this email.

Thank You.
"""

    # CREATE EMAIL MESSAGE
    message = MIMEMultipart()

    message["From"] = settings.smtp_email

    message["To"] = receiver_email

    message["Subject"] = subject

    # ATTACH BODY
    message.attach(
        MIMEText(body, "plain")
    )

    try:

        # CONNECT TO SMTP SERVER
        server = smtplib.SMTP(
            settings.smtp_host,
            settings.smtp_port
        )

        # START TLS ENCRYPTION
        server.starttls()

        # LOGIN TO SMTP
        server.login(
            settings.smtp_email,
            settings.smtp_password
        )

        # SEND EMAIL
        server.sendmail(
            settings.smtp_email,
            receiver_email,
            message.as_string()
        )

        print("OTP email sent successfully")

    except Exception as e:

        print(f"Email sending failed: {e}")

        raise e

    finally:

        # CLOSE SMTP CONNECTION
        server.quit()