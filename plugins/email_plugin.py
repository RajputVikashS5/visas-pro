# plugins/email_plugin.py
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

class Plugin:
    def get_tools(self):
        return [{
            "type": "function",
            "function": {
                "name": "send_email",
                "description": "Send an email",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "to": {"type": "string"},
                        "subject": {"type": "string"},
                        "body": {"type": "string"}
                    },
                    "required": ["to", "subject", "body"]
                }
            }
        }]

    def execute(self, function_name, **args):
        if function_name == "send_email":
            # Requires SMTP setup in .env
            try:
                msg = MIMEMultipart()
                msg['From'] = os.getenv('EMAIL_USER')
                msg['To'] = args['to']
                msg['Subject'] = args['subject']
                msg.attach(MIMEText(args['body'], 'plain'))

                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login(os.getenv('EMAIL_USER'), os.getenv('EMAIL_PASS'))
                server.send_message(msg)
                server.quit()
                return "Email sent!"
            except:
                return "Email failed (check .env)"
        return "Error"