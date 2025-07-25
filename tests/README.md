# SHALLION Test Documentation

## Overview

This project uses pytest as the testing framework, providing comprehensive test coverage including unit tests, integration tests, and frontend tests.

## Test Structure

```
tests/
├── __init__.py
├── conftest.py              # pytest configuration and fixtures
├── test_products.py         # Product-related tests
├── test_orders.py           # Order-related tests
├── test_users.py            # User-related tests
├── test_frontend.py         # Frontend-related tests
├── run_tests.py            # Test runner script
└── README.md               # Test documentation
```

## Installing Test Dependencies

```bash
# Activate virtual environment
source venv/bin/activate

# Install test dependencies
pip install -r requirements/test.txt
```

## Running Tests

### Using the Test Script

```bash
# Run all tests
python tests/run_tests.py

# Run specific test types
python tests/run_tests.py --type unit
python tests/run_tests.py --type integration
python tests/run_tests.py --type frontend
python tests/run_tests.py --type backend

# Run tests with coverage
python tests/run_tests.py --type coverage

# Check test environment
python tests/run_tests.py --check-env
```

### Using pytest Directly

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_products.py

# Run tests with markers
pytest -m unit
pytest -m integration
pytest -m fast
pytest -m slow

# Run tests with coverage
pytest --cov=apps --cov-report=html

# Run tests in parallel
pytest -n auto

# Verbose output
pytest -v
```

## Test Types

### 1. Unit Tests
- Test individual functions or methods
- Use mocks to isolate dependencies
- Fast execution
- Marker: `@pytest.mark.unit`

### 2. Integration Tests
- Test interactions between multiple components
- Use real database
- Marker: `@pytest.mark.integration`

### 3. Frontend Tests
- Test templates and views
- Test JavaScript functionality
- Test user interface

### 4. End-to-End Tests (E2E)
- Test complete user workflows
- Simulate real user operations
- Marker: `@pytest.mark.e2e`

## Test Fixtures

### User Fixtures
- `user`: Create test user
- `admin_user`: Create admin user
- `authenticated_client`: Authenticated client
- `admin_client`: Admin client

### Data Fixtures
- `sample_product_data`: Sample product data
- `sample_order_data`: Sample order data
- `sample_food_data`: Sample food data

### Utility Fixtures
- `request_factory`: Django request factory
- `db_access_without_rollback_and_truncate`: Database access

## Testing Best Practices

### 1. Test Naming
```python
def test_user_can_login_with_valid_credentials():
    """Test that user can login with valid credentials"""
    pass
```

### 2. Test Organization
```python
class TestUserModel:
    """Test User model functionality"""
    
    def test_user_creation(self):
        """Test user creation"""
        pass
    
    def test_user_str_representation(self):
        """Test user string representation"""
        pass
```

### 3. Using Fixtures
```python
def test_user_profile(authenticated_client, user):
    """Test user profile access"""
    response = authenticated_client.get('/api/users/profile/')
    assert response.status_code == 200
```

### 4. Test Data Isolation
```python
@pytest.mark.django_db
def test_product_creation():
    """Test product creation"""
    product = Product.objects.create(name='Test Product')
    assert product.name == 'Test Product'
```

## Coverage Reports

After running coverage tests, detailed HTML reports will be generated in the `htmlcov/` directory:

```bash
# Generate coverage report
pytest --cov=apps --cov-report=html

# View report
open htmlcov/index.html
```

## Continuous Integration

### GitHub Actions Configuration
```yaml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.12
      - name: Install dependencies
        run: |
          pip install -r requirements/test.txt
      - name: Run tests
        run: |
          python tests/run_tests.py --type coverage
```

## Debugging Tests

### 1. Running Single Tests
```bash
pytest tests/test_products.py::TestProductModel::test_product_creation -v
```

### 2. Using pdb for Debugging
```python
import pdb; pdb.set_trace()
```

### 3. Viewing Verbose Output
```bash
pytest -v -s
```

## Common Issues

### 1. Database Errors
Ensure test database configuration is correct:
```python
# settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}
```

### 2. Import Errors
Ensure test files are in the correct path and `PYTHONPATH` is set correctly.

### 3. Permission Errors
Some tests may require admin permissions, ensure you're using the correct fixtures.

## Test Maintenance

### 1. Regular Test Updates
- Add corresponding tests when adding new features
- Update related tests when modifying existing features
- Regularly check test coverage

### 2. Test Performance
- Use `@pytest.mark.slow` for slow tests
- Use parallel execution to improve test speed
- Regularly clean up test data

### 3. Test Documentation
- Keep test documentation updated
- Add test case descriptions
- Document test environment requirements 