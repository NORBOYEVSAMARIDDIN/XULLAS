import pytest
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from apps.products.models import Product, Category

User = get_user_model()


class TestProductModel(TestCase):
    """Test Product model"""
    
    def setUp(self):
        """Set up test data"""
        self.category = Category.objects.create(
            name='Test Category',
            description='Test category description'
        )
        self.product = Product.objects.create(
            name='Test Product',
            description='Test product description',
            price=29.99,
            category=self.category,
            stock=10,
            is_active=True
        )
    
    def test_product_creation(self):
        """Test product creation"""
        self.assertEqual(self.product.name, 'Test Product')
        self.assertEqual(self.product.price, 29.99)
        self.assertTrue(self.product.is_active)
    
    def test_product_str_representation(self):
        """Test product string representation"""
        self.assertEqual(str(self.product), 'Test Product')
    
    def test_product_price_formatting(self):
        """Test product price formatting"""
        self.assertEqual(self.product.get_formatted_price(), '£29.99')
    
    def test_product_availability(self):
        """Test product availability"""
        self.assertTrue(self.product.is_available())
        
        # Test when stock is 0
        self.product.stock = 0
        self.assertFalse(self.product.is_available())
        
        # Test when product is inactive
        self.product.stock = 10
        self.product.is_active = False
        self.assertFalse(self.product.is_available())


class TestCategoryModel(TestCase):
    """Test Category model"""
    
    def setUp(self):
        """Set up test data"""
        self.category = Category.objects.create(
            name='Test Category',
            description='Test category description'
        )
    
    def test_category_creation(self):
        """Test category creation"""
        self.assertEqual(self.category.name, 'Test Category')
        self.assertEqual(self.category.description, 'Test category description')
    
    def test_category_str_representation(self):
        """Test category string representation"""
        self.assertEqual(str(self.category), 'Test Category')


class TestProductViews(TestCase):
    """Test product views"""
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.category = Category.objects.create(
            name='Test Category',
            description='Test category description'
        )
        self.product = Product.objects.create(
            name='Test Product',
            description='Test product description',
            price=29.99,
            category=self.category,
            stock=10,
            is_active=True
        )
    
    def test_product_list_view(self):
        """Test product list view"""
        response = self.client.get(reverse('product_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Product')
    
    def test_product_detail_view(self):
        """Test product detail view"""
        response = self.client.get(reverse('product_detail', args=[self.product.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Product')
    
    def test_product_detail_view_404(self):
        """Test product detail view with non-existent product"""
        response = self.client.get(reverse('product_detail', args=[999]))
        self.assertEqual(response.status_code, 404)


@pytest.mark.django_db
class TestProductAPI:
    """Test product API endpoints"""
    
    def test_product_list_api(self, client):
        """Test product list API"""
        response = client.get('/api/products/')
        assert response.status_code == 200
    
    def test_product_detail_api(self, client, sample_product_data):
        """Test product detail API"""
        # Create a product first
        category = Category.objects.create(name='Test Category')
        product = Product.objects.create(
            category=category,
            **sample_product_data
        )
        
        response = client.get(f'/api/products/{product.id}/')
        assert response.status_code == 200
        assert response.json()['name'] == sample_product_data['name']


@pytest.mark.django_db
class TestProductSearch:
    """Test product search functionality"""
    
    def test_product_search_by_name(self, client):
        """Test product search by name"""
        category = Category.objects.create(name='Test Category')
        Product.objects.create(
            name='iPhone 15',
            description='Latest iPhone',
            price=999.99,
            category=category,
            stock=5,
            is_active=True
        )
        
        response = client.get('/api/products/search/?q=iPhone')
        assert response.status_code == 200
        assert len(response.json()) > 0
    
    def test_product_search_empty_query(self, client):
        """Test product search with empty query"""
        response = client.get('/api/products/search/?q=')
        assert response.status_code == 200
        assert len(response.json()) == 0


@pytest.mark.django_db
class TestProductFiltering:
    """Test product filtering functionality"""
    
    def test_product_filter_by_category(self, client):
        """Test product filtering by category"""
        category1 = Category.objects.create(name='Electronics')
        category2 = Category.objects.create(name='Clothing')
        
        Product.objects.create(
            name='iPhone',
            description='Smartphone',
            price=999.99,
            category=category1,
            stock=5,
            is_active=True
        )
        
        Product.objects.create(
            name='T-Shirt',
            description='Cotton T-shirt',
            price=29.99,
            category=category2,
            stock=10,
            is_active=True
        )
        
        response = client.get(f'/api/products/?category={category1.id}')
        assert response.status_code == 200
        products = response.json()
        assert all(product['category'] == category1.id for product in products)
    
    def test_product_filter_by_price_range(self, client):
        """Test product filtering by price range"""
        category = Category.objects.create(name='Test Category')
        
        Product.objects.create(
            name='Cheap Product',
            description='Low price product',
            price=10.00,
            category=category,
            stock=5,
            is_active=True
        )
        
        Product.objects.create(
            name='Expensive Product',
            description='High price product',
            price=100.00,
            category=category,
            stock=2,
            is_active=True
        )
        
        response = client.get('/api/products/?min_price=50&max_price=150')
        assert response.status_code == 200
        products = response.json()
        assert all(50 <= product['price'] <= 150 for product in products) 