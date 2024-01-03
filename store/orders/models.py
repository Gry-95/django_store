from django.db import models

from products.models import Basket
from users.models import User


class Order(models.Model):
    CREATED = 0
    PAID = 1
    ON_WAI = 2
    DELIVERED = 3
    STATUS_CHOICES = (
        (CREATED, 'Создан'),
        (PAID, 'Оплачен'),
        (ON_WAI, 'В пути'),
        (DELIVERED, 'Доставлен'),
    )

    first_name = models.CharField(max_length=54, verbose_name='Имя')
    last_name = models.CharField(max_length=64, verbose_name='Фамилия')
    email = models.EmailField(max_length=255, verbose_name='Email')
    address = models.CharField(max_length=255, verbose_name='Адресс')
    basket_history = models.JSONField(default=dict, verbose_name='История заказов')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    status = models.SmallIntegerField(choices=STATUS_CHOICES, default=CREATED)
    initiator = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'Заказ #{self.pk}. {self.first_name} {self.last_name}'

    def update_after_payment(self):
        baskets = Basket.objects.filter(user=self.initiator)
        self.status = self.PAID
        self.basket_history = {
            'purchased_items': [basket.de_json() for basket in baskets],
            'total_sum': float(baskets.total_sum()),
        }
        baskets.delete()
        self.save()
