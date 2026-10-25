
"use strict";

/* =========================================
   BITEBOX FOOD ORDERING APPLICATION
========================================= */

const CURRENCY = new Intl.NumberFormat("en-IN", {
  style: "currency",
  currency: "INR",
  maximumFractionDigits: 2
});

const foodItems = [
  {
    id: 1,
    name: "Margherita Pizza",
    category: "Pizza",
    price: 249,
    rating: 4.8,
    time: "20-25 min",
    description: "Classic cheese, tomato sauce and fresh basil.",
    image: "https://images.unsplash.com/photo-1574071318508-1cdbab80d002?auto=format&fit=crop&w=700&q=80"
  },
  {
    id: 2,
    name: "Pepperoni Pizza",
    category: "Pizza",
    price: 349,
    rating: 4.9,
    time: "25-30 min",
    description: "Loaded with pepperoni and melted mozzarella.",
    image: "https://images.unsplash.com/photo-1628840042765-356cda07504e?auto=format&fit=crop&w=700&q=80"
  },
  {
    id: 3,
    name: "Classic Cheeseburger",
    category: "Burger",
    price: 179,
    rating: 4.7,
    time: "15-20 min",
    description: "Juicy patty, cheese, lettuce and house sauce.",
    image: "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?auto=format&fit=crop&w=700&q=80"
  },
  {
    id: 4,
    name: "Crispy Chicken Burger",
    category: "Burger",
    price: 219,
    rating: 4.8,
    time: "20-25 min",
    description: "Crispy chicken with creamy, spicy mayo.",
    image: "https://images.unsplash.com/photo-1606755962773-d324e0a13086?auto=format&fit=crop&w=700&q=80"
  },
  {
    id: 5,
    name: "Paneer Butter Masala",
    category: "Indian",
    price: 259,
    rating: 4.9,
    time: "25-30 min",
    description: "Soft paneer in a rich and creamy tomato gravy.",
    image: "https://images.unsplash.com/photo-1631452180519-c014fe946bc7?auto=format&fit=crop&w=700&q=80"
  },
  {
    id: 6,
    name: "Chicken Biryani",
    category: "Indian",
    price: 299,
    rating: 4.9,
    time: "25-35 min",
    description: "Fragrant basmati rice with aromatic spices.",
    image: "https://images.unsplash.com/photo-1589302168068-964664d93dc0?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=NHwxMjA3fDA%3D"
  },
  {
    id: 7,
    name: "Masala Dosa",
    category: "Indian",
    price: 129,
    rating: 4.6,
    time: "15-20 min",
    description: "Golden crispy dosa served with chutney and sambar.",
    image: "https://images.unsplash.com/photo-1668236543090-82eba5ee5976?auto=format&fit=crop&w=700&q=80"
  },
  {
    id: 8,
    name: "Veg Fried Rice",
    category: "Indian",
    price: 169,
    rating: 4.5,
    time: "15-20 min",
    description: "Wok-tossed rice with fresh vegetables and spices.",
    image: "https://images.unsplash.com/photo-1603133872878-684f208fb84b?auto=format&fit=crop&w=700&q=80"
  },
  {
    id: 9,
    name: "Chocolate Brownie",
    category: "Dessert",
    price: 119,
    rating: 4.8,
    time: "10-15 min",
    description: "Rich chocolate brownie with a fudgy centre.",
    image: "https://images.unsplash.com/photo-1606313564200-e75d5e30476c?auto=format&fit=crop&w=700&q=80"
  },
  {
    id: 10,
    name: "Strawberry Cheesecake",
    category: "Dessert",
    price: 159,
    rating: 4.7,
    time: "10-15 min",
    description: "Creamy cheesecake with strawberry topping.",
    image: "https://images.unsplash.com/photo-1533134242443-d4fd215305ad?auto=format&fit=crop&w=700&q=80"
  },
  {
    id: 11,
    name: "Fresh Lemonade",
    category: "Drinks",
    price: 69,
    rating: 4.5,
    time: "5-10 min",
    description: "Refreshing lemonade with a hint of mint.",
    image: "https://images.unsplash.com/photo-1665582313032-29058cee9c94?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=NHwxMjA3fDA%3D"
  },
  {
    id: 12,
    name: "Cold Coffee",
    category: "Drinks",
    price: 99,
    rating: 4.6,
    time: "5-10 min",
    description: "Chilled coffee blended with creamy milk.",
    image: "https://images.unsplash.com/photo-1461023058943-07fcbe16d735?auto=format&fit=crop&w=700&q=80"
  }
];

