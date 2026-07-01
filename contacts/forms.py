from django import forms

from .models import Contact
from auxiliary.constants import FIELD_ATTRIBUTES, REPLACEMENT_PLACEHOLDERS


class BootstrapFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            model_field = self._meta.model._meta.get_field(field_name)
            attrs = FIELD_ATTRIBUTES.get(type(model_field), {})
            for attr_name, attr_value in attrs.items():
                field.widget.attrs.setdefault(attr_name, attr_value)
            field.widget.attrs.setdefault('class', 'form-control')
            placeholder = REPLACEMENT_PLACEHOLDERS.get(field_name, field.label or field_name)
            placeholder = placeholder[0].lower() + placeholder[1:]
            field.widget.attrs['placeholder'] = f'Введите {placeholder}'


class ContactForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['username', 'phone', 'email', 'message']
        labels = {
            'username': 'Ваше имя',
            'phone': 'Телефон',
            'email': 'Email',
            'message': 'Сообщение',
        }
