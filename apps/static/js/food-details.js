import { Cart } from './cart.js';
import { formatCurrency } from './helpers.js';
import { foodProducts, getFoodById } from './food-shop.js';

const cart = new Cart();

// Sample reviews data
const reviews = [
    {
        id: 1,
        foodId: 'f1',
        reviewerName: 'Sarah M.',
        rating: 5,
        date: '2024-01-15',
        text: 'Absolutely delicious! The eggs were perfectly cooked and the bacon was crispy. Will definitely order again!'
    },
    {
        id: 2,
        foodId: 'f1',
        reviewerName: 'John D.',
        rating: 4,
        date: '2024-01-12',
        text: 'Great breakfast option. Generous portions and fresh ingredients. Only giving 4 stars because the toast was a bit too crispy.'
    },
    {
        id: 3,
        foodId: 'f3',
        reviewerName: 'Emma L.',
        rating: 5,
        date: '2024-01-14',
        text: 'Best Caesar salad I\'ve ever had! The chicken was perfectly grilled and the dressing was amazing.'
    },
    {
        id: 4,
        foodId: 'f4',
        reviewerName: 'Mike R.',
        rating: 5,
        date: '2024-01-13',
        text: 'Incredible burger! The beef was juicy and the fries were perfectly crispy. Highly recommend!'
    },
    {
        id: 5,
        foodId: 'f5',
        reviewerName: 'Lisa K.',
        rating: 4,
        date: '2024-01-11',
        text: 'The salmon was cooked perfectly and the teriyaki sauce was delicious. Great healthy option!'
    },
    {
        id: 6,
        foodId: 'f7',
        reviewerName: 'David P.',
        rating: 5,
        date: '2024-01-10',
        text: 'Chocolate lava cake was divine! Warm, gooey center with vanilla ice cream. Perfect dessert!'
    }
];

// Nutrition data for each food item
const nutritionData = {
    'f1': { calories: 650, protein: 35, carbs: 45, fat: 28, fiber: 8 },
    'f2': { calories: 320, protein: 8, carbs: 25, fat: 22, fiber: 12 },
    'f3': { calories: 380, protein: 28, carbs: 15, fat: 18, fiber: 6 },
    'f4': { calories: 850, protein: 42, carbs: 65, fat: 45, fiber: 4 },
    'f5': { calories: 520, protein: 38, carbs: 55, fat: 18, fiber: 8 },
    'f6': { calories: 420, protein: 12, carbs: 68, fat: 14, fiber: 9 },
    'f7': { calories: 280, protein: 6, carbs: 35, fat: 14, fiber: 2 },
    'f8': { calories: 220, protein: 4, carbs: 28, fat: 8, fiber: 6 },
    'f9': { calories: 5, protein: 0, carbs: 1, fat: 0, fiber: 0 },
    'f10': { calories: 120, protein: 2, carbs: 25, fat: 1, fiber: 4 },
    'f11': { calories: 480, protein: 12, carbs: 35, fat: 28, fiber: 3 },
    'f12': { calories: 180, protein: 6, carbs: 22, fat: 8, fiber: 4 }
};

let currentFood = null;
let currentQuantity = 1;

// Initialize the page
document.addEventListener('DOMContentLoaded', () => {
    loadFoodDetails();
    setupQuantityControls();
    setupAddToCart();
    updateCartCount();
});

function loadFoodDetails() {
    // Get food ID from URL parameters
    const urlParams = new URLSearchParams(window.location.search);
    const foodId = urlParams.get('id');
    
    if (!foodId) {
        showError('Food item not found');
        return;
    }
    
    // Find the food item
    currentFood = getFoodById(foodId);
    
    if (!currentFood) {
        showError('Food item not found');
        return;
    }
    
    // Update page title
    document.title = `${currentFood.name} | SHALLION`;
    
    // Populate food details
    document.getElementById('food-title').textContent = currentFood.name;
    document.getElementById('food-description').textContent = currentFood.description;
    document.getElementById('food-price').textContent = formatCurrency(currentFood.price);
    document.getElementById('food-main-image').src = currentFood.image;
    document.getElementById('food-main-image').alt = currentFood.name;
    
    // Update rating
    const ratingElement = document.getElementById('food-rating');
    ratingElement.innerHTML = `
        <i class="fas fa-star"></i>
        <span>${currentFood.rating}</span>
    `;
    
    // Update details
    document.getElementById('preparation-time').textContent = currentFood.preparationTime;
    document.getElementById('calories').textContent = `${nutritionData[foodId]?.calories || 0} cal`;
    document.getElementById('category').textContent = currentFood.category.charAt(0).toUpperCase() + currentFood.category.slice(1);
    
    // Update badges
    const badgesContainer = document.getElementById('food-badges');
    badgesContainer.innerHTML = '';
    
    if (currentFood.isPopular) {
        badgesContainer.innerHTML += '<span class="food-badge">Popular</span>';
    }
    if (currentFood.isVegetarian) {
        badgesContainer.innerHTML += '<span class="food-badge vegetarian">Vegetarian</span>';
    }
    
    // Update allergens
    const allergensContainer = document.getElementById('allergens-list');
    if (currentFood.allergens && currentFood.allergens.length > 0) {
        allergensContainer.innerHTML = currentFood.allergens.map(allergen => 
            `<span class="allergen-tag">${allergen}</span>`
        ).join('');
    } else {
        allergensContainer.innerHTML = '<span class="allergen-tag">No allergens</span>';
    }
    
    // Update nutrition information
    const nutritionContainer = document.getElementById('nutrition-grid');
    const nutrition = nutritionData[foodId] || {};
    nutritionContainer.innerHTML = `
        <div class="nutrition-item">
            <div class="nutrition-value">${nutrition.calories || 0}</div>
            <div class="nutrition-label">Calories</div>
        </div>
        <div class="nutrition-item">
            <div class="nutrition-value">${nutrition.protein || 0}g</div>
            <div class="nutrition-label">Protein</div>
        </div>
        <div class="nutrition-item">
            <div class="nutrition-value">${nutrition.carbs || 0}g</div>
            <div class="nutrition-label">Carbs</div>
        </div>
        <div class="nutrition-item">
            <div class="nutrition-value">${nutrition.fat || 0}g</div>
            <div class="nutrition-label">Fat</div>
        </div>
    `;
    
    // Load reviews
    loadReviews(foodId);
    
    // Load related foods
    loadRelatedFoods(foodId);
}

