from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

app_name = 'visits'

urlpatterns = [
    path('list/', login_required(views.VisitsView.as_view()), name='list'),
    path('<int:id>/', login_required(views.VisitDetailView.as_view()), name='detail'),
]