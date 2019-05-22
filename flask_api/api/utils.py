import hashlib
from flask_mail import Message
from flask_api.app import mail, app
from flask_api.api.restplus import async


def send_sms(phone_number, validate_number):
    """
    发送短信
    :param phone_number:
    :param validate_number:
    :return:
    """
    return True, ""


def encrypted_password(password):
    """
    对密码非对称加密
    :param password:
    :return:
    """
    password = "salt" + password + "sugar"
    md5 = hashlib.md5()
    md5.update(password.encode("utf-8"))
    return md5.hexdigest()


@async
def send_async_email(_app, msg):
    with _app.app_context():
        mail.send(msg)


def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    send_async_email(app, msg)
