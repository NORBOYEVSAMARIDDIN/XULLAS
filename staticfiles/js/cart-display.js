import { Cart } from './cart.js';
import { formatCurrency } from './helpers.js';

export class CartDisplay {
    constructor(cart) {
        this.cart = cart;
        this.init();
    }

    init() {
        this.renderCartItems();
        this.setupEventDelegation();
    }

    renderCartItems() {
        const cartItemsContainer = document.getElementById('cart-items');
        if (!cartItemsContainer) return;

        if (this.cart.items.length === 0) {
            cartItemsContainer.innerHTML = `
                <div class="empty-cart-message">
                    <p>Your cart is currently empty.</p>
                    <a href="shop.html" class="btn btn-primary">Continue Shopping</a>
                </div>
            `;
            this.toggleCheckoutButton(false);
            return;
        }

        cartItemsContainer.innerHTML = this.cart.items.map(item => `
            <div class="cart-item" data-variant="${item.variantKey}">
                <img src="${item.image}" alt="${item.name}" class="cart-item-image">
                <div class="cart-item-details">
                    <h4 class="cart-item-title">${item.name}</h4>
                    <p class="cart-item-variants">${item.selectedSize}, ${item.selectedColor}</p>
                    <div class="cart-item-actions">
                        <button class="btn-quantity minus">-</button>
                        <span class="quantity">${item.quantity}</span>
                        <button class="btn-quantity plus">+</button>
                        <button class="btn-remove">Remove</button>
                    </div>
                </div>
                <div class="cart-item-price">${formatCurrency(item.price * item.quantity)}</div>
            </div>
        `).join('');

        this.updateCartSummary();
        this.toggleCheckoutButton(true);
    }

    updateCartSummary() {
        const { subtotal, shipping, total } = this.cart.calculateTotal();
        
        const updateElement = (id, value) => {
            const el = document.getElementById(id);
            if (el) el.textContent = typeof value === 'number' ? formatCurrency(value) : value;
        };

        updateElement('cart-subtotal', subtotal);
        updateElement('cart-total', total);
        updateElement('cart-shipping', shipping === 0 ? 'Free' : formatCurrency(shipping));
    }

    toggleCheckoutButton(show) {
        const checkoutBtn = document.getElementById('checkout-btn');
        if (checkoutBtn) checkoutBtn.style.display = show ? 'block' : 'none';
    }

    setupEventDelegation() {
        const cartContainer = document.getElementById('cart-items');
        if (!cartContainer) return;

        cartContainer.addEventListener('click', (e) => {
            const cartItem = e.target.closest('.cart-item');
            if (!cartItem) return;
            
            const variantKey = cartItem.dataset.variant;
            const item = this.cart.items.find(item => item.variantKey === variantKey);
            
            if (!item) return;
            
            if (e.target.classList.contains('btn-remove')) {
                this.cart.removeItem(variantKey);
                this.renderCartItems();
                this.dispatchCartUpdate();
            } 
            else if (e.target.classList.contains('minus')) {
                this.cart.updateQuantity(variantKey, Math.max(1, item.quantity - 1));
                this.renderCartItems();
                this.dispatchCartUpdate();
            }
            else if (e.target.classList.contains('plus')) {
                this.cart.updateQuantity(variantKey, item.quantity + 1);
                this.renderCartItems();
                this.dispatchCartUpdate();
            }
        });
    }

    dispatchCartUpdate() {
        document.dispatchEvent(new CustomEvent('cartUpdated', {
            detail: { cart: this.cart }
        }));
    }
}