/* =========================================
   HELPERS AND LOCAL STORAGE
========================================= */

function formatMoney(amount) {
  return CURRENCY.format(amount);
}

function escapeHTML(value) {
  return String(value ?? "").replace(/[&<>"']/g, character => ({
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    '"': "&quot;",
    "'": "&#39;"
  })[character]);
}

function readStorage(key, fallback) {
  try {
    const value = localStorage.getItem(key);
    return value === null ? fallback : JSON.parse(value);
  } catch {
    return fallback;
  }
}

function writeStorage(key, value) {
  try {
    localStorage.setItem(key, JSON.stringify(value));
    return true;
  } catch {
    showToast("Could not save data. Check your browser storage.");
    return false;
  }
}

function getCart() {
  const cart = readStorage("biteboxCart", []);
  return Array.isArray(cart) ? cart : [];
}

function saveCart(cart) {
  return writeStorage("biteboxCart", cart);
}

function getOrders() {
  const orders = readStorage("biteboxOrders", []);
  return Array.isArray(orders) ? orders : [];
}

function saveOrders(orders) {
  return writeStorage("biteboxOrders", orders);
}

function getFood(id) {
  return foodItems.find(item => item.id === Number(id));
}

let activeCategory = "All";
let toastTimeout;

/* =========================================
   TOAST MESSAGE
========================================= */

function showToast(message) {
  const toast = document.getElementById("toast");
  toast.textContent = message;
  toast.classList.add("show");

  clearTimeout(toastTimeout);
  toastTimeout = setTimeout(() => {
    toast.classList.remove("show");
  }, 2600);
}

/* =========================================
   RENDER FOOD MENU
========================================= */

const foodGrid = document.getElementById("foodGrid");
const searchInput = document.getElementById("searchInput");
const sortSelect = document.getElementById("sortSelect");
const noResults = document.getElementById("noResults");

function renderFood() {
  const searchText = searchInput.value.trim().toLowerCase();

  let results = foodItems.filter(item => {
    const matchesCategory =
      activeCategory === "All" || item.category === activeCategory;

    const matchesSearch =
      item.name.toLowerCase().includes(searchText) ||
      item.category.toLowerCase().includes(searchText) ||
      item.description.toLowerCase().includes(searchText);

    return matchesCategory && matchesSearch;
  });

  switch (sortSelect.value) {
    case "low":
      results.sort((a, b) => a.price - b.price);
      break;
    case "high":
      results.sort((a, b) => b.price - a.price);
      break;
    case "rating":
      results.sort((a, b) => b.rating - a.rating);
      break;
    default:
      results.sort((a, b) => a.id - b.id);
  }

  foodGrid.innerHTML = results.map(item => `
    <article class="food-card">
      <div class="food-image-wrap">
        <img
          class="food-image"
          src="${escapeHTML(item.image)}"
          alt="${escapeHTML(item.name)}"
          loading="lazy"
        >
        <span class="food-category">${escapeHTML(item.category)}</span>
      </div>

      <div class="food-details">
        <div class="food-meta">
          <span class="food-rating">★ ${item.rating.toFixed(1)}</span>
          <span class="food-time">◷ ${escapeHTML(item.time)}</span>
        </div>

        <h3>${escapeHTML(item.name)}</h3>
        <p class="food-description">${escapeHTML(item.description)}</p>

        <div class="food-bottom">
          <span class="food-price">${formatMoney(item.price)}</span>
          <button
            class="add-button"
            type="button"
            data-add="${item.id}"
            aria-label="Add ${escapeHTML(item.name)} to cart"
          >+</button>
        </div>
      </div>
    </article>
  `).join("");

  noResults.hidden = results.length > 0;
}

searchInput.addEventListener("input", renderFood);
sortSelect.addEventListener("change", renderFood);

document.getElementById("categoryList").addEventListener("click", event => {
  const button = event.target.closest("[data-category]");
  if (!button) return;

  activeCategory = button.dataset.category;

  document.querySelectorAll(".category-button").forEach(categoryButton => {
    categoryButton.classList.toggle("active", categoryButton === button);
  });

  renderFood();
});

/* =========================================
   CART OPERATIONS
========================================= */

const cartDrawer = document.getElementById("cartDrawer");
const cartOverlay = document.getElementById("cartOverlay");
const cartItemsElement = document.getElementById("cartItems");

function openCart() {
  cartDrawer.classList.add("open");
  cartOverlay.classList.add("open");
  document.body.classList.add("no-scroll");
}

