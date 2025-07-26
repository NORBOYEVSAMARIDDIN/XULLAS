import pytest
from django.conf import settings
from django.test import RequestFactory
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.fixture(scope="session")
def django_db_setup(django_db_setup, django_db_blocker):
    """Setup database for testing"""
    with django_db_blocker.unblock():
        pass


@pytest.fixture
def db_access_without_rollback_and_truncate(django_db_setup, django_db_blocker):
    """Database access without rollback and truncate"""
    django_db_blocker.unblock()
    yield
    django_db_blocker.restore()


@pytest.fixture
def request_factory():
    """Request factory for testing views"""
    return RequestFactory()


@pytest.fixture
def user():
    """Create a test user"""
    return User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass123'
    )


@pytest.fixture
def admin_user():
    """Create a test admin user"""
    return User.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='adminpass123'
    )


@pytest.fixture
def authenticated_client(client, user):
    """Authenticated client with a test user"""
    client.force_login(user)
    return client


@pytest.fixture
def admin_client(client, admin_user):
    """Authenticated client with an admin user"""
    client.force_login(admin_user)
    return client


@pytest.fixture
def sample_product_data():
    """Sample product data for testing"""
    return {
        'name': 'Test Product',
        'description': 'Test product description',
        'price': 29.99,
        'category': 'test',
        'image': 'test-image.jpg',
        'stock': 10,
        'is_active': True
    }


@pytest.fixture
def sample_order_data():
    """Sample order data for testing"""
    return {
        'customer_name': 'Test Customer',
        'customer_email': 'customer@example.com',
        'customer_phone': '+1234567890',
        'shipping_address': '123 Test St, Test City',
        'total_amount': 59.98,
        'status': 'pending'
    }


@pytest.fixture
def sample_food_data():
    """Sample food data for testing"""
    return {
        'name': 'Test Food Item',
        'description': 'Test food description',
        'price': 15.99,
        'category': 'lunch',
        'image': 'test-food.jpg',
        'preparation_time': '20 min',
        'is_vegetarian': False,
        'allergens': ['gluten', 'dairy']
    } 