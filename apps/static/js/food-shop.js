import { Cart } from './cart.js';
import { formatCurrency } from './helpers.js';

// Food products data
export const foodProducts = [
    {
        id: 'f1',
        name: "Classic English Breakfast",
        description: "Two eggs, bacon, sausage, baked beans, mushrooms, and toast",
        price: 12.99,
        category: "breakfast",
        image: "https://images.unsplash.com/photo-1551218808-94e220e084d2?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80",
        rating: 4.8,
        preparationTime: "15 min",
        isPopular: true,
        isVegetarian: false,
        allergens: ["eggs", "gluten", "dairy"]
    },
    {
        id: 'f2',
        name: "Avocado Toast Deluxe",
        description: "Sourdough toast with smashed avocado, cherry tomatoes, and microgreens",
        price: 8.99,
        category: "breakfast",
        image: "https://images.unsplash.com/photo-1541519227354-08fa5d50c44d?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80",
        rating: 4.6,
        preparationTime: "8 min",
        isPopular: false,
        isVegetarian: true,
        allergens: ["gluten"]
    },
    {
        id: 'f3',
        name: "Grilled Chicken Caesar Salad",
        description: "Fresh romaine lettuce, grilled chicken, parmesan cheese, and caesar dressing",
        price: 14.99,
        category: "lunch",
        image: "https://images.unsplash.com/photo-1546793665-c74683f339c1?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80",
        rating: 4.7,
        preparationTime: "20 min",
        isPopular: true,
        isVegetarian: false,
        allergens: ["eggs", "dairy", "gluten"]
    },
    {
        id: 'f4',
        name: "Beef Burger with Fries",
        description: "Angus beef patty, lettuce, tomato, cheese, and crispy fries",
        price: 16.99,
        category: "lunch",
        image: "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80",
        rating: 4.9,
        preparationTime: "25 min",
        isPopular: true,
        isVegetarian: false,
        allergens: ["gluten", "dairy"]
    },
    {
        id: 'f5',
        name: "Salmon Teriyaki Bowl",
        description: "Grilled salmon with teriyaki sauce, steamed rice, and vegetables",
        price: 18.99,
        category: "dinner",
        image: "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80",
        rating: 4.8,
        preparationTime: "30 min",
        isPopular: true,
        isVegetarian: false,
        allergens: ["fish", "soy"]
    },
    {
        id: 'f6',
        name: "Vegetarian Pasta Primavera",
        description: "Fresh vegetables, al dente pasta, and light cream sauce",
        price: 13.99,
        category: "dinner",
        image: "https://images.unsplash.com/photo-1551183053-bf91a1d81141?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80",
        rating: 4.5,
        preparationTime: "22 min",
        isPopular: false,
        isVegetarian: true,
        allergens: ["gluten", "dairy"]
    },
    {
        id: 'f7',
        name: "Chocolate Lava Cake",
        description: "Warm chocolate cake with molten center, served with vanilla ice cream",
        price: 7.99,
        category: "desserts",
        image: "https://images.unsplash.com/photo-1563805042-7684c019e1cb?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80",
        rating: 4.9,
        preparationTime: "12 min",
        isPopular: true,
        isVegetarian: true,
        allergens: ["eggs", "dairy", "gluten"]
    },
    {
        id: 'f8',
        name: "Fresh Fruit Smoothie Bowl",
        description: "Acai bowl topped with granola, fresh fruits, and honey",
        price: 9.99,
        category: "desserts",
        image: "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80",
        rating: 4.6,
        preparationTime: "8 min",
        isPopular: false,
        isVegetarian: true,
        allergens: ["nuts"]
    },
    {
        id: 'f9',
        name: "Artisan Coffee",
        description: "Single-origin coffee beans, freshly ground and brewed",
        price: 3.99,
        category: "drinks",
        image: "https://images.unsplash.com/photo-1509042239860-f550ce710b93?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80",
        rating: 4.7,
        preparationTime: "5 min",
        isPopular: true,
        isVegetarian: true,
        allergens: []
    },
    {
        id: 'f10',
        name: "Fresh Green Juice",
        description: "Kale, spinach, apple, and ginger juice",
        price: 5.99,
        category: "drinks",
        image: "https://images.unsplash.com/photo-1621506289937-a8e4df240d0b?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80",
        rating: 4.4,
        preparationTime: "6 min",
        isPopular: false,
        isVegetarian: true,
        allergens: []
    },
    {
        id: 'f11',
        name: "Loaded Nachos",
        description: "Tortilla chips with melted cheese, jalapeños, and sour cream",
        price: 11.99,
        category: "snacks",
        image: "https://images.unsplash.com/photo-1513456852971-30c0b8199d4d?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80",
        rating: 4.6,
        preparationTime: "15 min",
        isPopular: true,
        isVegetarian: false,
        allergens: ["dairy", "gluten"]
    },
    {
        id: 'f12',
        name: "Hummus with Pita",
        description: "Fresh hummus served with warm pita bread and olive oil",
        price: 6.99,
        category: "snacks",
        image: "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80",
        rating: 4.5,
        preparationTime: "10 min",
        isPopular: false,
        isVegetarian: true,
        allergens: ["sesame", "gluten"]
    }
];

