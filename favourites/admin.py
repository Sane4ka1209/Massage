from django.contrib import admin
from mainpage.admin import ReadOnlyAdmin
from .models import ClientFavourites
# Register your models here.

class ClientFavouritesAdmin(ReadOnlyAdmin):
    model = ClientFavourites

admin.site.register(ClientFavourites, ClientFavouritesAdmin)