from django.contrib import admin

# Register your models here.

from .models import Thread, Topic, Comment, User

admin.site.register(User)
admin.site.register(Thread)
admin.site.register(Topic)
admin.site.register(Comment)