const cart = new Cart();

export function getFoodByCategory(category) {
    if (category === 'all') return foodProducts;
    return foodProducts.filter(food => food.category === category);
}

export function searchFood(query) {
    const searchTerm = query.toLowerCase();
    return foodProducts.filter(food => 
        food.name.toLowerCase().includes(searchTerm) || 
        food.description.toLowerCase().includes(searchTerm) ||
        food.category.toLowerCase().includes(searchTerm)
    );
}

export function getFoodById(id) {
    return foodProducts.find(food => food.id === id);
}

function renderFoodProducts(foodsToRender = foodProducts) {
    const grid = document.getElementById('food-grid');
    if (!grid) return;
    
    grid.innerHTML = foodsToRender.map(food => `
        <div class="food-card" data-category="${food.category}">
            <div class="food-image">
                <img src="${food.image}" alt="${food.name}" loading="lazy">
                ${food.isPopular ? '<span class="food-badge">Popular</span>' : ''}
                ${food.isVegetarian ? '<span class="food-badge" style="background: #27ae60; top: 40px;">Veg</span>' : ''}
            </div>
            <div class="food-info">
                <h3 class="food-title">${food.name}</h3>
                <p class="food-description">${food.description}</p>
                <div class="food-meta">
                    <div class="food-price">${formatCurrency(food.price)}</div>
                    <div class="food-rating">
                        <i class="fas fa-star"></i>
                        <span>${food.rating}</span>
                    </div>
                </div>
                <div class="food-meta">
                    <small style="color: var(--gray);">
                        <i class="fas fa-clock"></i> ${food.preparationTime}
                    </small>
                    <small style="color: var(--gray);">
                        <i class="fas fa-fire"></i> ${Math.floor(Math.random() * 300 + 200)} cal
                    </small>
                </div>
                <div class="food-actions">
                    <button class="btn btn-primary add-to-cart-food" data-id="${food.id}">
                        Add to Cart
                    </button>
                    <button class="btn btn-outline view-details" data-id="${food.id}">
                        Details
                    </button>
                </div>
            </div>
        </div>
    `).join('');

    // Add event listeners
    document.querySelectorAll('.add-to-cart-food').forEach(btn => {
        btn.addEventListener('click', (e) => {
            const foodId = e.target.dataset.id;
            const food = foodProducts.find(f => f.id === foodId);
            if (food) {
                cart.addItem(food);
                updateCartCount();
                
                // Show quick confirmation
                showNotification('Added to cart!', 'success');
            }
        });
    });

    document.querySelectorAll('.view-details').forEach(btn => {
        btn.addEventListener('click', (e) => {
            const foodId = e.target.dataset.id;
            // Navigate to food details page
            window.location.href = `food-details.html?id=${foodId}`;
        });
    });
}

function setupFoodFilters() {
    document.querySelectorAll('.food-filter-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelector('.food-filter-btn.active').classList.remove('active');
            btn.classList.add('active');
            const category = btn.dataset.category;
            const filteredFoods = getFoodByCategory(category);
            renderFoodProducts(filteredFoods);
        });
    });
}

function updateCartCount() {
    const count = cart.getTotalItems();
    document.querySelectorAll('.cart-count').forEach(el => {
        el.textContent = count;
    });
}

function showNotification(message, type = 'success') {
    const notification = document.createElement('div');
    notification.textContent = message;
    notification.style.position = 'fixed';
    notification.style.bottom = '20px';
    notification.style.right = '20px';
    notification.style.backgroundColor = type === 'success' ? 'var(--primary)' : '#f39c12';
    notification.style.color = 'white';
    notification.style.padding = 'var(--space-sm) var(--space-md)';
    notification.style.borderRadius = 'var(--border-radius)';
    notification.style.zIndex = '1000';
    notification.style.boxShadow = 'var(--shadow-md)';
    notification.style.transform = 'translateX(100%)';
    notification.style.transition = 'transform 0.3s ease';
    
    document.body.appendChild(notification);
    
    // Animate in
    setTimeout(() => {
        notification.style.transform = 'translateX(0)';
    }, 100);
    
    // Remove after 3 seconds
    setTimeout(() => {
        notification.style.transform = 'translateX(100%)';
        setTimeout(() => {
            notification.remove();
        }, 300);
    }, 3000);
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    renderFoodProducts();
    setupFoodFilters();
    updateCartCount();
}); 