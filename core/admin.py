from django.contrib import admin
from .models import Post


class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ('id', 'title', 'published', 'created_at')


admin.site.register(Post, PostAdmin)
