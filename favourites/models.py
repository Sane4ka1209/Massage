from django.db import models
from accounts.models import custom_user_foreign_key
from masters.models import Master
# Create your models here.

class ClientFavourites(models.Model):
    client = models.OneToOneField(
        custom_user_foreign_key(),
        on_delete=models.CASCADE,
        primary_key=True,
        verbose_name='Клиент',
        related_name='favourites'
    )
    masters = models.ManyToManyField(
        Master,
        verbose_name='Массажисты',
        related_name='favourites'
    )

    def __str__(self) -> str:
        return self.client

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'