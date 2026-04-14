from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, RedirectView
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.conf import settings

from blog.models import BlogPost
from blog.forms import BlogPostForm
from .utils import send_100_views_congratulation


class BlogView(ListView):
    model = BlogPost
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    paginate_by = 3

    def get_queryset(self):
        admin_mode = self.request.session.get('admin_mode', False)
        if admin_mode:
            return BlogPost.objects.all().order_by('created_at')
        return BlogPost.objects.filter(published=True).order_by('created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['admin_mode'] = self.request.session.get('admin_mode', False)
        return context

class PostDetailView(DetailView):
    """Возвращает пост, увеличивает счётчик просмотров.
    При достижении 100 просмотров отправляет уведомление автору.
    В режиме 'Посетитель' черновики недоступны (фильтруются в get_queryset).
    """
    model = BlogPost
    template_name = 'blog/post_details.html'
    context_object_name = 'post'

    def get_queryset(self):
        admin_mode = self.request.session.get('admin_mode', False)
        if admin_mode:
            return BlogPost.objects.all()
        return BlogPost.objects.filter(published=True)

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        obj = super().get_object(queryset=queryset)
        if obj.published:
            obj.number_of_views += 1
            obj.save(update_fields=['number_of_views'])
            if obj.number_of_views == 100:
                send_100_views_congratulation(obj)
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['admin_mode'] = self.request.session.get('admin_mode', False)
        return context

class PostCreateView(CreateView):
    model = BlogPost
    form_class = BlogPostForm
    template_name = 'blog/post_create.html'
    success_url = reverse_lazy('blog:index')

class PostEditView(UpdateView):
    model = BlogPost
    form_class = BlogPostForm
    template_name = 'blog/post_update.html'
    context_object_name = 'post'

    def get_success_url(self):
        return reverse_lazy('blog:details', kwargs={'pk': self.object.pk})

class PostDeleteView(DeleteView):
    model = BlogPost
    template_name = 'blog/post_delete.html'
    context_object_name = 'post'
    success_url = reverse_lazy('blog:index')

class ToggleModeView(RedirectView):
    url = reverse_lazy('blog:index')

    def get(self, request, *args, **kwargs):
        current = request.session.get('admin_mode', False)
        request.session['admin_mode'] = not current
        return super().get(request, *args, **kwargs)
