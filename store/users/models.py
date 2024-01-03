from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.db import models
from django.urls import reverse
from django.utils.timezone import now

from conf.settings import DOMAIN_NAME, EMAIL_HOST_USER


class User(AbstractUser):
    image = models.ImageField(upload_to='profile_images/%Y/%m/%d/', verbose_name='Аватар пользователя', null=True,
                              blank=True)
    is_verified_email = models.BooleanField(default=False)


class EmailVerification(models.Model):
    code = models.UUIDField(unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    expiration = models.DateTimeField()

    def __str__(self):
        return f'EmailVerification object for {self.user.email}'

    def send_verification_email(self):
        link = reverse('users:email_verification', kwargs={'email': self.user.email, 'code': self.code})
        verification_link = f'{DOMAIN_NAME}{link}'
        subject = f'Подтвеждение учетной записи для {self.user.username}'
        message = f'Для подтверждения учетной записи для {self.user.email} перейдите по ссылке: {verification_link}'
        send_mail(
            subject=subject,
            message=message,
            from_email=EMAIL_HOST_USER,
            recipient_list=[self.user.email],
            fail_silently=False,
        )

    def is_expired(self):
        return True if now() >= self.expiration else False
