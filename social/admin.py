from django.contrib import admin
from .models import Comment, Like, ReComment

# Register your models here.


admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(ReComment)