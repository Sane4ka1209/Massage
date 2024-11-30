from django.db import models
from services.models import Service
from django.core.validators import MinValueValidator
from working_schedule.models import get_time_step
from django.core.exceptions import ValidationError
# Create your models here.

def time_validator(value):
    if not value is int:
        value = int(value)
    if value % get_time_step() == 0:
        return value
    else:
        raise ValidationError('Это значение должно делить на {} без остатка'.format(get_time_step()))
    

class Master(models.Model):
    name = models.CharField(
        max_length = 50,
        verbose_name='ФИО',
        primary_key=True
    )
    is_works = models.BooleanField(
        default = True,
        verbose_name='Работает'
    )

    class Meta:
        verbose_name='Массажист'
        verbose_name_plural='Массажисты'
    
    def __str__(self) -> str:
        return self.name

class MasterTime(models.Model):
    service = models.ForeignKey(
        Service,
        on_delete = models.CASCADE,
        verbose_name='Услуга'
    )
    master = models.ForeignKey(
        Master,
        on_delete = models.CASCADE,
        verbose_name='Парикмахер'
    )
    time = models.IntegerField(
        validators=[MinValueValidator(0), time_validator],
        verbose_name='Время, мин'
    )

    class Meta:
        verbose_name='Время выполнения'
        verbose_name_plural='Время выполнения'
        constraints = [
            models.UniqueConstraint(fields=['service', 'master'], name='unique_constraint')
        ]
    
    def __str__(self) -> str:
        return f'{self.master}:{self.service} = {self.time}'