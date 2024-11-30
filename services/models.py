from django.db import models
from django.core.validators import MinValueValidator

# Create your models here.

class Service(models.Model):
    name = models.CharField(
        max_length = 250,
        verbose_name='Название',
        primary_key=True
    )
    price = models.DecimalField(
        verbose_name='Цена',
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(0.0)]
    )
    description = models.TextField(
        blank = True,
        null = True,
        verbose_name='Описание'
    )

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        verbose_name='Услуга'
        verbose_name_plural='Услуги'