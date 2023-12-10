from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.db import models
from django.urls import reverse
from django.utils.timezone import now

from products.models import ProductModel


class CustomUserModel(AbstractUser):
    first_name = models.CharField(max_length=150, blank=False, null=False)
    last_name = models.CharField(max_length=150, blank=False, null=False)
    email = models.EmailField(blank=False, null=False, unique=True)
    latitude = models.FloatField(null=True, blank=True)  # широта координат
    longitude = models.FloatField(null=True, blank=True)  # долгота координат
    address = models.CharField(max_length=250, blank=True, null=True)
    entrance = models.IntegerField(blank=True, null=True)  # подъезд
    floor = models.IntegerField(blank=True, null=True)  # этаж
    apartment = models.IntegerField(blank=True, null=True)  # квартира
    building = models.IntegerField(blank=True, null=True)  # строение/корпус
    baskets = models.ManyToManyField("BasketModel")
    email_verification = models.BooleanField(default=False)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'


class BasketModel(models.Model):
    items = models.ManyToManyField('BasketItem')
    user = models.ForeignKey(
        to=CustomUserModel, on_delete=models.CASCADE, related_name='basket_user', to_field='username'
    )
    creation_date = models.DateTimeField(auto_now_add=True)
    is_delivered = models.BooleanField(default=False)  # Значит, что заказ доставлен
    is_payed = models.BooleanField(default=False)  # Значит, что заказ оплачен
    is_completed = models.BooleanField(default=False)  # Значит, что заказ выполнен
    is_collected = models.BooleanField(default=False)  # Значит, что заказ собран пользователем

    def total_quantity(self):
        return sum(item.quantity for item in self.items.all())

    def total_price(self):
        return sum(item.quantity * item.product.price for item in self.items.all())

    def __str__(self):
        return f"Basket {self.pk} for {self.user.username}"

    class Meta:
        verbose_name = 'корзина'
        verbose_name_plural = 'корзины'


class BasketItem(models.Model):
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    user = models.ForeignKey(
        to=CustomUserModel, on_delete=models.CASCADE, related_name='basket_item_user', to_field='username'
    )
    basket = models.ForeignKey(to=BasketModel, on_delete=models.CASCADE, related_name='basket_item_basket')

    def price(self):
        price = self.quantity * self.product.price
        return price

    def save(self, *args, **kwargs):
        if self.user is not None and self.user.username:
            current_user = get_user_model().objects.get(username=self.user.username)

            try:
                basket = BasketModel.objects.get(
                    user=current_user, is_payed=False, is_collected=False, is_delivered=False, is_completed=False
                )
            except BasketModel.DoesNotExist:
                basket = BasketModel(user=current_user)
                basket.save()
            super().save(*args, **kwargs)
            basket.items.add(self)

    class Meta:
        verbose_name = 'элемент корзины'
        verbose_name_plural = 'элементы корзины'

    def __str__(self):
        return f"{self.product} - {self.quantity}"


class EmailVerification(models.Model):
    code = models.UUIDField(unique=True)
    user = models.ForeignKey(to=CustomUserModel, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    expiration = models.DateTimeField()

    def send_verify_email(self):
        print("Началась задача")
        link = reverse('users:verification', kwargs={'email': self.user.email, 'code': self.code})
        verification_link = f'{settings.DOMAIN_NAME}{link}'
        subject = f'Подтвердите почту для sushifeast.com | {self.user.first_name} {self.user.last_name}'
        message = f'''
        {self.user.first_name} {self.user.last_name}, нажмите на ссылку ниже, чтобы подтвердить вашу почту.
        {verification_link}

        С уважением,
        sushifeast.com
        '''

        send_mail(
            subject=subject, message=message, from_email=settings.EMAIL_HOST_USER,
            recipient_list=[self.user.email], fail_silently=False)
        print(settings.EMAIL_HOST_USER)

    def is_expired(self):
        return True if now() >= self.expiration else False

    def __str__(self):
        return f'Verification for {self.user.email}'

    class Meta:
        verbose_name = 'верификация почты'
        verbose_name_plural = 'верификации почты'
