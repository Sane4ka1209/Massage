from typing import Any
from django.views.generic import ListView
from .models import Service
from masters.models import MasterTime
# Create your views here.


class ServicesView(ListView):
    model = Service
    template_name = 'services/list.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = {}
        context['object_list'] = (
            Service.objects
            .filter(
                name__in = MasterTime.objects.filter(master__is_works = True).values('service_id')
            )
        )
        return context