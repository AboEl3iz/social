from django.contrib import admin
from .models import Post, Comment, Like, Category, Tag, Report, Block

# Register your models here.

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Report)
admin.site.register(Block)
