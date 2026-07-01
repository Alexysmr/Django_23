from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import redirect
from django.db.models import Q

from blog.models import BlogPost
from blog.forms import BlogPostForm
from auxiliary.utils import send_100_views_congratulation


class BlogView(ListView):
    model = BlogPost
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    paginate_by = 3

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return BlogPost.objects.filter(published=True).order_by('created_at')
        if self.request.user.has_perm('blog.change_blogpost'):
            return BlogPost.objects.all().order_by('created_at')
        if self.request.user.is_authenticated:
            return BlogPost.objects.filter(Q(published=True) | Q(owner=self.request.user))



class PostDetailView(DetailView):
    """Возвращает посты, увеличивает счётчик просмотров.
    При достижении 100 просмотров отправляет уведомление автору."""
    model = BlogPost
    template_name = 'blog/post_details.html'
    context_object_name = 'post'

    def get_queryset(self):
        if self.request.user.has_perm('blog.change_blogpost'):
            return BlogPost.objects.all()
        if self.request.user.is_authenticated:
            return BlogPost.objects.filter(
                Q(published=True) | Q(owner=self.request.user)
            )
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


class PostCreateView(LoginRequiredMixin, CreateView):
    model = BlogPost
    form_class = BlogPostForm
    success_url = reverse_lazy('blog:index')

    def form_valid(self, form):
        product = form.save(commit=False)
        product.owner = self.request.user
        product.save()
        return super().form_valid(form)


class PostEditView(LoginRequiredMixin, UpdateView):
    model = BlogPost
    form_class = BlogPostForm
    template_name = 'blog/post_update.html'
    context_object_name = 'post'

    def get_success_url(self):
        return reverse_lazy('blog:details', kwargs={'pk': self.object.pk})

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.owner != request.user and not request.user.has_perm('blog.change_blogpost'):
            messages.error(request, "Чтобы редактировать нужно иметь соответствующие права.")
            return redirect('blog:index')
        return super().dispatch(request, *args, **kwargs)


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = BlogPost
    template_name = 'blog/post_delete.html'
    context_object_name = 'post'
    success_url = reverse_lazy('blog:index')

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.owner != request.user and not request.user.has_perm('blog.delete_blogpost'):
            messages.error(request, "Чтобы удалять нужно иметь соответствующие права.")
            return redirect('blog:index')
        return super().dispatch(request, *args, **kwargs)