function setupQuantityControls() {
    const minusBtn = document.getElementById('quantity-minus');
    const plusBtn = document.getElementById('quantity-plus');
    const quantityInput = document.getElementById('quantity-input');
    
    minusBtn.addEventListener('click', () => {
        if (currentQuantity > 1) {
            currentQuantity--;
            quantityInput.value = currentQuantity;
        }
    });
    
    plusBtn.addEventListener('click', () => {
        if (currentQuantity < 10) {
            currentQuantity++;
            quantityInput.value = currentQuantity;
        }
    });
    
    quantityInput.addEventListener('change', () => {
        const value = parseInt(quantityInput.value);
        if (value >= 1 && value <= 10) {
            currentQuantity = value;
        } else {
            quantityInput.value = currentQuantity;
        }
    });
}

function setupAddToCart() {
    const addToCartBtn = document.getElementById('add-to-cart-btn');
    
    addToCartBtn.addEventListener('click', () => {
        if (!currentFood) return;
        
        // Add multiple items based on quantity
        for (let i = 0; i < currentQuantity; i++) {
            cart.addItem(currentFood);
        }
        
        updateCartCount();
        showNotification(`Added ${currentQuantity} ${currentQuantity === 1 ? 'item' : 'items'} to cart!`, 'success');
        
        // Reset quantity
        currentQuantity = 1;
        document.getElementById('quantity-input').value = 1;
    });
}

function loadReviews(foodId) {
    const reviewsContainer = document.getElementById('reviews-container');
    const foodReviews = reviews.filter(review => review.foodId === foodId);
    
    if (foodReviews.length === 0) {
        reviewsContainer.innerHTML = '<p>No reviews yet. Be the first to review this item!</p>';
        return;
    }
    
    reviewsContainer.innerHTML = foodReviews.map(review => `
        <div class="review-item">
            <div class="review-header">
                <span class="reviewer-name">${review.reviewerName}</span>
                <span class="review-date">${formatDate(review.date)}</span>
            </div>
            <div class="review-rating">
                ${generateStars(review.rating)}
            </div>
            <div class="review-text">${review.text}</div>
        </div>
    `).join('');
}

function loadRelatedFoods(foodId) {
    const relatedContainer = document.getElementById('related-foods');
    const currentCategory = currentFood.category;
    
    // Get 4 related foods from the same category (excluding current food)
    const relatedFoods = foodProducts
        .filter(food => food.category === currentCategory && food.id !== foodId)
        .slice(0, 4);
    
    // If not enough from same category, add some from other categories
    if (relatedFoods.length < 4) {
        const otherFoods = foodProducts
            .filter(food => food.category !== currentCategory && food.id !== foodId)
            .slice(0, 4 - relatedFoods.length);
        relatedFoods.push(...otherFoods);
    }
    
    relatedContainer.innerHTML = relatedFoods.map(food => `
        <div class="related-food-card" onclick="window.location.href='food-details.html?id=${food.id}'">
            <div class="related-food-image">
                <img src="${food.image}" alt="${food.name}">
            </div>
            <div class="related-food-info">
                <div class="related-food-title">${food.name}</div>
                <div class="related-food-price">${formatCurrency(food.price)}</div>
            </div>
        </div>
    `).join('');
}

function generateStars(rating) {
    const fullStars = Math.floor(rating);
    const hasHalfStar = rating % 1 !== 0;
    const emptyStars = 5 - fullStars - (hasHalfStar ? 1 : 0);
    
    let stars = '';
    
    // Full stars
    for (let i = 0; i < fullStars; i++) {
        stars += '<i class="fas fa-star"></i>';
    }
    
    // Half star
    if (hasHalfStar) {
        stars += '<i class="fas fa-star-half-alt"></i>';
    }
    
    // Empty stars
    for (let i = 0; i < emptyStars; i++) {
        stars += '<i class="far fa-star"></i>';
    }
    
    return stars;
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-GB', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
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
    notification.style.backgroundColor = type === 'success' ? 'var(--primary)' : '#e74c3c';
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

function showError(message) {
    const mainContainer = document.querySelector('.food-detail-container');
    mainContainer.innerHTML = `
        <div style="grid-column: 1 / -1; text-align: center; padding: var(--space-xl);">
            <h2>Error</h2>
            <p>${message}</p>
            <a href="food-shop.html" class="btn btn-primary">Back to Food Menu</a>
        </div>
    `;
} 