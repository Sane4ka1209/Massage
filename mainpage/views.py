from typing import Any
from django.views.generic import TemplateView
from working_schedule.models import get_day_time, get_lunch_break_time, weekdays
# Create your views here.

class MainView(TemplateView):
    template_name = 'main.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = {}
        context['schedule'] = [
            {
                'day': get_day_time(i),
                'lunch_break': get_lunch_break_time(i)
            } for i in range(0, 7)
        ]
        context['weekdays'] = weekdays
        return context