import pytest
from decimal import Decimal
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from apps.orders.models import Order, OrderItem
from apps.products.models import Product, Category

User = get_user_model()


class TestOrderModel(TestCase):
    """Test Order model"""
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.category = Category.objects.create(name='Test Category')
        self.product = Product.objects.create(
            name='Test Product',
            description='Test product description',
            price=29.99,
            category=self.category,
            stock=10,
            is_active=True
        )
        self.order = Order.objects.create(
            user=self.user,
            customer_name='Test Customer',
            customer_email='customer@example.com',
            customer_phone='+1234567890',
            shipping_address='123 Test St, Test City',
            total_amount=Decimal('59.98'),
            status='pending'
        )
    
    def test_order_creation(self):
        """Test order creation"""
        self.assertEqual(self.order.customer_name, 'Test Customer')
        self.assertEqual(self.order.total_amount, Decimal('59.98'))
        self.assertEqual(self.order.status, 'pending')
    
    def test_order_str_representation(self):
        """Test order string representation"""
        expected = f"Order {self.order.id} - {self.order.customer_name}"
        self.assertEqual(str(self.order), expected)
    
    def test_order_status_choices(self):
        """Test order status choices"""
        valid_statuses = ['pending', 'processing', 'shipped', 'delivered', 'cancelled']
        self.assertIn(self.order.status, valid_statuses)
    
    def test_order_total_calculation(self):
        """Test order total calculation"""
        # Create order items
        OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=2,
            price=Decimal('29.99')
        )
        
        # Recalculate total
        self.order.calculate_total()
        self.assertEqual(self.order.total_amount, Decimal('59.98'))


class TestOrderItemModel(TestCase):
    """Test OrderItem model"""
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.category = Category.objects.create(name='Test Category')
        self.product = Product.objects.create(
            name='Test Product',
            description='Test product description',
            price=29.99,
            category=self.category,
            stock=10,
            is_active=True
        )
        self.order = Order.objects.create(
            user=self.user,
            customer_name='Test Customer',
            customer_email='customer@example.com',
            total_amount=Decimal('59.98'),
            status='pending'
        )
        self.order_item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=2,
            price=Decimal('29.99')
        )
    
    def test_order_item_creation(self):
        """Test order item creation"""
        self.assertEqual(self.order_item.quantity, 2)
        self.assertEqual(self.order_item.price, Decimal('29.99'))
    
    def test_order_item_str_representation(self):
        """Test order item string representation"""
        expected = f"{self.order_item.quantity}x {self.product.name}"
        self.assertEqual(str(self.order_item), expected)
    
    def test_order_item_total(self):
        """Test order item total calculation"""
        total = self.order_item.quantity * self.order_item.price
        self.assertEqual(total, Decimal('59.98'))


