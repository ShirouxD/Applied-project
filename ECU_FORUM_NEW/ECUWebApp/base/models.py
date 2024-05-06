from django.db import models
# from django.contrib.auth.models import User
# from django.db.models.deletion import CASCADE
from django.contrib.auth.models import AbstractUser

# Create your models here.

#Model for Notification
class Notification(models.Model):
    title = models.TextField()
    body = models.TextField()
    updated = models.DateTimeField(auto_now= True)
    created = models.DateTimeField(auto_now_add= True)

    class Meta:
       ordering = ['-updated', '-created']

class User(AbstractUser):
    username = models.CharField(max_length=150, unique=True, null=True)
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True, null=True)
    bio = models.TextField(null=True)
    avatar = models.ImageField(null=True, default="avatar.svg")
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    notifications = models.ManyToManyField(Notification, related_name='notifications', blank=True)





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
    pinned = models.BooleanField(default=False)

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
    

class SocialPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    caption = models.TextField()
    image = models.ImageField(upload_to='social_images', null=True, blank=True)
    video = models.FileField(upload_to='social_videos', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

class SocialComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(SocialPost, on_delete=models.CASCADE)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

class Room(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Reservation(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user_id = models.CharField(max_length=100)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.room.name} - {self.date} ({self.start_time} to {self.end_time})"

# Model for Chats
class Chat(models.Model):
    sender = models.ForeignKey(User, related_name='sender', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='receiver', on_delete=models.CASCADE)
    updated = models.DateTimeField(auto_now= True)
    created = models.DateTimeField(auto_now_add= True)


    class Meta:
       ordering = ['-updated', '-created']

# Model for Messages
class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now= True)
    created = models.DateTimeField(auto_now_add= True)


    class Meta:
       ordering = ['-updated', '-created']
    
    def __str__(self):
        return self.body[0:50]