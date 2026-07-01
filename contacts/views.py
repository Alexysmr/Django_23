from django.views.generic import TemplateView
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from .models import Contact
from .forms import ContactForm

class ContactsView(FormView):
    template_name = 'contacts/index.html'
    form_class = ContactForm
    success_url = reverse_lazy('contacts:contact_success')

    def get_context_data(self, **kwargs):
        """Добавление списка контактов в контекст"""
        context = super().get_context_data(**kwargs)
        context['contacts'] = Contact.objects.all().order_by('-created_at')
        return context

    def form_valid(self, form):
        """Обработка валидной формы"""
        contact = form.save()
        self.request.session['last_submission'] = {
            'username': contact.username,
            'message': contact.message,
        }
        print(f'You have new message from {contact.username}({contact.phone}, {contact.email}): {contact.message}')
        return super().form_valid(form)


class ContactSuccessView(TemplateView):
    template_name = 'contacts/answer_by_message.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        last_submission = self.request.session.get('last_submission', {})
        context['username'] = last_submission.get('username', '')
        context['message'] = last_submission.get('message', '')
        return context
