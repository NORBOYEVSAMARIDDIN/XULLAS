import { getProductById } from './products.js';
import { Cart } from './cart.js';
import { formatCurrency } from './helpers.js';

const cart = new Cart();

document.addEventListener('DOMContentLoaded', function() {
    // Get product ID from URL
    const urlParams = new URLSearchParams(window.location.search);
    const productId = urlParams.get('id');
    const product = getProductById(productId);
    
    if (!product) {
        window.location.href = 'shop.html';
        return;
    }
    
    // Render product details
    renderProductDetails(product);
    
    // Setup event listeners
    setupEventListeners(product);
});

function renderProductDetails(product) {
    document.title = `${product.name} | SHALLION`;
    document.querySelector('.product-title').textContent = product.name;
    document.querySelector('.product-description').textContent = product.description;
    
    // Price
    const priceContainer = document.querySelector('.price-container');
    priceContainer.innerHTML = `
        <span class="product-price">${formatCurrency(product.price)}</span>
        ${product.originalPrice ? `
            <span class="original-price">${formatCurrency(product.originalPrice)}</span>
        ` : ''}
    `;
    
    // Main image
    document.querySelector('.product-main-image').src = product.image;
    document.querySelector('.product-main-image').alt = product.name;
    
    // Thumbnails
    const thumbnailsContainer = document.querySelector('.product-thumbnails');
    if (product.thumbnails && product.thumbnails.length > 0) {
        thumbnailsContainer.innerHTML = product.thumbnails.map(thumb => `
            <img src="${thumb}" alt="${product.name}" class="product-thumbnail">
        `).join('');
    } else {
        thumbnailsContainer.innerHTML = '';
    }
    
    // Colors
    const colorOptions = document.querySelector('.color-options');
    colorOptions.innerHTML = product.colors.map((color, index) => `
        <div class="color-option ${index === 0 ? 'selected' : ''}" 
             style="background: ${color}; ${color === '#ffffff' ? 'border: 1px solid #ddd' : ''}" 
             data-color="${product.colorNames[index]}">
        </div>
    `).join('');
    
    // Sizes
    const sizeOptions = document.querySelector('.size-options');
    sizeOptions.innerHTML = product.sizes.map((size, index) => `
        <div class="size-option ${index === 0 ? 'selected' : ''}" data-size="${size}">
            ${size}
        </div>
    `).join('');
}

function setupEventListeners(product) {
    // Color selection
    const colorOptions = document.querySelectorAll('.color-option');
    colorOptions.forEach(option => {
        option.addEventListener('click', function() {
            document.querySelector('.color-option.selected').classList.remove('selected');
            this.classList.add('selected');
        });
    });
    
    // Size selection
    const sizeOptions = document.querySelectorAll('.size-option');
    sizeOptions.forEach(option => {
        option.addEventListener('click', function() {
            document.querySelector('.size-option.selected').classList.remove('selected');
            this.classList.add('selected');
        });
    });
    
    // Quantity controls
    const quantityInput = document.querySelector('.quantity-controls input');
    document.querySelector('.quantity-btn.minus').addEventListener('click', () => {
        if (quantityInput.value > 1) quantityInput.value--;
    });
    document.querySelector('.quantity-btn.plus').addEventListener('click', () => {
        if (quantityInput.value < 10) quantityInput.value++;
    });
    
    // Thumbnail navigation
    document.querySelectorAll('.product-thumbnail').forEach(thumb => {
        thumb.addEventListener('click', function() {
            document.querySelector('.product-main-image').src = this.src;
        });
    });
    
    // Add to cart
    document.querySelector('.add-to-cart').addEventListener('click', function() {
        const selectedColor = document.querySelector('.color-option.selected').dataset.color;
        const selectedSize = document.querySelector('.size-option.selected').dataset.size;
        const quantity = parseInt(quantityInput.value);
        
        const productToAdd = {
            ...product,
            selectedColor,
            selectedSize,
            quantity
        };
        
        cart.addItem(productToAdd, quantity);
        updateCartCount();
        
        // Show confirmation
        alert(`${quantity} ${product.name} (${selectedSize}, ${selectedColor}) added to cart`);
    });
}

function updateCartCount() {
    const count = cart.getTotalItems();
    document.querySelectorAll('.cart-count').forEach(el => {
        el.textContent = count;
    });
}