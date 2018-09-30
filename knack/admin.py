from django.contrib import admin

from .models import Blog, BlogAdmin, Post, PostAdmin, Resource, ResourceAdmin

admin.site.register(Blog, BlogAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Resource, ResourceAdmin)