function closeCart() {
  cartDrawer.classList.remove("open");
  cartOverlay.classList.remove("open");

  if (!document.getElementById("checkoutModal").classList.contains("open") &&
      !document.getElementById("confirmationModal").classList.contains("open")) {
    document.body.classList.remove("no-scroll");
  }
}

document.getElementById("cartButton").addEventListener("click", openCart);
document.getElementById("closeCart").addEventListener("click", closeCart);
cartOverlay.addEventListener("click", closeCart);

foodGrid.addEventListener("click", event => {
  const button = event.target.closest("[data-add]");
  if (!button) return;

  addToCart(Number(button.dataset.add));
});

function addToCart(foodId) {
  const food = getFood(foodId);
  if (!food) return;

  const cart = getCart();
  const existingItem = cart.find(item => item.id === foodId);

  if (existingItem) {
    existingItem.quantity += 1;
  } else {
    cart.push({ id: foodId, quantity: 1 });
  }

  if (saveCart(cart)) {
    renderCart();
    showToast(`${food.name} added to cart!`);
  }
}

function changeQuantity(foodId, change) {
  const cart = getCart();
  const item = cart.find(cartItem => cartItem.id === foodId);

  if (!item) return;

  item.quantity += change;

  const updatedCart = cart.filter(cartItem => cartItem.quantity > 0);
  saveCart(updatedCart);
  renderCart();
}

function removeFromCart(foodId) {
  const updatedCart = getCart().filter(item => item.id !== foodId);
  saveCart(updatedCart);
  renderCart();
  showToast("Item removed from cart.");
}

function calculateTotals() {
  const cart = getCart();

  const subtotal = cart.reduce((sum, cartItem) => {
    const food = getFood(cartItem.id);
    return food ? sum + food.price * cartItem.quantity : sum;
  }, 0);

  const delivery = subtotal === 0 || subtotal >= 500 ? 0 : 40;
  const tax = Math.round(subtotal * 0.05 * 100) / 100;
  const total = Math.round((subtotal + delivery + tax) * 100) / 100;

  return { subtotal, delivery, tax, total };
}

function renderCart() {
  const cart = getCart().filter(item =>
    getFood(item.id) && Number.isInteger(item.quantity) && item.quantity > 0
  );

  document.getElementById("cartCount").textContent =
    cart.reduce((sum, item) => sum + item.quantity, 0);

  if (cart.length === 0) {
    cartItemsElement.innerHTML =
      '<p class="empty-cart">Your cart is empty. Add something delicious! 🍕</p>';
  } else {
    cartItemsElement.innerHTML = cart.map(cartItem => {
      const food = getFood(cartItem.id);

      return `
        <div class="cart-item">
          <img src="${escapeHTML(food.image)}" alt="${escapeHTML(food.name)}">
          <div>
            <h4>${escapeHTML(food.name)}</h4>
            <span class="cart-item-price">${formatMoney(food.price * cartItem.quantity)}</span>
            <div class="cart-item-actions">
              <button class="quantity-button" data-quantity="${food.id}" data-change="-1"
                aria-label="Decrease ${escapeHTML(food.name)} quantity">−</button>
              <span>${cartItem.quantity}</span>
              <button class="quantity-button" data-quantity="${food.id}" data-change="1"
                aria-label="Increase ${escapeHTML(food.name)} quantity">+</button>
              <button class="remove-button" data-remove="${food.id}">Remove</button>
            </div>
          </div>
        </div>
      `;
    }).join("");
  }

  const totals = calculateTotals();

  document.getElementById("subtotal").textContent = formatMoney(totals.subtotal);
  document.getElementById("deliveryFee").textContent = formatMoney(totals.delivery);
  document.getElementById("tax").textContent = formatMoney(totals.tax);
  document.getElementById("grandTotal").textContent = formatMoney(totals.total);
  document.getElementById("checkoutTotal").textContent = formatMoney(totals.total);

  document.getElementById("checkoutButton").disabled = cart.length === 0;
}

cartItemsElement.addEventListener("click", event => {
  const quantityButton = event.target.closest("[data-quantity]");
  const removeButton = event.target.closest("[data-remove]");

  if (quantityButton) {
    changeQuantity(
      Number(quantityButton.dataset.quantity),
      Number(quantityButton.dataset.change)
    );
  }

  if (removeButton) {
    removeFromCart(Number(removeButton.dataset.remove));
  }
});

/* =========================================
   CHECKOUT AND ORDER CREATION
========================================= */

const checkoutModal = document.getElementById("checkoutModal");
const confirmationModal = document.getElementById("confirmationModal");
const checkoutForm = document.getElementById("checkoutForm");

