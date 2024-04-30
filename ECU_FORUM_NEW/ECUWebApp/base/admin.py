from django.contrib import admin

# Register your models here.

from .models import Thread, Topic, Comment, User, Room, SocialPost, SocialPage

admin.site.register(User)
admin.site.register(Thread)
admin.site.register(Topic)
admin.site.register(Comment)
admin.site.register(Room)
admin.site.register(SocialPost)
admin.site.register(SocialPage)