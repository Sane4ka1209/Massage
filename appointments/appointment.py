from django.conf import settings
from .models import Appointment, Master, Service
from django.shortcuts import get_object_or_404
from masters.models import MasterTime
from datetime import date, time, datetime, timedelta

class OAppointment:
    def __init__(self, request):
        self.session = request.session
        appointment = self.session.get(settings.APPOINTMENT_SESSION_ID)
        if not appointment:
            appointment = self.session[settings.APPOINTMENT_SESSION_ID] = {}
        self.appointment = appointment
    
    def set_master(self, master: Master):
        self.appointment['master'] = master.name
        self.appointment.pop('services', None)
        self.appointment.pop('date', None)
        self.appointment.pop('time', None)
        self.save()
    
    def get_master(self):
        return get_object_or_404(Master, name = self.appointment.get('master'))
    
    def set_date(self, date):
        self.appointment['date'] = date
        self.appointment.pop('time', None)
        self.save()

    def get_date(self):
        return date.fromisoformat(self.appointment.get('date'))
    
    def set_time(self, time):
        self.appointment['time'] = time
        self.save()

    def get_time(self):
        return time.fromisoformat(self.appointment.get('time'))
    
    def add_service(self, service: Service):
        if not self.appointment.get('services'):
            self.appointment['services'] = [service.name]
            self.save()
            return
        if service.name in self.appointment.get('services'):
            return
        self.appointment.get('services').append(service.name)
        self.save()
    
    def remove_service(self, service: Service):
        if not self.appointment.get('services'):
            return
        if service.name in self.appointment.get('services'):
            self.appointment.get('services').remove(service.name)
            self.save()
    
    def get_services(self):
        if not self.appointment.get('services'):
            return []
        return Service.objects.filter(name__in = self.appointment.get('services'))
    
    def get_services_with_duration(self):
        if not self.appointment.get('services'):
            return []
        return MasterTime.objects.filter(master = self.get_master(), service__in = self.get_services())
    
    def create_appointment(self, client) -> Appointment|None:
        if (
            self.appointment.get('services')
            and self.appointment.get('master')
            and self.appointment.get('date')
            and self.appointment.get('time')
        ):
            start_time = datetime.combine(self.get_date(), self.get_time())
            aps = Appointment.objects.filter(start_time__gte = start_time, start_time__lte = start_time + timedelta(minutes=self.get_all_duration()))
            if aps:
                return None
            appointment = Appointment(
                master = self.get_master(),
                start_time = start_time,
                client = client
            )
            appointment.save()
            appointment.services.set(self.get_services())
            appointment.save()
            return appointment
        return None
    
    def save(self):
        self.session.modified = True
    
    def get_all_duration(self):
        return sum(i.time for i in MasterTime.objects.filter(master = self.get_master(), service__in = self.get_services()))
    
    def get_all_price(self):
        return sum(i.price for i in self.get_services())
