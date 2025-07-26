import { Cart } from './cart.js';
import { formatCurrency } from './helpers.js';

// Initialize Stripe
const stripe = Stripe('pk_test_51RMYDPQWFBpOUOaVaUOVeom3TuwFcA8iDgidYIaNzFlZbxo2s9Mm1vFmoyMGR9hKXFE8ftoVjGkzNgRzhDjWbYIG007AzxM6f1');
const cart = new Cart();
let cardElement; // Stripe card element

document.addEventListener('DOMContentLoaded', function() {
    initializeCheckout();
});

async function initializeCheckout() {
    try {
        // Load and display cart
        const { items, subtotal, tax, shipping, total } = loadCart();
        renderOrderSummary(items, subtotal, tax, shipping, total);
        
        // Initialize payment UI
        initializeStripe();
        setupPaymentMethods();
        
        // Set up form submission
        document.getElementById('payment-form').addEventListener('submit', handleSubmit);
        
        // Ensure payment button shows correct total
        updatePaymentButton(total);
        
    } catch (error) {
        console.error('Initialization error:', error);
        showError('Failed to initialize checkout. Please refresh the page.');
    }
}

function loadCart() {
    try {
        const subtotal = cart.getSubtotal();
        const { tax, shipping, total } = cart.calculateTotal();
        
        if (isNaN(subtotal) || isNaN(tax) || isNaN(shipping) || isNaN(total)) {
            throw new Error('Invalid cart values');
        }
        
        return {
            items: cart.items,
            subtotal,
            tax,
            shipping,
            total
        };
    } catch (error) {
        console.error('Error loading cart:', error);
        throw new Error('Could not load your cart. Please try again.');
    }
}

function renderOrderSummary(items, subtotal, tax, shipping, total) {
    try {
        const orderItems = document.getElementById('order-items');
        if (!orderItems) throw new Error('Order items element not found');
        
        orderItems.innerHTML = items.map(item => `
            <div class="order-item">
                <div class="item-image">
                    <img src="${item.image || 'placeholder.jpg'}" alt="${item.name || 'Product'}">
                </div>
                <div class="item-info">
                    <h4>${item.name || 'Unnamed Product'}</h4>
                    <p>${item.selectedSize || 'One Size'}, ${item.selectedColor || 'Standard'}</p>
                    <span class="item-quantity">Qty: ${item.quantity || 1}</span>
                </div>
                <div class="item-price">
                    ${formatCurrency((item.price || 0) * (item.quantity || 1))}
                </div>
            </div>
        `).join('');

        // Update totals display
        setElementText('subtotal', formatCurrency(subtotal));
        setElementText('shipping', formatCurrency(shipping));
        setElementText('tax', formatCurrency(tax));
        setElementText('total', formatCurrency(total));
        setElementValue('total-amount', total.toFixed(2));
        
    } catch (error) {
        console.error('Error rendering order summary:', error);
        throw new Error('Could not display order summary.');
    }
}

function setElementText(id, text) {
    const element = document.getElementById(id);
    if (element) element.textContent = text;
}

function setElementValue(id, value) {
    const element = document.getElementById(id);
    if (element) element.value = value;
}

function updatePaymentButton(total) {
    const submitButton = document.getElementById('submit-button');
    if (submitButton) {
        submitButton.textContent = `Pay £${total.toFixed(2)}`;
    }
}

function initializeStripe() {
    try {
        const elements = stripe.elements();
        cardElement = elements.create('card', {
            style: {
                base: {
                    fontSize: '16px',
                    color: '#32325d',
                    '::placeholder': { color: '#aab7c4' }
                },
                invalid: {
                    color: '#fa755a',
                    iconColor: '#fa755a'
                }
            }
        });
        
        const cardElementContainer = document.getElementById('card-element');
        if (cardElementContainer) {
            cardElement.mount('#card-element');
        } else {
            throw new Error('Card element container not found');
        }
        
        cardElement.on('change', (event) => {
            const displayError = document.getElementById('card-errors');
            if (displayError) {
                displayError.textContent = event.error ? event.error.message : '';
                displayError.style.display = event.error ? 'block' : 'none';
            }
        });
        
    } catch (error) {
        console.error('Error initializing Stripe:', error);
        throw new Error('Payment system initialization failed.');
    }
}

function setupPaymentMethods() {
    try {
        const paymentMethods = document.querySelectorAll('.payment-method');
        if (!paymentMethods.length) throw new Error('No payment methods found');
        
        paymentMethods.forEach(method => {
            method.addEventListener('click', function() {
                document.querySelector('.payment-method.active')?.classList.remove('active');
                this.classList.add('active');
                
                const cardContainer = document.querySelector('.card-element-container');
                if (cardContainer) {
                    cardContainer.style.display = 
                        this.dataset.method === 'card' ? 'block' : 'none';
                }
            });
        });
        
        // Activate first payment method by default
        if (paymentMethods[0]) {
            paymentMethods[0].click();
        }
        
    } catch (error) {
        console.error('Error setting up payment methods:', error);
        throw new Error('Could not set up payment options.');
    }
}

