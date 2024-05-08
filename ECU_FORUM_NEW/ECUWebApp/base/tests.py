from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from unittest import mock

class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.login_url = reverse('login')  

        # Create a test user
        User = get_user_model()  # Get the custom user model
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )

    def test_loginPage_GET(self):
        response = self.client.get(self.login_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'base/login_register.html')

    def test_loginPage_POST_success(self):
        response = self.client.post(self.login_url, {
            'email': 'test@example.com',
            'password': 'testpassword'
        })

        self.assertRedirects(response, reverse('home'))  

    def test_loginPage_POST_invalid_credentials(self):
        response = self.client.post(self.login_url, {
            'email': 'wrong@example.com',
            'password': 'wrongpassword'
        })

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'base/login_register.html')
        self.assertContains(response, 'Username or password does not exist')


from base.models import Thread  
from base.forms import ThreadForm  
from unittest.mock import patch


class TestCreateThread(TestCase):

    def setUp(self):
        self.client = Client()
        self.create_thread_url = reverse('create_thread')
        User = get_user_model()
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')

    def test_createThread_GET(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.create_thread_url)
        self.assertEquals(response.status_code, 302)  
        self.assertRedirects(response, reverse('login') + '?next=' + self.create_thread_url)  

    def test_createThread_POST_valid_form(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(self.create_thread_url, {'topic': 'Test Topic', 'content': 'Test Content'})
        self.assertEquals(response.status_code, 302)  # Expect a redirect
        self.assertRedirects(response, reverse('login') + '?next=' + self.create_thread_url) 

from django.shortcuts import get_object_or_404
from base.models import SocialPost, SocialComment
from base.forms import SocialCommentForm

class TestSocialPost(TestCase):

    def setUp(self):
        self.client = Client()
        User = get_user_model()
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
        self.post = SocialPost.objects.create(user=self.user)

    def test_socialPost_POST_invalid_form(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('social_post', kwargs={'pk': self.post.pk}), {'body': ''})
        self.assertFalse(SocialComment.objects.filter(user=self.user, post=self.post, body='').exists())

    def test_socialPost_POST_valid_form(self):
        self.client.login(username='testuser', password='testpassword')
        User = get_user_model()
        comment_user = User.objects.create_user(username='commentuser', email='comment@example.com', password='testpassword')

        # Mock the request.user attribute to return the desired user object
        with mock.patch('django.contrib.auth.models.AnonymousUser', return_value=comment_user):
            response = self.client.post(reverse('social_post', kwargs={'pk': self.post.pk}), {'body': 'Test Comment'})
            self.assertEquals(response.status_code, 302)

    def test_socialPost_GET(self):
        response = self.client.get(reverse('social_post', kwargs={'pk': self.post.pk}))
        self.assertEquals(response.status_code, 200)  # Expect a successful response


from .forms import MyUserCreationForm
from django.contrib.auth.models import AnonymousUser
from django.contrib.messages.storage.fallback import FallbackStorage

class TestRegisterPage(TestCase):
    
    def setUp(self):
        self.client = Client()
    
    def test_registerPage_GET(self):
        # Test GET request to the register page
        response = self.client.get(reverse('register'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'base/login_register.html')
        self.assertIsInstance(response.context['form'], MyUserCreationForm)
    
    def test_registerPage_POST_valid_form(self):
        # Test POST request with valid form data
        form_data = {
            'name': 'Test user',
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123'
        }
        response = self.client.post(reverse('register'), data=form_data, follow=True)
        self.assertRedirects(response, reverse('home'))
        self.assertTrue(get_user_model().objects.filter(username='testuser').exists())
        self.assertTrue(response.wsgi_request.user.is_authenticated)
    
    def test_registerPage_POST_invalid_form(self):
        # Test POST request with invalid form data
        form_data = {}  # Empty form data
        response = self.client.post(reverse('register'), data=form_data)
        self.assertEquals(response.status_code, 200)
        self.assertFalse(get_user_model().objects.filter(username='').exists())  
        try:
            storage = response.cookies['messages'].value
        except KeyError:
            storage = ''
        self.assertEqual(storage, '')  # Check if error message is present in storage
