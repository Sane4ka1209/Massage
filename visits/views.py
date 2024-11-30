from typing import Any
from django.shortcuts import get_object_or_404
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.views.generic import ListView, DetailView
from .models import Visit
from accounts.models import custom_user
from favourites.models import ClientFavourites

# Create your views here.

class VisitsView(ListView):
    model = Visit
    template_name='visits/list.html'

    def get_queryset(self) -> QuerySet[Any]:
        return Visit.objects.filter(client = custom_user(self.request))

class VisitDetailView(DetailView):
    model = Visit
    template_name='visits/detail.html'

    def get_object(self, queryset: QuerySet[Any] | None = ...) -> Model:
        return get_object_or_404(Visit, client = custom_user(self.request), id = self.kwargs['id'])
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = {}
        context['object'] = kwargs['object']
        fav = ClientFavourites.objects.filter(client = custom_user(self.request))
        if fav:
            context['is_favourite'] = True if context['object'].master in fav[0].masters.all() else False
        else:
            context['is_favourite'] = False
        return context