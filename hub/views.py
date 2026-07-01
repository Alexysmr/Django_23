from django.views.generic import TemplateView
from auxiliary.constants import PORTAL_APPS

class HubView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['apps'] = PORTAL_APPS
        return context
