from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.files.uploadedfile import SimpleUploadedFile
from users.forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from users.models import UserProfile

class UserViewsTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword123')
    
    def test_register_view_get(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')

    def test_register_view_post_success(self):
        response = self.client.post(reverse('register'), data={
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'Testpassword123',
            'password2': 'Testpassword123',
        })
        self.assertEqual(User.objects.count(), 2)  # Original user + new user
        self.assertRedirects(response, reverse('login'))

    def test_register_view_post_fail(self):
        response = self.client.post(reverse('register'), data={
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'Testpassword123',
            'password2': 'Testpassword1234',  # Mismatched passwords
        }, follow=True)
        form = response.context.get('form')
        self.assertTrue(form.errors)

    def test_logout_view(self):
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.get(reverse('logout'))
        self.assertRedirects(response, reverse('login'))

    def test_profile_view_get(self):
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/profile.html')
        
    def test_account_settings_view_get(self):
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.get(reverse('account-settings'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/account_settings.html')

    def test_account_settings_view_post(self):
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.post(reverse('account-settings'), data={
            'username': 'updateduser',
            'email': 'updated@example.com'
        })
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'updateduser')
        self.assertEqual(self.user.email, 'updated@example.com')
        self.assertRedirects(response, reverse('account-settings'))