from django.contrib import admin
from .models import Appointment
from mainpage.admin import ReadOnlyAdmin
# Register your models here.



class AppointmentAdmin(ReadOnlyAdmin):
    model = Appointment

admin.site.register(Appointment, AppointmentAdmin)