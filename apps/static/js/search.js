import { searchProducts } from './products.js';
import { renderProducts } from './app.js';

export function initSearch() {
    const searchInput = document.getElementById('search-input');
    const searchBtn = document.getElementById('search-btn');
    
    if (!searchInput || !searchBtn) return;
    
    function performSearch() {
        const query = searchInput.value.trim();
        const results = searchProducts(query);
        renderProducts(results);
    }
    
    searchBtn.addEventListener('click', performSearch);
    searchInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') performSearch();
    });
}

document.addEventListener('DOMContentLoaded', initSearch);