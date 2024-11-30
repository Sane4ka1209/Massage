from django.contrib import admin
from .models import Master, MasterTime
# Register your models here.

class MasterTImeInline(admin.TabularInline):
    model = MasterTime
    extra = 1

@admin.register(Master)
class MasterAdmin(admin.ModelAdmin):
    inlines = [MasterTImeInline]
