import hashlib


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
