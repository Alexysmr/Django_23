from django import forms
from blog.models import BlogPost


class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'content', 'preview', 'published']
        labels = {
            'title': 'Заголовок',
            'content': 'Пост',
            'preview': 'Изображение',
            'published': 'Опубликовать',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 15}),
            'preview': forms.FileInput(attrs={'class': 'form-control'}),
        }