async function handleSubmit(e) {
    e.preventDefault();
    
    // Save cart state in case of failure
    localStorage.setItem('pendingCart', JSON.stringify(cart.items));
    
    // Save order details for receipt
    const { items, subtotal, tax, shipping } = loadCart();
    saveOrderForReceipt(items, { subtotal, tax, shipping });
    
    const submitButton = document.getElementById('submit-button');
    if (!submitButton) {
        showError('Could not find payment button');
        return;
    }
    
    submitButton.disabled = true;
    submitButton.textContent = 'Processing...';
    
    try {
        // Validate form and amounts
        validateForm();
        const totalAmount = validateTotal();
        
        // Create payment method
        const { error, paymentMethod } = await stripe.createPaymentMethod({
            type: 'card',
            card: cardElement,
            billing_details: getBillingDetails()
        });
        
        if (error) throw error;
        if (!paymentMethod) throw new Error('Payment method not created');
        
        // Process payment
        const paymentResult = await processPayment(paymentMethod.id, totalAmount);
        
        if (!paymentResult.success) {
            throw new Error(paymentResult.error || 'Payment processing failed');
        }
        
        // On success
        cart.clear();
        localStorage.removeItem('pendingCart');
        redirectToSuccessPage(paymentResult.orderId, totalAmount);
        
    } catch (err) {
        console.error('Payment error:', err);
        handlePaymentError(err, submitButton);
    }
}

function saveOrderForReceipt(items, summary) {
    try {
        localStorage.setItem('pendingOrderItems', JSON.stringify(items));
        localStorage.setItem('pendingOrderSummary', JSON.stringify({
            subtotal: summary.subtotal,
            shipping: summary.shipping,
            tax: summary.tax
        }));
    } catch (e) {
        console.error('Error saving order for receipt:', e);
    }
}

function getBillingDetails() {
    return {
        name: getFormFieldValue('first-name') + ' ' + getFormFieldValue('last-name'),
        email: getFormFieldValue('email'),
        phone: getFormFieldValue('phone'),
        address: {
            line1: getFormFieldValue('address'),
            city: getFormFieldValue('city'),
            postal_code: getFormFieldValue('postcode'),
            country: getFormFieldValue('country')
        }
    };
}

function getFormFieldValue(id) {
    const element = document.getElementById(id);
    return element ? element.value.trim() : '';
}

function validateForm() {
    let isValid = true;
    const requiredFields = ['first-name', 'last-name', 'email', 'address', 'city', 'postcode', 'country'];
    
    requiredFields.forEach(fieldId => {
        const field = document.getElementById(fieldId);
        if (!field || !field.value.trim()) {
            if (field) field.style.borderColor = 'red';
            isValid = false;
        } else if (field) {
            field.style.borderColor = '';
        }
    });
    
    if (!isValid) {
        throw new Error('Please fill in all required fields');
    }
    
    return true;
}

function validateTotal() {
    const totalElement = document.getElementById('total-amount') || 
                        document.getElementById('total');
    
    if (!totalElement) {
        throw new Error('Could not find total amount element');
    }
    
    const totalText = totalElement.value || totalElement.textContent;
    const totalValue = parseFloat(totalText.replace(/[^0-9.]/g, ''));
    
    if (isNaN(totalValue) || totalValue <= 0) {
        throw new Error('Invalid order total');
    }
    
    return totalValue.toFixed(2);
}

async function processPayment(paymentMethodId, amount) {
    try {
        // In a real implementation, you would call your backend here:
        // const response = await fetch('/api/process-payment', {
        //     method: 'POST',
        //     headers: { 'Content-Type': 'application/json' },
        //     body: JSON.stringify({
        //         paymentMethodId,
        //         amount,
        //         items: cart.items
        //     })
        // });
        // return await response.json();
        
        // For demo purposes, simulate successful payment
        await new Promise(resolve => setTimeout(resolve, 1500));
        return {
            success: true,
            orderId: generateOrderId()
        };
    } catch (error) {
        console.error('Payment processing error:', error);
        return {
            success: false,
            error: error.message || 'Payment processing failed'
        };
    }
}

function redirectToSuccessPage(orderId, amount) {
    window.location.href = `payment-success.html?order_id=${orderId}&amount=${amount}`;
}

function handlePaymentError(error, submitButton) {
    const errorMessage = error.message || 'Payment processing failed';
    
    // Try to show error on page
    const errorElement = document.getElementById('card-errors');
    if (errorElement) {
        errorElement.textContent = errorMessage;
        errorElement.style.display = 'block';
        
        // Scroll to error
        errorElement.scrollIntoView({ behavior: 'smooth', block: 'center' });
    } else {
        console.error('No error element found:', errorMessage);
    }
    
    // Restore button
    if (submitButton) {
        submitButton.disabled = false;
        
        // Get current total for button text
        let totalText = '0.00';
        const totalElement = document.getElementById('total-amount') || 
                           document.getElementById('total');
        if (totalElement) {
            const totalValue = parseFloat((totalElement.value || totalElement.textContent).replace(/[^0-9.]/g, ''));
            if (!isNaN(totalValue) && totalValue > 0) {
                totalText = totalValue.toFixed(2);
            }
        }
        
        submitButton.textContent = `Pay £${totalText}`;
    }
}

function generateOrderId() {
    return 'ORD-' + Date.now().toString().slice(-8);
}

function showError(message) {
    console.error('Error:', message);
    alert(message); // Fallback error display
}