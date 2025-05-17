import smtplib
import imaplib
import email
from email.mime.text import MIMEText
from utils.config_loader import load_config
from utils.logger import get_logger

logger = get_logger("email_manager")

class EmailManager:
    def __init__(self):
        config = load_config()
        self.email_address = config.get("email_address")
        self.email_password = config.get("email_password")

    def run(self, *args, **kwargs):
        """Main execution method for the plugin"""
        if not args:
            return "Available commands: send <recipient> <subject> <body>, check"
            
        command = args[0].lower()
        if command == "send" and len(args) >= 4:
            return self.send_email(args[1], args[2], " ".join(args[3:]))
        elif command == "check":
            return "\n".join(self.check_inbox())
        else:
            return f"Unknown command: {command}"

    def send_email(self, recipient, subject, body):
        try:
            msg = MIMEText(body)
            msg["Subject"] = subject
            msg["From"] = self.email_address
            msg["To"] = recipient

            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                smtp.login(self.email_address, self.email_password)
                smtp.send_message(msg)
            logger.info(f"Email sent to {recipient}")
            return "✅ Email sent successfully!"
        except Exception as e:
            logger.error(f"Failed to send email: {e}")
            return f"Failed to send email: {e}"

    def check_inbox(self):
        try:
            with imaplib.IMAP4_SSL("imap.gmail.com") as mail:
                mail.login(self.email_address, self.email_password)
                mail.select("inbox")
                _, data = mail.search(None, "ALL")
                mail_ids = data[0].split()[-5:]  # Get last 5 emails
                emails = []
                for num in mail_ids:
                    _, msg_data = mail.fetch(num, "(RFC822)")
                    raw_email = msg_data[0][1]
                    msg = email.message_from_bytes(raw_email)
                    emails.append(f"📩 From: {msg['From']} - Subject: {msg['Subject']}")
                logger.info(f"Fetched {len(emails)} emails")
                return emails or ["Inbox empty."]
        except Exception as e:
            logger.error(f"Failed to fetch inbox: {e}")
            return [f"Failed to fetch inbox: {e}"]

# Module-level run function required by plugin manager
def run(*args, **kwargs):
    email_manager = EmailManager()
    return email_manager.run(*args, **kwargs)
