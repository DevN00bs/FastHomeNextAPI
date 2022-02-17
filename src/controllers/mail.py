from datetime import datetime, timedelta, timezone
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from os import environ
from os.path import join, dirname
from smtplib import SMTP, SMTPException

from jwt import encode

from ..utils.enums import ControllerStatus


def compose_body(file_name: str, info: dict[str, str]) -> MIMEText:
    template = open(join(dirname(__file__), f"../templates/{file_name}"))
    mail_body = MIMEText(template.read().format(**info), "html")
    template.close()
    return mail_body


def load_logo() -> MIMEImage:
    logo = open(join(dirname(__file__), "../templates/img/logo.png"), "rb")
    mail_logo = MIMEImage(logo.read())
    mail_logo.add_header("Content-ID", "<logo@fasthome>")
    logo.close()
    return mail_logo


def compose_mail(subject: str, mail_to: str, template_file: str, template_info: dict[str, str]) -> MIMEMultipart:
    mail = MIMEMultipart()
    mail["Subject"] = subject
    mail["From"] = f"FastHome <{environ['MAIL_ADDR']}>"
    mail["To"] = mail_to

    mail.attach(compose_body(template_file, template_info))
    mail.attach(load_logo())
    return mail


def send_email(subject: str, mail_to: str, template_file: str, template_info: dict[str, str]) -> ControllerStatus:
    try:
        sender = SMTP(environ["MAIL_SERVER"], int(environ["MAIL_PORT"]))
    except SMTPException:
        return ControllerStatus.ERROR

    try:
        sender.login(environ["MAIL_ADDR"], environ["MAIL_PASS"])
        sender.sendmail(environ["MAIL_ADDR"], mail_to,
                        compose_mail(subject, mail_to, template_file, template_info).as_string())
    except SMTPException:
        return ControllerStatus.ERROR
    finally:
        sender.quit()

    return ControllerStatus.SUCCESS


def create_verification_link(user_id: str) -> str:
    verify_token = encode({"id": user_id, "aud": "verify", "exp": (datetime.now(timezone.utc) + timedelta(minutes=11))},
                          environ["JWT_SECRET"])
    return f"{environ['FRONT_URL']}/verify/{verify_token}"
