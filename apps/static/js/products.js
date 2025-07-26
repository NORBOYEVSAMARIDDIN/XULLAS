export const products = [
    {
        id: 1,
        name: "Classic Shallion T-Shirt",
        description: "100% organic cotton crewneck tee with reinforced stitching",
        price: 24.99,
        originalPrice: 29.99,
        category: "shirts",
        colors: ["#2c3e50", "#ffffff", "#000000"],
        colorNames: ["navy", "white", "black"],
        sizes: ["S", "M", "L", "XL"],
        image: "/images/classic-tee.jpg",
        thumbnails: [
            "/images/classic-tee-1.jpg",
            "/images/classic-tee-2.jpg",
            "/images/classic-tee-3.jpg"
        ],
        stock: 42
    },
    {
        id: 2,
        name: "Premium Shallion Hoodie",
        description: "Heavyweight fleece hoodie",
        price: 59.99,
        category: "hoodies",
        colors: ["#000000", "#95a5a6", "#ff0000"],
        colorNames: ["black", "gray", "red"],
        sizes: ["M", "L", "XL"],
        image: "/images/premium-hoodie.jpg",
        thumbnails: [
            "/images/premium-hoodie-1.jpg",
            "/images/premium-hoodie-2.jpg",
            "/images/premium-hoodie-3.jpg"
        ],
        stock: 18
    },
    {
        id: 3,
        name: "Designer Shallion Apron",
        description: "Reinforced denim apron with adjustable neck strap",
        price: 34.99,
        category: "aprons",
        colors: ["#3498db", "#000000", "#ffffff"],
        colorNames: ["blue", "black", "white"],
        sizes: ["One Size"],
        image: "/images/denim-apron.jpg",
        thumbnails: [
            "/images/denim-apron-1.jpg",
            "/images/denim-apron-2.jpg",
            "/images/denim-apron-3.jpg"
        ],
        stock: 22
    },
    {
        id: 4,
        name: "Structured Shallion Cotton Cap",
        description: "Structured cap with embroidered logo",
        price: 19.99,
        category: "caps",
        colors: ["#008000", "#000000", "#ffffff"],
        colorNames: ["green", "black", "white"],
        sizes: ["Adjustable"],
        image: "/images/structured-cap.jpg",
        thumbnails: [
            "/images/structured-cap-1.jpg",
            "/images/structured-cap-2.jpg",
            "/images/structured-cap-3.jpg"
        ],
        stock: 0
    }
];

export function getProductsByCategory(category) {
    if (category === 'all') return products;
    return products.filter(product => product.category === category);
}

export function searchProducts(query) {
    const searchTerm = query.toLowerCase();
    return products.filter(product => 
        product.name.toLowerCase().includes(searchTerm) || 
        product.description.toLowerCase().includes(searchTerm) ||
        product.category.toLowerCase().includes(searchTerm)
    );
}

export function getProductById(id) {
    return products.find(product => product.id == id);
}
