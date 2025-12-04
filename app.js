const API = "http://127.0.0.1:8000";

let currentCartPayload = { items: [], tax: 0 }; // payload sent to /cart/build
let currentCart = null; // full cart returned from server

window.onload = () => {
    loadProducts();
    document.getElementById("checkoutBtn").onclick = checkout;
};

function loadProducts() {
    fetch(`${API}/api/products/`)
        .then(r => r.json())
        .then(products => {
            const container = document.getElementById("products");
            container.innerHTML = "";
            products.forEach(p => {
                const card = document.createElement("div");
                card.className = "product-card";
                card.innerHTML = `
                    <h3>${escapeHtml(p.name)}</h3>
                    <p>Price: $${p.price.toFixed(2)}</p>
                    <p>${escapeHtml(p.description)}</p>
                    <button onclick="addToCart('${p.id}')">Add to Cart</button>
                `;
                container.appendChild(card);
            });
        })
        .catch(err => console.error("Failed to load products", err));
}

function addToCart(productId) {
    let existing = currentCartPayload.items.find(i => i.product_id === productId);
    if (existing) existing.quantity++;
    else currentCartPayload.items.push({ product_id: productId, quantity: 1 });

    buildCart();
}

function buildCart() {
    fetch(`${API}/api/cart/build`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(currentCartPayload)
    })
    .then(r => r.json())
    .then(cart => {
        currentCart = cart;
        displayCart(cart);
    })
    .catch(err => console.error("Build cart failed", err));
}

function displayCart(cart) {
    const cartDiv = document.getElementById("cart");
    cartDiv.innerHTML = "";
    if (!cart || !cart.items || cart.items.length === 0) {
        cartDiv.innerHTML = "<p>Cart is empty</p>";
        document.getElementById("cart-summary").innerText = "";
        return;
    }
    cart.items.forEach(i => {
        const p = document.createElement("p");
        p.innerText = `${i.product.name} × ${i.quantity} = $${(i.product.price * i.quantity).toFixed(2)}`;
        cartDiv.appendChild(p);
    });
    document.getElementById("cart-summary").innerText = `Total: $${cart.total.toFixed(2)}`;
}

function checkout() {
    if (!currentCart) { alert("Cart is empty!"); return; }

    fetch(`${API}/api/orders/checkout`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            cart: currentCart,
            percent_discount: 10,
            flat_discount: 5,
            tax_rate: 0.10
        })
    })
    .then(r => {
        if (!r.ok) return r.json().then(err => { throw err; });
        return r.json();
    })
    .then(order => {
        alert("Order Success! Order ID: " + order.id);
        // clear local cart
        currentCartPayload = { items: [], tax: 0 };
        currentCart = null;
        displayCart(null);
    })
    .catch(err => {
        console.error("Checkout failed", err);
        alert("Checkout failed: " + (err.detail || JSON.stringify(err)));
    });
}

// small helper to avoid HTML injection
function escapeHtml(unsafe) {
    return unsafe
         .replace(/&/g, "&amp;")
         .replace(/</g, "&lt;")
         .replace(/>/g, "&gt;")
         .replace(/"/g, "&quot;")
         .replace(/'/g, "&#039;");
}
