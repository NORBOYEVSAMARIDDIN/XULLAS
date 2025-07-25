import { formatCurrency } from './helpers.js';

export class Cart {
    constructor() {
        this.items = JSON.parse(localStorage.getItem('shallion-cart')) || [];
    }

    addItem(product, quantity = 1, selectedColor, selectedSize) {
        // Validate and set default color/size if not provided
        selectedColor = selectedColor || product.colorNames?.[0] || 'Default';
        selectedSize = selectedSize || product.sizes?.[0] || 'One Size';
        
        // Create unique variant key
        const variantKey = `${product.id}-${selectedColor}-${selectedSize}`;
        
        // Check for existing variant
        const existingItem = this.items.find(item => item.variantKey === variantKey);
        
        if (existingItem) {
            existingItem.quantity += quantity;
        } else {
            this.items.push({
                ...product,
                quantity,
                selectedColor,
                selectedSize,
                variantKey,
                displayId: `${product.id}-${Date.now()}` // Unique display ID
            });
        }
        
        this.saveToStorage();
    }

    removeItem(variantKey) {
        this.items = this.items.filter(item => item.variantKey !== variantKey);
        this.saveToStorage();
    }

    updateQuantity(variantKey, quantity) {
        const item = this.items.find(item => item.variantKey === variantKey);
        if (item) {
            item.quantity = quantity;
            if (item.quantity <= 0) {
                this.removeItem(variantKey);
            } else {
                this.saveToStorage();
            }
        }
    }

    getTotalItems() {
        return this.items.reduce((total, item) => total + item.quantity, 0);
    }

    getSubtotal() {
        return this.items.reduce((total, item) => total + (item.price * item.quantity), 0);
    }

    calculateTotal() {
        const subtotal = this.getSubtotal();
        const tax = subtotal * 0.2; // 20% VAT
        const shipping = subtotal > 50 ? 0 : 4.99;
        return {
            subtotal,
            tax,
            shipping,
            total: subtotal + tax + shipping
        };
    }

    saveToStorage() {
        localStorage.setItem('shallion-cart', JSON.stringify(this.items));
    }

    clear() {
        this.items = [];
        this.saveToStorage();
    }
}