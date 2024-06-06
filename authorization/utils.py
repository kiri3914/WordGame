from django.core.mail import send_mail
from django.conf import settings
import random
import string


def send_code_email(user):
    code = ''.join(random.sample(string.digits, 6))
    user.auth_code = code
    user.save()
    subject = '注册验证码'
    message = '您的验证码是：' + code
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [user.email]
    send_mail(subject, message, from_email, recipient_list)