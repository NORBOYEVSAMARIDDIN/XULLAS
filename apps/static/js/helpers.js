export function formatCurrency(amount) {
    return new Intl.NumberFormat('en-GB', {
        style: 'currency',
        currency: 'GBP'
    }).format(amount);
}

export function generateOrderId() {
    return 'SH' + Date.now().toString().slice(-8);
}

export function getDeliveryDate(days = 3) {
    const date = new Date();
    date.setDate(date.getDate() + days);
    return date.toLocaleDateString('en-GB', { 
        weekday: 'long', 
        day: 'numeric',
        month: 'long'
    });
}