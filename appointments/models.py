from django.db import models
from accounts.models import custom_user_foreign_key
from masters.models import Master, MasterTime
from services.models import Service
from datetime import datetime
# Create your models here.

class Appointment(models.Model):
    id = models.AutoField(primary_key=True)
    client = models.ForeignKey(
        custom_user_foreign_key(),
        on_delete = models.CASCADE,
        verbose_name='Клиент'
    )
    master = models.ForeignKey(
        Master,
        on_delete = models.CASCADE,
        verbose_name='Массажист'
    )
    start_time = models.DateTimeField(
        verbose_name='Дата и время начала'
    )
    services = models.ManyToManyField(
        Service,
        verbose_name='Услуги'
    )

    class Meta:
        verbose_name='Запись'
        verbose_name_plural = 'Записи'
    
    def __str__(self):
        return f'{self.client} - {self.master}: {self.start_time.strftime('%d %m %Y / %H:%M')}'

    def get_all_price(self):
        return sum(i.price for i in self.services.all())
    
    def get_all_duration(self):
        return sum(i.time for i in MasterTime.objects.filter(service__in = self.services.all(), master = self.master))
    
    def get_services_with_duration(self):
        return MasterTime.objects.filter(service__in = self.services.all(), master = self.master)
    
    def can_be_confirmed(self):
        return self.start_time.replace(tzinfo=None) <= datetime.now()