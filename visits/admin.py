from django.contrib import admin
from .models import Visit
from mainpage.admin import ReadOnlyAdmin
# Register your models here.

class VisitAdmin(ReadOnlyAdmin):
    model = Visit

admin.site.register(Visit, VisitAdmin)