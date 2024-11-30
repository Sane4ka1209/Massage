from typing import Any
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, RedirectView
from .models import ClientFavourites
from accounts.models import custom_user
from visits.models import Master

# Create your views here.

class ClientFavouritesView(ListView):
    model = ClientFavourites
    template_name = 'favourites/list.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = {}
        obj = ClientFavourites.objects.filter(client = custom_user(self.request))
        context['object_list'] = obj[0].masters.all() if obj else []
        return context

class AddFavouriteView(RedirectView):
    http_method_names=['post']

    def get_redirect_url(self, *args: Any, **kwargs: Any) -> str | None:
        master = get_object_or_404(Master, name = kwargs['master_name'])
        client = custom_user(self.request)
        fav = ClientFavourites.objects.filter(client = client)
        if not fav:
            fav = ClientFavourites(
                client = client
            )
            fav.save()
            fav.masters.add(master)
            fav.save()
        else:
            fav[0].masters.add(master)
            fav[0].save()
        return self.request.POST.get('next')

class RemoveFavouriteView(RedirectView):
    http_method_names=['post']

    def get_redirect_url(self, *args: Any, **kwargs: Any) -> str | None:
        master = get_object_or_404(Master, name = kwargs['master_name'])
        client = custom_user(self.request)
        fav = ClientFavourites.objects.filter(client = client)
        if fav:
            fav[0].masters.remove(master)
            fav[0].save()
        return self.request.POST.get('next')