from django.db import models
# from django.contrib.auth.models import User
# from django.db.models.deletion import CASCADE
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    username = models.CharField(max_length=150, unique=True, null=True)
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True, null=True)
    bio = models.TextField(null=True)
    avatar = models.ImageField(null=True, default="avatar.svg")
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']





#Model for Topics
class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


#Model for threads
class Thread(models.Model):
    host = models.ForeignKey(User, on_delete = models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete = models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null = True, blank = True)
    participants = models.ManyToManyField(User, related_name='participants', blank=True)
    updated = models.DateTimeField(auto_now= True)
    created = models.DateTimeField(auto_now_add= True)

    class Meta:
       ordering = ['-updated', '-created']

    def __str__(self):
        return self.name
    
#Model for Comments
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now= True)
    created = models.DateTimeField(auto_now_add= True)


    class Meta:
       ordering = ['-updated', '-created']

    def __str__(self):
        return self.body[0:50]


##############################################################################################
class SocialPage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='Social_Images/',null=True, blank=True)
    video = models.FileField(upload_to='Social_videos/', null=True, blank=True)
    caption = models.TextField()

    def __str__(self):
        return f"Post by {self.user.username} on {self.timestamp}"