""" This file contains all Tests about User app """
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .forms import RegisterForm
from .views import redirect
from .models import Profile


class TestUser(TestCase):
    """Test all User app views"""

    def test_register_view(self):
        response = self.client.get(reverse('users:register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')

    def test_bad_register_view(self):
        """Test when information introduced is wrong"""
        response = self.client.post(reverse('users:register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')

    def test_login_view(self):
        response = self.client.get(reverse('users:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_logout_logged_out_view(self):
        """When user is not logged in"""
        response = self.client.get(reverse('users:logout'))
        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed(redirect('login.html'))

    def test_logout_logged_in_view(self):
        """When the user is logged in"""
        user = User.objects.create(username="name")
        self.client.force_login(user)
        response = self.client.get(reverse('users:logout'))
        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed(redirect('index.html'))

    def test_profile_logged_out_view(self):
        """When user is not logged in"""
        response = self.client.get(reverse('users:profile'))
        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed(redirect('login.html'))

    def test_profile_logged_in_view(self):
        """When the user is logged in"""
        user = User.objects.create(username="name")
        profile = Profile.objects.create(user=user)
        self.client.force_login(user)
        response = self.client.get(reverse('users:profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')


class TestUserForms(TestCase):
    """Test User app Form"""

    def test_valid_data(self):
        form = RegisterForm(data={
            'username': 'name',
            'email': 'email@gmail.com',
            'password1': 'Abcdef123!',
            'password2': 'Abcdef123!',
            'gender': 'M',
        })
        if not form.is_valid():
            print(form.errors)
        self.assertTrue(form.is_valid())

    def test_no_valid_data(self):
        """One error in the email given"""
        form = RegisterForm(data={
            'username': 'name',
            'email': 'emailgmail.com',
            'password1': 'bdcef123',
            'password2': 'abdcef123',
            'gender': 'M',
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 2)

    def test_no_data(self):
        """No data at all"""
        form = RegisterForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 5)

    class ProfileModelTest(TestCase):

        def setUp(self):
            self.user = User.objects.create(username='testuser')
            self.profile = Profile.objects.create(user=self.user)

        def test_profile_image_default_male(self):
            self.assertEqual(self.profile.profile_image.name, 'profile_images/default_male.jpg')

    class ProfileViewTest(TestCase):

        def setUp(self):
            self.user = User.objects.create_user(username='testuser', password='12345')
            self.profile = Profile.objects.create(user=self.user)

        def test_profile_view(self):
            self.client.login(username='testuser', password='12345')
            response = self.client.get(reverse('profile'))
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, 'profile.html')

        def test_profile_form_valid(self):
            self.client.login(username='testuser', password='12345')
            form_data = {
                'profile_image': SimpleUploadedFile(name='test_image.jpg',
                                                    content=open('profile_images/default_male.jpg', 'rb').read(),
                                                    content_type='image/jpeg')
            }
            response = self.client.post(reverse('profile'), data=form_data)
            self.profile.refresh_from_db()
            self.assertNotEqual(self.profile.profile_image.name, 'profile_images/default_male.jpg')
            self.assertEqual(response.status_code, 302)

    class ProfileFormTest(TestCase):

        def setUp(self):
            self.user = User.objects.create_user(username='testuser', password='12345')
            self.profile = Profile.objects.create(user=self.user)

        def test_profile_form_valid(self):
            form = ProfileForm(data={'profile_image': SimpleUploadedFile(name='test_image.jpg',
                                                                         content=open('profile_images/default_male.jpg',
                                                                                      'rb').read(),
                                                                         content_type='image/jpeg')})
            self.assertTrue(form.is_valid())