let lastPlacedOrderId = null;

function openModal(modal) {
  modal.classList.add("open");
  document.body.classList.add("no-scroll");
}

function closeModal(modal) {
  modal.classList.remove("open");

  if (!cartDrawer.classList.contains("open") &&
      !checkoutModal.classList.contains("open") &&
      !confirmationModal.classList.contains("open")) {
    document.body.classList.remove("no-scroll");
  }
}

document.getElementById("checkoutButton").addEventListener("click", () => {
  if (getCart().length === 0) {
    showToast("Your cart is empty.");
    return;
  }

  closeCart();
  document.getElementById("checkoutTotal").textContent =
    formatMoney(calculateTotals().total);
  openModal(checkoutModal);
});

document.getElementById("closeCheckout").addEventListener("click", () => {
  closeModal(checkoutModal);
});

checkoutModal.addEventListener("click", event => {
  if (event.target === checkoutModal) closeModal(checkoutModal);
});

confirmationModal.addEventListener("click", event => {
  if (event.target === confirmationModal) closeModal(confirmationModal);
});

checkoutForm.addEventListener("submit", event => {
  event.preventDefault();

  const cart = getCart().filter(item =>
    getFood(item.id) && item.quantity > 0
  );

  if (cart.length === 0) {
    closeModal(checkoutModal);
    showToast("Your cart is empty.");
    return;
  }

  if (!checkoutForm.reportValidity()) return;

  const customerName = document.getElementById("customerName").value.trim();
  const customerPhone = document.getElementById("customerPhone").value.trim();
  const customerAddress = document.getElementById("customerAddress").value.trim();
  const paymentMethod = document.getElementById("paymentMethod").value;

  if (!customerName || !customerAddress || !/^[0-9]{10}$/.test(customerPhone)) {
    showToast("Please enter valid checkout details.");
    return;
  }

  const totals = calculateTotals();
  const createdAt = new Date().toISOString();

  // Use a timestamp-based ID and check for collisions.
  const orders = getOrders();
  let orderId;

  do {
    orderId = "BB" + Date.now().toString().slice(-8) +
      Math.floor(Math.random() * 10);
  } while (orders.some(order => order.orderId === orderId));

  const order = {
    orderId,
    customerName,
    customerPhone,
    address: customerAddress,
    paymentMethod,
    items: cart.map(item => ({
      id: item.id,
      name: getFood(item.id).name,
      price: getFood(item.id).price,
      quantity: item.quantity
    })),
    subtotal: totals.subtotal,
    deliveryFee: totals.delivery,
    tax: totals.tax,
    total: totals.total,
    statusIndex: 0,
    status: "Order Confirmed",
    createdAt,
    updatedAt: createdAt
  };

  orders.push(order);

  // Do not clear the cart if the order couldn't be saved.
  if (!saveOrders(orders)) return;

  try {
    localStorage.setItem("biteboxLatestOrderId", orderId);
  } catch {
    showToast("Order saved, but the latest-order shortcut could not be saved.");
  }

  lastPlacedOrderId = orderId;

  saveCart([]);
  renderCart();
  checkoutForm.reset();
  closeModal(checkoutModal);

  document.getElementById("confirmationOrderId").textContent = orderId;
  openModal(confirmationModal);
});

document.getElementById("trackNewOrderBtn").addEventListener("click", () => {
  if (!lastPlacedOrderId) return;

  closeModal(confirmationModal);
  document.getElementById("trackingOrderId").value = lastPlacedOrderId;
  showTracking(lastPlacedOrderId);

  document.getElementById("tracking").scrollIntoView({ behavior: "smooth" });
});

document.getElementById("continueShoppingBtn").addEventListener("click", () => {
  closeModal(confirmationModal);
  document.getElementById("menu").scrollIntoView({ behavior: "smooth" });
});

/* =========================================
   ORDER TRACKING
========================================= */

const trackingStages = [
  "Order Confirmed",
  "Preparing Your Food",
  "Out for Delivery",
  "Delivered"
];

const trackingForm = document.getElementById("trackingForm");
const trackingInput = document.getElementById("trackingOrderId");
const trackingResult = document.getElementById("trackingResult");
const trackingMessage = document.getElementById("trackingMessage");
const advanceTrackingButton = document.getElementById("advanceTrackingBtn");

let currentTrackingOrderId = null;

function findOrder(orderId) {
  const normalizedId = orderId.trim().toLowerCase();

  return getOrders().find(order =>
    String(order.orderId).toLowerCase() === normalizedId
  );
}

