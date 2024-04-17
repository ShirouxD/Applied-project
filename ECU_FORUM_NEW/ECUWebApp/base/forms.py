from django.forms import ModelForm
from .models import Thread, SocialPage, User
from django import forms
from django.contrib.auth.forms import UserCreationForm



class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'email','password1', 'password2' ]


class ThreadForm(ModelForm):
    class Meta:
        model = Thread
        fields = '__all__'
        exclude = ['host', 'participants']



################################################################################
# class SocialPageForm(forms.ModelForm):
#     class Meta:
#         model = SocialPage
#         fields = ['image', 'caption']

class SocialPageForm(forms.ModelForm):
    class Meta:
        model = SocialPage
        fields = ['image', 'video', 'caption']
        labels = {
            'image': 'Upload Image',  # Customize the label for the image field
            'video': 'Upload Video',  # Customize the label for the video field
        }

    def clean(self):
        cleaned_data = super().clean()
        image = cleaned_data.get("image")
        video = cleaned_data.get("video")
        
        # Check if neither image nor video is provided
        if not image and not video:
            raise forms.ValidationError("Please upload either an image or a video.")

        return cleaned_data
    
class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'bio', 'avatar']
        