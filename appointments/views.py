from typing import Any
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.http import HttpRequest
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, RedirectView, TemplateView, DetailView
from masters.models import Master, MasterTime
from .appointment import OAppointment
from services.models import Service
from favourites.models import ClientFavourites
from accounts.models import custom_user
from django.urls import reverse
from working_schedule.models import get_free_time
from datetime import timedelta, datetime
from appointments.models import Appointment
from visits.models import Visit

# Create your views here.

class SelectMasterView(ListView):
    template_name = 'appointment/select_master.html'
    model = Master

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = {}
        context['object_list'] = Master.objects.filter(is_works = True)
        cf = ClientFavourites.objects.filter(client = custom_user(self.request))
        context['favourites'] = cf[0].masters.all() if cf else []
        return context

class SelectedMaster(RedirectView):
    http_method_names = ['post']

    def get_redirect_url(self, *args: Any, **kwargs: Any) -> str | None:
        return reverse('appointments:select_services')
    
    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        appointment = OAppointment(request)
        appointment.set_master(get_object_or_404(Master, name = kwargs['name']))
        return super().post(request, *args, **kwargs)

class AddedService(RedirectView):
    http_method_names = ['post']

    def get_redirect_url(self, *args: Any, **kwargs: Any) -> str | None:
        return reverse('appointments:select_services')
    
    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        appointment = OAppointment(request)
        appointment.add_service(get_object_or_404(Service, name = kwargs['name']))
        return super().post(request, *args, **kwargs)

class RemovedService(RedirectView):
    http_method_names = ['post']

    def get_redirect_url(self, *args: Any, **kwargs: Any) -> str | None:
        return reverse('appointments:select_services')
    
    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        appointment = OAppointment(request)
        appointment.remove_service(get_object_or_404(Service, name = kwargs['name']))
        return super().post(request, *args, **kwargs)

class SelectServicesView(ListView):
    template_name = 'appointment/select_services.html'
    model = MasterTime

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = {}
        appointment = OAppointment(self.request)
        context['object_list'] = MasterTime.objects.filter(master = appointment.get_master())
        context['appointment'] = appointment
        return context
    
class SelectDateView(TemplateView):
    template_name = 'appointment/select_date.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = {}
        context['dates'] = []
        appointment = OAppointment(self.request)
        context['appointment'] = appointment
        for i in range(0, 15):
            if get_free_time(datetime.now() + timedelta(days=i), appointment.get_all_duration()):
                context.get('dates').append((datetime.now() + timedelta(days=i)).date())
        return context

class SelectedDate(RedirectView):
    http_method_names=['post']

    def get_redirect_url(self, *args: Any, **kwargs: Any) -> str | None:
        return reverse('appointments:select_time')
    
    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        appointment = OAppointment(self.request)
        appointment.set_date(kwargs['date'])
        return super().post(request, *args, **kwargs)

class SelectTimeView(TemplateView):
    template_name = 'appointment/select_time.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = {}
        appointment = OAppointment(self.request)
        context['appointment'] = appointment
        context['times'] = get_free_time(appointment.get_date(), appointment.get_all_duration())
        return context

class SelectedTime(RedirectView):
    http_method_names=['post']

    def get_redirect_url(self, *args: Any, **kwargs: Any) -> str | None:
        appointment = OAppointment(self.request)
        appointment.set_time(kwargs['time'])
        ap = appointment.create_appointment(custom_user(self.request))
        if ap:
            return reverse('appointments:success', kwargs={'id': ap.id})
        else:
            return reverse('appointments:error')

class SuccessView(DetailView):
    template_name = 'appointment/success.html'
    model = Appointment
    
    def get_object(self, queryset: QuerySet[Any] | None = ...) -> Model:
        return get_object_or_404(Appointment, id = self.kwargs['id'])

class ErrorView(TemplateView):
    template_name = 'appointment/error.html'

class AppointmentsView(ListView):
    model = Appointment
    template_name = 'appointment/list.html'

    def get_queryset(self) -> QuerySet[Any]:
        return Appointment.objects.filter(client = custom_user(self.request))

class AppointmentDetailView(DetailView):
    template_name='appointment/detail.html'
    model = Appointment

    def get_object(self, queryset: QuerySet[Any] | None = ...) -> Model:
        return get_object_or_404(Appointment, id = self.kwargs['id'])

class AppointmentConfirmedView(TemplateView):
    template_name='appointment/confirmed.html'

class AppointmentConfirmView(RedirectView):
    http_method_names=['post']

    def get_redirect_url(self, *args: Any, **kwargs: Any) -> str | None:
        appointment = get_object_or_404(Appointment, id = kwargs['id'])
        new_visit = Visit(
            client = appointment.client,
            master = appointment.master,
            start_time = appointment.start_time,
            end_time = appointment.start_time + timedelta(minutes=appointment.get_all_duration()),
            all_price = appointment.get_all_price()
        )
        new_visit.save()
        new_visit.services.set(appointment.services.all())
        new_visit.save()
        appointment.delete()
        return reverse('appointments:confirmed')

class AppointmentCanceledView(TemplateView):
    template_name='appointment/canceled.html'

class AppointmentCancelView(RedirectView):
    http_method_names=['post']
    def get_redirect_url(self, *args: Any, **kwargs: Any) -> str | None:
        get_object_or_404(Appointment, id = kwargs['id']).delete()
        return reverse('appointments:canceled')