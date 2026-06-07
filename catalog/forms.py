from django import forms

from .models import Product, Contact
from auxiliary.constants import FORBIDDEN_WORDS, TYPE_OF_IMAGE, MAX_IMAGE_SIZE_BYTES, FIELD_ATTRIBUTES, REPLACEMENT_PLACEHOLDERS


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


class ProductForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        labels = {
            'name': 'Наименование товара',
            'description': 'Описание',
            'category': 'Категория',
            'image': f'Изображение (формат {", ".join(TYPE_OF_IMAGE)}, не более {int(MAX_IMAGE_SIZE_BYTES/1048576)} МБ)',
            'price': 'Цена (руб)',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'price' in self.fields:
            self.fields['price'].widget.attrs.update({'min': '0', 'step': '0.01'})

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is None:
            return price
        if price < 0:
            raise forms.ValidationError('Цена не может быть отрицательной')
        return price

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name:
            name_lower = name.lower()
            for word in FORBIDDEN_WORDS:
                if word in name_lower:
                    raise forms.ValidationError(f'Название содержит запрещённое слово: "{word}".')
        return name

    def clean_description(self):
        description = self.cleaned_data.get('description')
        if description:
            desc_lower = description.lower()
            for word in FORBIDDEN_WORDS:
                if word in desc_lower:
                    raise forms.ValidationError(f'Описание содержит запрещённое слово: "{word}".')
        return description

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if not image:
            return image
        new_file = hasattr(image, 'content_type')
        if new_file:
            if image.size > MAX_IMAGE_SIZE_BYTES:
                raise forms.ValidationError(f'Файл не более {MAX_IMAGE_SIZE_BYTES // 1048576} МБ')
            if image.content_type not in [f'image/{fmt.lower()}' for fmt in TYPE_OF_IMAGE]:
                raise forms.ValidationError(f'Допустимы только {", ".join(TYPE_OF_IMAGE)}.')
            return image


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
