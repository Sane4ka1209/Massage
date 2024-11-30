from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

app_name = 'favourites'

urlpatterns = [
    path('list/', login_required(views.ClientFavouritesView.as_view()), name='list'),
    path('add/<str:master_name>', login_required(views.AddFavouriteView.as_view()), name='add'),
    path('remove/<str:master_name>', login_required(views.RemoveFavouriteView.as_view()), name='remove')
]