function showTracking(orderId) {
  const order = findOrder(orderId);

  if (!order) {
    trackingResult.hidden = true;
    trackingMessage.textContent =
      "Order not found. Check your order ID and try again.";
    trackingMessage.style.color = "#b42318";
    currentTrackingOrderId = null;
    return;
  }

  const statusIndex = Math.max(
    0,
    Math.min(
      Number.isInteger(Number(order.statusIndex)) ? Number(order.statusIndex) : 0,
      trackingStages.length - 1
    )
  );

  currentTrackingOrderId = order.orderId;
  trackingResult.hidden = false;
  trackingMessage.textContent = "";
  trackingMessage.style.color = "";

  document.getElementById("displayOrderId").textContent = order.orderId;
  document.getElementById("trackingStatusBadge").textContent =
    trackingStages[statusIndex];
  document.getElementById("trackingCustomer").textContent =
    "Customer: " + (order.customerName || "Customer");
  document.getElementById("trackingTotal").textContent =
    "Order total: " + formatMoney(Number(order.total) || 0);
  document.getElementById("trackingAddress").textContent =
    "Delivery address: " + (order.address || "Not available");

  document.querySelectorAll(".tracking-step").forEach((step, index) => {
    step.classList.toggle("completed", index < statusIndex);
    step.classList.toggle("current", index === statusIndex);
  });

  const updateDate = order.updatedAt ? new Date(order.updatedAt) : null;
  document.getElementById("trackingUpdated").textContent =
    "Last updated: " +
    (updateDate && !Number.isNaN(updateDate.getTime())
      ? updateDate.toLocaleString()
      : "Not available");

  advanceTrackingButton.disabled = statusIndex === trackingStages.length - 1;
  advanceTrackingButton.textContent =
    statusIndex === trackingStages.length - 1
      ? "Order Delivered ✓"
      : "Move to Next Stage";
}

trackingForm.addEventListener("submit", event => {
  event.preventDefault();
  showTracking(trackingInput.value);
});

document.getElementById("latestOrderBtn").addEventListener("click", () => {
  let latestOrderId = null;

  try {
    latestOrderId = localStorage.getItem("biteboxLatestOrderId");
  } catch {
    // The manual order ID field still works.
  }

  if (!latestOrderId) {
    const orders = getOrders();
    latestOrderId = orders.length ? orders[orders.length - 1].orderId : null;
  }

  if (!latestOrderId) {
    trackingResult.hidden = true;
    trackingMessage.textContent = "You haven't placed an order yet.";
    trackingMessage.style.color = "#b42318";
    return;
  }

  trackingInput.value = latestOrderId;
  showTracking(latestOrderId);
});

advanceTrackingButton.addEventListener("click", () => {
  if (!currentTrackingOrderId) return;

  const orders = getOrders();
  const order = orders.find(item => item.orderId === currentTrackingOrderId);

  if (!order) {
    showTracking(currentTrackingOrderId);
    return;
  }

  const currentIndex = Math.max(0, Number(order.statusIndex) || 0);

  if (currentIndex >= trackingStages.length - 1) {
    showTracking(order.orderId);
    return;
  }

  order.statusIndex = currentIndex + 1;
  order.status = trackingStages[order.statusIndex];
  order.updatedAt = new Date().toISOString();

  if (saveOrders(orders)) {
    showTracking(order.orderId);
    showToast("Order status updated: " + order.status);
  }
});

/* =========================================
   MOBILE NAVIGATION AND INITIALIZATION
========================================= */

const menuToggle = document.getElementById("menuToggle");
const navLinks = document.getElementById("navLinks");

menuToggle.addEventListener("click", () => {
  const isOpen = navLinks.classList.toggle("open");
  menuToggle.setAttribute("aria-expanded", String(isOpen));
  menuToggle.textContent = isOpen ? "✕" : "☰";
});

navLinks.querySelectorAll("a").forEach(link => {
  link.addEventListener("click", () => {
    navLinks.classList.remove("open");
    menuToggle.setAttribute("aria-expanded", "false");
    menuToggle.textContent = "☰";
  });
});

document.addEventListener("keydown", event => {
  if (event.key === "Escape") {
    closeCart();
    closeModal(checkoutModal);
    closeModal(confirmationModal);
    navLinks.classList.remove("open");
    menuToggle.setAttribute("aria-expanded", "false");
    menuToggle.textContent = "☰";
  }
});

document.getElementById("currentYear").textContent = new Date().getFullYear();

renderFood();
renderCart();