class TestOrderViews(TestCase):
    """Test order views"""
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.category = Category.objects.create(name='Test Category')
        self.product = Product.objects.create(
            name='Test Product',
            description='Test product description',
            price=29.99,
            category=self.category,
            stock=10,
            is_active=True
        )
        self.order = Order.objects.create(
            user=self.user,
            customer_name='Test Customer',
            customer_email='customer@example.com',
            total_amount=Decimal('59.98'),
            status='pending'
        )
    
    def test_order_list_view_authenticated(self):
        """Test order list view for authenticated user"""
        self.client.force_login(self.user)
        response = self.client.get(reverse('order_list'))
        self.assertEqual(response.status_code, 200)
    
    def test_order_list_view_unauthenticated(self):
        """Test order list view for unauthenticated user"""
        response = self.client.get(reverse('order_list'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
    
    def test_order_detail_view_authenticated(self):
        """Test order detail view for authenticated user"""
        self.client.force_login(self.user)
        response = self.client.get(reverse('order_detail', args=[self.order.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Customer')
    
    def test_order_detail_view_unauthenticated(self):
        """Test order detail view for unauthenticated user"""
        response = self.client.get(reverse('order_detail', args=[self.order.id]))
        self.assertEqual(response.status_code, 302)  # Redirect to login
    
    def test_order_detail_view_wrong_user(self):
        """Test order detail view for wrong user"""
        other_user = User.objects.create_user(
            username='otheruser',
            email='other@example.com',
            password='otherpass123'
        )
        self.client.force_login(other_user)
        response = self.client.get(reverse('order_detail', args=[self.order.id]))
        self.assertEqual(response.status_code, 404)  # Not found


@pytest.mark.django_db
class TestOrderAPI:
    """Test order API endpoints"""
    
    def test_order_list_api_authenticated(self, authenticated_client, user):
        """Test order list API for authenticated user"""
        response = authenticated_client.get('/api/orders/')
        assert response.status_code == 200
    
    def test_order_list_api_unauthenticated(self, client):
        """Test order list API for unauthenticated user"""
        response = client.get('/api/orders/')
        assert response.status_code == 401
    
    def test_order_detail_api(self, authenticated_client, user, sample_order_data):
        """Test order detail API"""
        order = Order.objects.create(
            user=user,
            **sample_order_data
        )
        
        response = authenticated_client.get(f'/api/orders/{order.id}/')
        assert response.status_code == 200
        assert response.json()['customer_name'] == sample_order_data['customer_name']
    
    def test_create_order_api(self, authenticated_client, user, sample_order_data):
        """Test create order API"""
        response = authenticated_client.post('/api/orders/', sample_order_data)
        assert response.status_code == 201
        assert Order.objects.count() == 1
    
    def test_update_order_status_api(self, admin_client, user, sample_order_data):
        """Test update order status API"""
        order = Order.objects.create(
            user=user,
            **sample_order_data
        )
        
        new_status = 'processing'
        response = admin_client.patch(
            f'/api/orders/{order.id}/',
            {'status': new_status},
            content_type='application/json'
        )
        assert response.status_code == 200
        assert response.json()['status'] == new_status


@pytest.mark.django_db
class TestOrderWorkflow:
    """Test order workflow"""
    
    def test_order_creation_workflow(self, authenticated_client, user, sample_product_data):
        """Test complete order creation workflow"""
        # Create product
        category = Category.objects.create(name='Test Category')
        product = Product.objects.create(
            category=category,
            **sample_product_data
        )
        
        # Create order
        order_data = {
            'customer_name': 'Test Customer',
            'customer_email': 'customer@example.com',
            'customer_phone': '+1234567890',
            'shipping_address': '123 Test St, Test City',
            'items': [
                {
                    'product_id': product.id,
                    'quantity': 2
                }
            ]
        }
        
        response = authenticated_client.post('/api/orders/', order_data, content_type='application/json')
        assert response.status_code == 201
        
        # Verify order was created
        order = Order.objects.first()
        assert order.customer_name == 'Test Customer'
        assert order.status == 'pending'
        
        # Verify order items were created
        assert order.items.count() == 1
        order_item = order.items.first()
        assert order_item.product == product
        assert order_item.quantity == 2
    
    def test_order_status_transitions(self, admin_client, user, sample_order_data):
        """Test order status transitions"""
        order = Order.objects.create(
            user=user,
            **sample_order_data
        )
        
        # Test valid status transitions
        valid_transitions = ['processing', 'shipped', 'delivered']
        for status in valid_transitions:
            response = admin_client.patch(
                f'/api/orders/{order.id}/',
                {'status': status},
                content_type='application/json'
            )
            assert response.status_code == 200
            order.refresh_from_db()
            assert order.status == status
    
    def test_order_cancellation(self, admin_client, user, sample_order_data):
        """Test order cancellation"""
        order = Order.objects.create(
            user=user,
            **sample_order_data
        )
        
        response = admin_client.patch(
            f'/api/orders/{order.id}/',
            {'status': 'cancelled'},
            content_type='application/json'
        )
        assert response.status_code == 200
        
        order.refresh_from_db()
        assert order.status == 'cancelled'


@pytest.mark.django_db
class TestOrderValidation:
    """Test order validation"""
    
    def test_order_with_invalid_email(self, authenticated_client, user):
        """Test order creation with invalid email"""
        order_data = {
            'customer_name': 'Test Customer',
            'customer_email': 'invalid-email',
            'total_amount': 29.99,
            'status': 'pending'
        }
        
        response = authenticated_client.post('/api/orders/', order_data)
        assert response.status_code == 400
    
    def test_order_with_negative_total(self, authenticated_client, user):
        """Test order creation with negative total"""
        order_data = {
            'customer_name': 'Test Customer',
            'customer_email': 'customer@example.com',
            'total_amount': -10.00,
            'status': 'pending'
        }
        
        response = authenticated_client.post('/api/orders/', order_data)
        assert response.status_code == 400
    
    def test_order_with_empty_required_fields(self, authenticated_client, user):
        """Test order creation with empty required fields"""
        order_data = {
            'customer_name': '',
            'customer_email': '',
            'total_amount': 29.99,
            'status': 'pending'
        }
        
        response = authenticated_client.post('/api/orders/', order_data)
        assert response.status_code == 400 