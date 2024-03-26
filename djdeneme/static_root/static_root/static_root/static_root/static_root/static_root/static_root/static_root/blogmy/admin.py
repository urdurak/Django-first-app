from django.contrib import admin
from blogmy.models import myblogger, Comment , FavoriteBlog
# Register your models here.

admin.site.register(myblogger)
admin.site.register(Comment)
admin.site.register(FavoriteBlog)