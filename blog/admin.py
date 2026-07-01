from django.contrib import admin

from blog.models import BlogPost


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'content', 'preview', 'published', 'number_of_views')
    search_fields = ('title', 'created_at')
