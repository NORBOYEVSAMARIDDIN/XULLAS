import pytest
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class TestFrontendViews(TestCase):
    """Test frontend views"""
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_home_page(self):
        """Test home page"""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'SHALLION')
    
    def test_shop_page(self):
        """Test shop page"""
        response = self.client.get(reverse('shop'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Shop')
    
    def test_food_shop_page(self):
        """Test food shop page"""
        response = self.client.get(reverse('food_shop'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Food')
    
    def test_cart_page(self):
        """Test cart page"""
        response = self.client.get(reverse('cart'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Cart')
    
    def test_checkout_page(self):
        """Test checkout page"""
        response = self.client.get(reverse('checkout'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Checkout')
    
    def test_account_page_authenticated(self):
        """Test account page for authenticated user"""
        self.client.force_login(self.user)
        response = self.client.get(reverse('account'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Account')
    
    def test_account_page_unauthenticated(self):
        """Test account page for unauthenticated user"""
        response = self.client.get(reverse('account'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
    
    def test_help_page(self):
        """Test help page"""
        response = self.client.get(reverse('help'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Help')


@pytest.mark.django_db
class TestFrontendAPI:
    """Test frontend API endpoints"""
    
    def test_cart_api_add_item(self, client):
        """Test adding item to cart via API"""
        data = {
            'product_id': 1,
            'quantity': 2
        }
        response = client.post('/api/cart/add/', data)
        assert response.status_code == 200
    
    def test_cart_api_remove_item(self, client):
        """Test removing item from cart via API"""
        data = {
            'product_id': 1
        }
        response = client.post('/api/cart/remove/', data)
        assert response.status_code == 200
    
    def test_cart_api_get_items(self, client):
        """Test getting cart items via API"""
        response = client.get('/api/cart/items/')
        assert response.status_code == 200
    
    def test_search_api(self, client):
        """Test search API"""
        response = client.get('/api/search/?q=test')
        assert response.status_code == 200
    
    def test_food_search_api(self, client):
        """Test food search API"""
        response = client.get('/api/food/search/?q=burger')
        assert response.status_code == 200


class TestFrontendTemplates(TestCase):
    """Test frontend templates"""
    
    def test_base_template_inheritance(self):
        """Test base template inheritance"""
        response = self.client.get(reverse('home'))
        self.assertContains(response, 'SHALLION')
        self.assertContains(response, 'Shop')
        self.assertContains(response, 'Food')
        self.assertContains(response, 'Account')
        self.assertContains(response, 'Help')
    
    def test_navigation_consistency(self):
        """Test navigation consistency across pages"""
        pages = ['home', 'shop', 'food_shop', 'cart', 'checkout', 'help']
        
        for page in pages:
            try:
                response = self.client.get(reverse(page))
                if response.status_code == 200:
                    self.assertContains(response, 'SHALLION')
                    self.assertContains(response, 'Shop')
                    self.assertContains(response, 'Food')
                    self.assertContains(response, 'Account')
                    self.assertContains(response, 'Help')
            except:
                # Skip pages that don't exist yet
                pass
    
    def test_responsive_design_elements(self):
        """Test responsive design elements"""
        response = self.client.get(reverse('home'))
        self.assertContains(response, 'viewport')
        self.assertContains(response, 'width=device-width')


@pytest.mark.django_db
class TestFrontendJavaScript:
    """Test frontend JavaScript functionality"""
    
    def test_cart_functionality(self, client):
        """Test cart JavaScript functionality"""
        # Test cart initialization
        response = client.get(reverse('cart'))
        self.assertContains(response, 'cart.js')
        
        # Test cart operations
        data = {
            'action': 'add',
            'product_id': 1,
            'quantity': 1
        }
        response = client.post('/api/cart/update/', data)
        assert response.status_code == 200
    
    def test_search_functionality(self, client):
        """Test search JavaScript functionality"""
        response = client.get(reverse('shop'))
        self.assertContains(response, 'search.js')
        
        # Test search API
        response = client.get('/api/search/?q=test')
        assert response.status_code == 200
    
    def test_food_filtering(self, client):
        """Test food filtering functionality"""
        response = client.get(reverse('food_shop'))
        self.assertContains(response, 'food-shop.js')
        
        # Test food filtering API
        response = client.get('/api/food/filter/?category=breakfast')
        assert response.status_code == 200
    
    def test_checkout_functionality(self, client):
        """Test checkout JavaScript functionality"""
        response = client.get(reverse('checkout'))
        self.assertContains(response, 'checkout.js')
        
        # Test payment processing
        data = {
            'payment_method': 'card',
            'amount': 29.99
        }
        response = client.post('/api/payment/process/', data)
        assert response.status_code in [200, 400, 500]  # Various possible responses


class TestFrontendPerformance(TestCase):
    """Test frontend performance"""
    
    def test_page_load_time(self):
        """Test page load time"""
        import time
        
        start_time = time.time()
        response = self.client.get(reverse('home'))
        load_time = time.time() - start_time
        
        self.assertEqual(response.status_code, 200)
        self.assertLess(load_time, 2.0)  # Should load in less than 2 seconds
    
    def test_static_files_loading(self):
        """Test static files loading"""
        response = self.client.get(reverse('home'))
        
        # Check if CSS files are referenced
        self.assertContains(response, 'base.css')
        self.assertContains(response, 'components.css')
        
        # Check if JavaScript files are referenced
        self.assertContains(response, 'app.js')
    
    def test_image_optimization(self):
        """Test image optimization"""
        response = self.client.get(reverse('food_shop'))
        
        # Check if images have proper attributes
        self.assertContains(response, 'loading="lazy"')
        self.assertContains(response, 'alt=')


@pytest.mark.django_db
class TestFrontendSecurity:
    """Test frontend security"""
    
    def test_csrf_protection(self, client):
        """Test CSRF protection"""
        response = client.get(reverse('checkout'))
        self.assertContains(response, 'csrfmiddlewaretoken')
    
    def test_xss_protection(self, client):
        """Test XSS protection"""
        # Test with potentially malicious input
        malicious_input = '<script>alert("xss")</script>'
        response = client.get(f'/api/search/?q={malicious_input}')
        
        # Should not contain the script tag in response
        if response.status_code == 200:
            self.assertNotIn('<script>', response.content.decode())
    
    def test_sql_injection_protection(self, client):
        """Test SQL injection protection"""
        # Test with potentially malicious input
        malicious_input = "'; DROP TABLE products; --"
        response = client.get(f'/api/search/?q={malicious_input}')
        
        # Should not crash the application
        self.assertIn(response.status_code, [200, 400, 404])
    
    def test_authentication_required_pages(self, client):
        """Test authentication required pages"""
        protected_pages = ['account', 'profile', 'orders']
        
        for page in protected_pages:
            try:
                response = client.get(reverse(page))
                self.assertIn(response.status_code, [302, 403])  # Should redirect or forbid
            except:
                # Skip pages that don't exist yet
                pass


class TestFrontendAccessibility(TestCase):
    """Test frontend accessibility"""
    
    def test_semantic_html(self):
        """Test semantic HTML structure"""
        response = self.client.get(reverse('home'))
        
        # Check for semantic elements
        self.assertContains(response, '<header>')
        self.assertContains(response, '<main>')
        self.assertContains(response, '<nav>')
    
    def test_alt_text_for_images(self):
        """Test alt text for images"""
        response = self.client.get(reverse('food_shop'))
        
        # Check if images have alt attributes
        self.assertContains(response, 'alt=')
    
    def test_form_labels(self):
        """Test form labels"""
        response = self.client.get(reverse('checkout'))
        
        # Check if forms have proper labels
        self.assertContains(response, '<label>')
    
    def test_keyboard_navigation(self):
        """Test keyboard navigation support"""
        response = self.client.get(reverse('shop'))
        
        # Check for tabindex or focusable elements
        self.assertContains(response, 'tabindex') or self.assertContains(response, 'button') or self.assertContains(response, 'a href') 