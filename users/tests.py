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
            """Set up a test user and associated profile for use in the tests"""
            self.user = User.objects.create(username='testuser')
            self.profile = Profile.objects.create(user=self.user)

        def test_profile_image_default_male(self):
            """Test that the default profile image for the user is 'default_male.jpg'"""
            self.assertEqual(self.profile.profile_image.name, 'profile_images/default_male.jpg')

    class ProfileViewTest(TestCase):
        def setUp(self):
            """Set up a test user with a known password, and associated profile for use in the tests"""
            self.user = User.objects.create_user(username='testuser', password='Abc.12345')
            self.profile = Profile.objects.create(user=self.user)

        def test_profile_view(self):
            """Test that a logged in user can access the profile view"""
            self.client.login(username='testuser', password='Abc.12345')
            response = self.client.get(reverse('profile'))
            self.assertEqual(response.status_code, 200)
            # Test that the correct template is used for the profile view
            self.assertTemplateUsed(response, 'profile.html')

        def test_profile_form_valid(self):
            """Test that a valid profile form can be submitted successfully"""
            self.client.login(username='testuser', password='Abc.12345')
            form_data = {
                'profile_image': SimpleUploadedFile(name='test_image.jpg',
                                                    content=open('profile_images/default_male.jpg', 'rb').read(),
                                                    content_type='image/jpeg')
            }
            response = self.client.post(reverse('profile'), data=form_data)
            """Test that the profile image has been updated"""
            self.profile.refresh_from_db()
            self.assertNotEqual(self.profile.profile_image.name, 'profile_images/default_male.jpg')
            """Test that a successful form submission results in a redirect (status code 302)"""
            self.assertEqual(response.status_code, 302)

    class ProfileFormTest(TestCase):
        def setUp(self):
            """Set up a test user with a known password, and associated profile for use in the tests"""
            self.user = User.objects.create_user(username='testuser', password='Abc.12345')
            self.profile = Profile.objects.create(user=self.user)

        def test_profile_form_valid(self):
            """Test that a valid profile form is considered valid by Django's form validation"""
            form = ProfileForm(data={'profile_image': SimpleUploadedFile(name='test_image.jpg',
                                                                         content=open('profile_images/default_male.jpg',
                                                                                      'rb').read(),
                                                                         content_type='image/jpeg')})
            self.assertTrue(form.is_valid())

    class TestProductSearchView(TestCase):
        def setUp(self):
            """Set up some products in the database for testing"""
            Product.objects.create(name='Chepignon', description='This is Product1')
            Product.objects.create(name='Sucre', description='This is Product2')

        def test_product_search_typo(self):
            """Simulate a typo in the product search"""
            response = self.client.get(reverse('product_search') + '?q=Champignon')

            """Check that the response status code is 200"""
            self.assertEqual(response.status_code, 200)

            """Check that no products are returned in the search results"""
            self.assertEqual(len(response.context['products']), 0)

        def test_product_search_substring(self):
            """Search for a product name"""
            response = self.client.get(reverse('product_search') + '?q=sucre')

            """Check that the response status code is 200"""
            self.assertEqual(response.status_code, 200)

            """Check that the correct product is returned in the search results"""