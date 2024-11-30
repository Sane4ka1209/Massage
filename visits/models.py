from django.db import models
from accounts.models import custom_user_foreign_key
from masters.models import Master
from services.models import Service

# Create your models here.

class Visit(models.Model):
    id = models.AutoField(primary_key=True)
    client = models.ForeignKey(
        custom_user_foreign_key(),
        on_delete=models.CASCADE,
        verbose_name='Клиент'
    )
    master = models.ForeignKey(
        Master,
        on_delete=models.CASCADE,
        verbose_name='Парикмахер'
    )
    start_time = models.DateTimeField(
        verbose_name='Дата и время начала'
    )
    end_time = models.DateTimeField(
        verbose_name='Дата и время окончания'
    )
    all_price = models.DecimalField(
        verbose_name='Стоимость',
        max_digits=6,
        decimal_places=2,
    )
    services = models.ManyToManyField(
        Service,
        verbose_name='Оказанные услуги'
    )

    def __str__(self) -> str:
        return f'{self.client} - {self.master}: {self.start_time.strftime('%d %m %Y / %H:%M')} - {self.end_time.strftime('%d %m %Y / %H:%M')}'
    
    class Meta:
        verbose_name='Посещение'
        verbose_name_plural='Посещения'