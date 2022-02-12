from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from os import environ
from smtplib import SMTP


def compose_body(file_name: str, info: dict[str, str]) -> MIMEText:
    template = open(f"../templates/${file_name}")
    mail_body = MIMEText(template.read().format(info), "html")
    template.close()
    return mail_body


def load_logo() -> MIMEImage:
    logo = open("../templates/img/logo.png", "rb")
    mail_logo = MIMEImage(logo.read())
    mail_logo.add_header("Content-ID", "logo@fasthome")
    logo.close()
    return mail_logo


def compose_mail(subject: str, mail_to: str, template_file: str, template_info: dict[str, str]) -> MIMEMultipart:
    mail = MIMEMultipart()
    mail["Subject"] = subject
    mail["From"] = environ["MAIL_ADDR"]
    mail["To"] = mail_to

    mail.attach(compose_body(template_file, template_info))
    mail.attach(load_logo())
    return mail


def send_email(subject: str, mail_to: str, template_file: str, template_info: dict[str, str]):
    mail = compose_mail(subject, mail_to, template_file, template_info)
    sender = SMTP(environ["MAIL_SERVER"], int(environ["MAIL_PORT"]))
    sender.login(environ["MAIL_ADDR"], environ["MAIL_PASS"])
    sender.sendmail(environ["MAIL_ADDR"], mail_to, mail.as_string())
    sender.quit()
