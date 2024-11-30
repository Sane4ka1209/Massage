from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

app_name = 'appointments'

urlpatterns = [
    path('new/select_master/', login_required(views.SelectMasterView.as_view()), name='select_master'),
    path('new/select_master/<str:name>/', login_required(views.SelectedMaster.as_view()), name='selected_master'),
    path('new/select_services/', login_required(views.SelectServicesView.as_view()), name='select_services'),
    path('new/select_services/add/<str:name>/',login_required( views.AddedService.as_view()), name='add_service'),
    path('new/select_services/remove/<str:name>/', login_required(views.RemovedService.as_view()), name='remove_service'),
    path('new/select_date/', login_required(views.SelectDateView.as_view()), name='select_date'),
    path('new/select_date/<str:date>/', login_required(views.SelectedDate.as_view()), name='selected_date'),
    path('new/select_time/', login_required(views.SelectTimeView.as_view()), name='select_time'),
    path('new/success/<int:id>/', login_required(views.SuccessView.as_view()), name='success'),
    path('new/error/', login_required(views.ErrorView.as_view()), name='error'),
    path('new/select_time/<str:time>/', login_required(views.SelectedTime.as_view()), name='selected_time'),
    path('list/', login_required(views.AppointmentsView.as_view()), name='list'),
    path('<int:id>/', login_required(views.AppointmentDetailView.as_view()), name='detail'),
    path('<int:id>/confirm/', login_required(views.AppointmentConfirmView.as_view()), name='confirm'),
    path('confirmed/', login_required(views.AppointmentConfirmedView.as_view()), name='confirmed'),
    path('<int:id>/cancel/', login_required(views.AppointmentCancelView.as_view()), name='cancel'),
    path('canceled/', login_required(views.AppointmentCanceledView.as_view()), name='canceled'),
]