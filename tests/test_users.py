import pytest
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from apps.users.models import UserProfile

User = get_user_model()


class TestUserModel(TestCase):
    """Test User model"""

    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )

    def test_user_creation(self):
        """Test user creation"""
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertEqual(self.user.first_name, 'Test')
        self.assertEqual(self.user.last_name, 'User')
        self.assertTrue(self.user.check_password('testpass123'))

    def test_user_str_representation(self):
        """Test user string representation"""
        self.assertEqual(str(self.user), 'testuser')

    def test_user_full_name(self):
        """Test user full name"""
        self.assertEqual(self.user.get_full_name(), 'Test User')

    def test_user_short_name(self):
        """Test user short name"""
        self.assertEqual(self.user.get_short_name(), 'Test')

    def test_superuser_creation(self):
        """Test superuser creation"""
        admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpass123'
        )
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)


class TestUserProfileModel(TestCase):
    """Test UserProfile model"""

    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.profile = UserProfile.objects.create(
            user=self.user,
            phone='+1234567890',
            address='123 Test St, Test City',
            date_of_birth='1990-01-01'
        )

    def test_profile_creation(self):
        """Test profile creation"""
        self.assertEqual(self.profile.user, self.user)
        self.assertEqual(self.profile.phone, '+1234567890')
        self.assertEqual(self.profile.address, '123 Test St, Test City')

    def test_profile_str_representation(self):
        """Test profile string representation"""
        self.assertEqual(str(self.profile), f"{self.user.username}'s profile")

    def test_profile_auto_creation(self):
        """Test profile auto creation when user is created"""
        new_user = User.objects.create_user(
            username='newuser',
            email='new@example.com',
            password='newpass123'
        )
        self.assertTrue(hasattr(new_user, 'profile'))
        self.assertIsNotNone(new_user.profile)


class TestUserViews(TestCase):
    """Test user views"""

    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    def test_user_registration_view(self):
        """Test user registration view"""
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Register')

    def test_user_registration_post(self):
        """Test user registration POST request"""
        data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'password1': 'newpass123',
            'password2': 'newpass123',
            'first_name': 'New',
            'last_name': 'User'
        }
        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful registration

        # Check if user was created
        new_user = User.objects.get(username='newuser')
        self.assertEqual(new_user.email, 'new@example.com')

    def test_user_login_view(self):
        """Test user login view"""
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Login')

    def test_user_login_post(self):
        """Test user login POST request"""
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        response = self.client.post(reverse('login'), data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful login

        # Check if user is authenticated
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_user_logout_view(self):
        """Test user logout view"""
        # Login first
        self.client.force_login(self.user)

        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)  # Redirect after logout

        # Check if user is not authenticated
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_user_profile_view_authenticated(self):
        """Test user profile view for authenticated user"""
        self.client.force_login(self.user)
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'testuser')

    def test_user_profile_view_unauthenticated(self):
        """Test user profile view for unauthenticated user"""
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_user_profile_update(self):
        """Test user profile update"""
        self.client.force_login(self.user)

        data = {
            'first_name': 'Updated',
            'last_name': 'Name',
            'email': 'updated@example.com'
        }
        response = self.client.post(reverse('profile'), data)
        self.assertEqual(response.status_code, 302)  # Redirect after update

        # Check if user was updated
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Updated')
        self.assertEqual(self.user.email, 'updated@example.com')


@pytest.mark.django_db
class TestUserAPI:
    """Test user API endpoints"""

    def test_user_registration_api(self, client):
        """Test user registration API"""
        data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'newpass123',
            'first_name': 'New',
            'last_name': 'User'
        }
        response = client.post('/api/users/register/', data)
        assert response.status_code == 201
        assert User.objects.filter(username='newuser').exists()

    def test_user_login_api(self, client, user):
        """Test user login API"""
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        response = client.post('/api/users/login/', data)
        assert response.status_code == 200
        assert 'token' in response.json()

    def test_user_profile_api_authenticated(self, authenticated_client, user):
        """Test user profile API for authenticated user"""
        response = authenticated_client.get('/api/users/profile/')
        assert response.status_code == 200
        assert response.json()['username'] == 'testuser'

    def test_user_profile_api_unauthenticated(self, client):
        """Test user profile API for unauthenticated user"""
        response = client.get('/api/users/profile/')
        assert response.status_code == 401

    def test_user_profile_update_api(self, authenticated_client, user):
        """Test user profile update API"""
        data = {
            'first_name': 'Updated',
            'last_name': 'Name',
            'email': 'updated@example.com'
        }
        response = authenticated_client.patch('/api/users/profile/', data)
        assert response.status_code == 200
        assert response.json()['first_name'] == 'Updated'


@pytest.mark.django_db
class TestUserAuthentication:
    """Test user authentication"""

    def test_user_registration_validation(self, client):
        """Test user registration validation"""
        # Test with invalid email
        data = {
            'username': 'newuser',
            'email': 'invalid-email',
            'password': 'newpass123'
        }
        response = client.post('/api/users/register/', data)
        assert response.status_code == 400

        # Test with weak password
        data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'password': '123'
        }
        response = client.post('/api/users/register/', data)
        assert response.status_code == 400

        # Test with duplicate username
        User.objects.create_user(
            username='existinguser',
            email='existing@example.com',
            password='existingpass123'
        )
        data = {
            'username': 'existinguser',
            'email': 'new@example.com',
            'password': 'newpass123'
        }
        response = client.post('/api/users/register/', data)
        assert response.status_code == 400

    def test_user_login_validation(self, client, user):
        """Test user login validation"""
        # Test with wrong password
        data = {
            'username': 'testuser',
            'password': 'wrongpassword'
        }
        response = client.post('/api/users/login/', data)
        assert response.status_code == 400

        # Test with non-existent user
        data = {
            'username': 'nonexistent',
            'password': 'testpass123'
        }
        response = client.post('/api/users/login/', data)
        assert response.status_code == 400

    def test_password_change(self, authenticated_client, user):
        """Test password change"""
        data = {
            'old_password': 'testpass123',
            'new_password1': 'newpass123',
            'new_password2': 'newpass123'
        }
        response = authenticated_client.post('/api/users/change-password/', data)
        assert response.status_code == 200

        # Verify password was changed
        user.refresh_from_db()
        assert user.check_password('newpass123')


@pytest.mark.django_db
class TestUserPermissions:
    """Test user permissions"""

    def test_user_can_access_own_profile(self, authenticated_client, user):
        """Test user can access own profile"""
        response = authenticated_client.get(f'/api/users/{user.id}/')
        assert response.status_code == 200

    def test_user_cannot_access_other_profile(self, authenticated_client, user):
        """Test user cannot access other user's profile"""
        other_user = User.objects.create_user(
            username='otheruser',
            email='other@example.com',
            password='otherpass123'
        )
        response = authenticated_client.get(f'/api/users/{other_user.id}/')
        assert response.status_code == 403

    def test_admin_can_access_all_profiles(self, admin_client, user):
        """Test admin can access all profiles"""
        response = admin_client.get(f'/api/users/{user.id}/')
        assert response.status_code == 200

    def test_user_list_only_for_admin(self, authenticated_client, user):
        """Test user list is only accessible by admin"""
        response = authenticated_client.get('/api/users/')
        assert response.status_code == 403

    def test_user_list_for_admin(self, admin_client, user):
        """Test user list is accessible by admin"""
        response = admin_client.get('/api/users/')
        assert response.status_code == 200 