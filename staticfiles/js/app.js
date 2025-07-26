import { Cart } from './cart.js';
import { CartDisplay } from './cart-display.js';
import { products, getProductsByCategory } from './products.js';
import { formatCurrency } from './helpers.js';
import { initSearch } from './search.js';

const cart = new Cart();
const cartDisplay = new CartDisplay(cart);

export function renderProducts(productsToRender = products) {
    const grid = document.getElementById('product-grid');
    if (!grid) return;
    
    grid.innerHTML = productsToRender.map(product => `
    <div class="product-card" data-category="${product.category}">
        <div class="product-image">
            <img src="${product.image}" alt="${product.name}" loading="lazy">
            ${product.stock <= 0 ? '<span class="out-of-stock">Out of Stock</span>' : ''}
        </div>
        <div class="product-info">
            <h3 class="product-title">${product.name}</h3>
            <p class="product-description">${product.description}</p>
            <div class="price-container">
                <span class="product-price">${formatCurrency(product.price)}</span>
                ${product.originalPrice ? `
                    <span class="original-price">${formatCurrency(product.originalPrice)}</span>
                ` : ''}
            </div>
            <div class="product-actions">
                <button class="btn btn-primary add-to-cart" data-id="${product.id}" ${product.stock <= 0 ? 'disabled' : ''}>
                    ${product.stock <= 0 ? 'Out of Stock' : 'Add to Cart'}
                </button>
                <a href="product-details.html?id=${product.id}" class="btn btn-details">Product Details</a>
            </div>
        </div>
    </div>
`).join('');

    // Add event listeners
    document.querySelectorAll('.add-to-cart').forEach(btn => {
        btn.addEventListener('click', (e) => {
            const productId = e.target.dataset.id;
            const product = products.find(p => p.id == productId);
            if (product) {
                cart.addItem(product);
                updateCartCount();
                
                // Show quick confirmation
                const confirmation = document.createElement('div');
                confirmation.textContent = 'Added to cart!';
                confirmation.style.position = 'fixed';
                confirmation.style.bottom = '20px';
                confirmation.style.right = '20px';
                confirmation.style.backgroundColor = 'var(--primary)';
                confirmation.style.color = 'white';
                confirmation.style.padding = 'var(--space-sm) var(--space-md)';
                confirmation.style.borderRadius = 'var(--border-radius)';
                confirmation.style.zIndex = '1000';
                confirmation.style.boxShadow = 'var(--shadow-md)';
                document.body.appendChild(confirmation);
                
                setTimeout(() => {
                    confirmation.remove();
                }, 2000);
            }
        });
    });
}

function setupCategoryFilters() {
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelector('.filter-btn.active').classList.remove('active');
            btn.classList.add('active');
            const category = btn.dataset.category;
            const filteredProducts = getProductsByCategory(category);
            renderProducts(filteredProducts);
        });
    });
}

export function updateCartCount() {
    const count = cart.getTotalItems();
    document.querySelectorAll('.cart-count').forEach(el => {
        el.textContent = count;
    });
}

export function initializeCart() {
    if (window.location.pathname.includes('cart.html')) {
        cart.renderCartItems();
    }
    updateCartCount();
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    renderProducts();
    initializeCart();
    setupCategoryFilters();
    initSearch();
});
