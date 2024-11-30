from django.db import models
from django.core.exceptions import ValidationError
from datetime import time, timedelta, date, datetime
from django.conf import settings
from datetimerange import DateTimeRange
import math

# Create your models here.
weekdays = [
    'Понедельник',
    'Вторник',
    'Среда',
    'Четверг',
    'Пятница',
    'Суббота',
    'Воскресенье',
]

class Rule(models.Model):
    RULECHOICES = (
        ('Будни', 'Будни'),
        ('Выходные', 'Выходные'),
        ('Понедельник', 'Понедельник'),
        ('Вторник', 'Вторник'),
        ('Среда', 'Среда'),
        ('Четверг', 'Четверг'),
        ('Пятница', 'Пятница'),
        ('Суббота', 'Суббота'),
        ('Воскресенье', 'Воскресенье')
    )

    name = models.CharField(
        choices=RULECHOICES,
        verbose_name='Название',
        primary_key=True,
        max_length=15,
        help_text='''
Правила на конкретные дни недели главнее чем правила на будни или выходные,
по умолчанию по выходным не работает
'''
    )
    day_start_time = models.TimeField(
        verbose_name='Время начала рабочего дня',
        help_text='По умолчанию 8:00',
        blank=True,
        null=True
    )
    day_end_time = models.TimeField(
        verbose_name='Время завершения рабочего дня',
        help_text='По умолчанию 18:00',
        blank=True,
        null=True
    )
    lunch_break_start_time = models.TimeField(
        verbose_name='Время начала обеденнего перерыва',
        help_text='По умолчанию 12:00',
        blank=True,
        null=True
    )
    lunch_break_end_time = models.TimeField(
        verbose_name='Время завершения обеденнего перерыва',
        help_text='По умолчанию 14:00',
        blank=True,
        null=True
    )
    enable_lunch_break = models.BooleanField(
        default=True,
        verbose_name='Есть ли обеденный перерыв'
    )
    is_works = models.BooleanField(
        default=True,
        verbose_name='Работает ли в эти дни'
    )

    class Meta:
        verbose_name='Правило'
        verbose_name_plural='Правила'
    
    def clean(self) -> None:
        super().clean()
        if self.day_start_time and self.day_end_time:
            if self.day_start_time >= self.day_end_time:
                raise ValidationError('Время начала не может быть позже или равно времени завершения')
        if self.enable_lunch_break and self.lunch_break_end_time and self.lunch_break_start_time:
            if self.lunch_break_start_time <= self.day_start_time or self.lunch_break_end_time >= self.day_end_time:
                raise ValidationError('Обеденный перерыв не может выходить за рамки рабочего дня')
            if self.lunch_break_start_time >= self.lunch_break_end_time:
                raise ValidationError('Время начала не может быть позже или равно времени завершения')
    
    def __str__(self) -> str:
        return f'{self.name} = ' + (f'{self.day_start_time or time(8, 0, 0, 0)} - {self.day_end_time or time(18, 0, 0, 0)}' + (f' Обед = {self.lunch_break_start_time or time(12, 0, 0, 0)} - {self.lunch_break_end_time or time(14, 0, 0, 0)}' if self.enable_lunch_break else ' Без обеда') if self.is_works else 'Не работаем')

def get_day_time(weekday: int) -> list|None:
    wd = weekdays[weekday]
    r = Rule.objects.filter(name = wd)
    if r:
        if not r[0].is_works:
            return None
        else:
            return [r[0].day_start_time or time(8, 0, 0, 0), r[0].day_end_time or time(18, 0, 0, 0)]
    else:
        if weekday < 5:
            s = 'Будни'
        else:
            s = 'Выходные'
        r = Rule.objects.filter(name = s)
        if r:
            if not r[0].is_works:
                return None
            else:
                return [r[0].day_start_time or time(8, 0, 0, 0), r[0].day_end_time or time(18, 0, 0, 0)]
        else:
            return [time(8, 0, 0, 0), time(18, 0, 0, 0)]

def get_lunch_break_time(weekday: int) -> list|None:
    wd = weekdays[weekday]
    r = Rule.objects.filter(name = wd)
    if r:
        if not r[0].enable_lunch_break:
            return None
        else:
            return [r[0].lunch_break_start_time or time(12, 0, 0, 0), r[0].lunch_break_end_time or time(14, 0, 0, 0)]
    else:
        if weekday < 5:
            s = 'Будни'
        else:
            s = 'Выходные'
        r = Rule.objects.filter(name = s)
        if r:
            if not r[0].enable_lunch_break:
                return None
            else:
                return [r[0].lunch_break_start_time or time(12, 0, 0, 0), r[0].lunch_break_end_time or time(14, 0, 0, 0)]
        else:
            return [time(12, 0, 0, 0), time(14, 0, 0, 0)]
        
def get_time_step():
    return settings.TIME_STEP

def get_free_time_in_period(period: list, duration: int) -> list:
        def sub(t: time, delta: timedelta) -> time:
            return (datetime.combine(date.today(), t) - delta).time()
        
        if period[0] >= sub(period[1], timedelta(minutes=duration)):
            return []
        p = [period[0], sub(period[1], timedelta(minutes=duration))]
        return [
            i.time() for i in DateTimeRange(datetime.combine(date.today(), p[0]), datetime.combine(date.today(), p[1])).range(timedelta(minutes=get_time_step()))
        ]

def get_free_time(Day: date, duration: int) -> list:
    def get_start_period_time(period: list[time]) -> list[time]|None:
        if Day != date.today():
            return period
        if period[0] < datetime.now().time():
            now = datetime.now()
            hours, minutes = divmod(math.ceil(now.minute/get_time_step())*get_time_step(), 60)
            rounded_time = (now + timedelta(hours=hours)).replace(minute=minutes).time()
            if rounded_time >= period[1]:
                return None
            else:
                return [rounded_time, period[1]]
    times = []
    day = get_day_time(Day.weekday())
    if not day:
        return []
    lunch_break = get_lunch_break_time(Day.weekday())
    if lunch_break:
        periods = []
        period = get_start_period_time([day[0], lunch_break[0]])
        if period: periods.append(period)
        period = get_start_period_time([lunch_break[1], day[1]])
        if period: periods.append(period)
    else:
        period = get_start_period_time([day[0], day[1]])
        if period: periods = [period]
    from appointments.models import Appointment
    appointments = Appointment.objects.filter(start_time__contains = Day)
    for appointment in appointments:
        for i in range(0, len(periods)):
            if periods[i][0] <= appointment.start_time.time() <= periods[i][1]:
                p = periods[i]
                periods[i] = [p[0], appointment.start_time.time()]
                periods.insert(i + 1, [appointment.start_time.time(), p[1]])
                break
    for i in periods:
        times += get_free_time_in_period(i, duration)
    return times