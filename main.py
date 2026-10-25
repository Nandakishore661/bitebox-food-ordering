import tkinter as tk
from tkinter import ttk, messagebox
import random
from datetime import datetime

# -------------------- COLORS --------------------

BG = "#FFF8F1"
ORANGE = "#E85D04"
DARK = "#292321"
WHITE = "#FFFFFF"
GREEN = "#218838"

# -------------------- FOOD DATA --------------------

foods = [
    {
        "id": 1,
        "name": "Cheese Pizza",
        "restaurant": "Oven Story",
        "category": "Pizza",
        "price": 249,
        "rating": 4.5,
        "emoji": "🍕"
    },
    {
        "id": 2,
        "name": "Veg Burger",
        "restaurant": "Burger Hub",
        "category": "Burger",
        "price": 129,
        "rating": 4.3,
        "emoji": "🍔"
    },
    {
        "id": 3,
        "name": "Chicken Biryani",
        "restaurant": "Hyderabad Spice",
        "category": "Biryani",
        "price": 219,
        "rating": 4.8,
        "emoji": "🍛"
    },
    {
        "id": 4,
        "name": "Masala Dosa",
        "restaurant": "South Tiffins",
        "category": "South Indian",
        "price": 99,
        "rating": 4.4,
        "emoji": "🥞"
    },
    {
        "id": 5,
        "name": "Chocolate Brownie",
        "restaurant": "Sweet Tooth",
        "category": "Dessert",
        "price": 119,
        "rating": 4.6,
        "emoji": "🍫"
    },
    {
        "id": 6,
        "name": "Paneer Wrap",
        "restaurant": "Wrap House",
        "category": "Wraps",
        "price": 159,
        "rating": 4.2,
        "emoji": "🌯"
    },
    {
        "id": 7,
        "name": "French Fries",
        "restaurant": "Burger Hub",
        "category": "Snacks",
        "price": 89,
        "rating": 4.1,
        "emoji": "🍟"
    },
    {
        "id": 8,
        "name": "Cold Coffee",
        "restaurant": "Cafe Cloud",
        "category": "Drinks",
        "price": 109,
        "rating": 4.3,
        "emoji": "🥤"
    }
]


# -------------------- APPLICATION --------------------

class QuickBite:

    def __init__(self, root):
        self.root = root

        self.root.title("QuickBite Food Delivery")
        self.root.geometry("1150x800")
        self.root.configure(bg=BG)

        self.cart = {}
        self.favorites = set()
        self.orders = []
        self.current_category = "All"

        self.create_header()
        self.create_banner()
        self.create_categories()
        self.create_food_area()
        self.create_footer()

        self.display_foods()

    # -------------------- HEADER --------------------

    def create_header(self):

        header = tk.Frame(
            self.root,
            bg=WHITE,
            height=75
        )
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header,
            text="🍊 QuickBite",
            font=("Arial", 23, "bold"),
            bg=WHITE,
            fg=ORANGE
        ).pack(side="left", padx=25)

        self.search = tk.Entry(
            header,
            font=("Arial", 12),
            width=25,
            relief="flat",
            bg="#F2F2F2"
        )
        self.search.pack(side="left", padx=20, ipady=9)

        self.search.insert(0, "")
        self.search.bind(
            "<KeyRelease>",
            lambda event: self.display_foods()
        )

        tk.Button(
            header,
            text="♡ Favorites",
            command=self.show_favorites,
            bg=WHITE,
            fg=DARK,
            relief="flat",
            font=("Arial", 10, "bold")
        ).pack(side="right", padx=8)

        self.cart_button = tk.Button(
            header,
            text="🛒 Cart (0)",
            command=self.open_cart,
            bg=ORANGE,
            fg=WHITE,
            relief="flat",
            font=("Arial", 10, "bold"),
            padx=15,
            pady=10
        )
        self.cart_button.pack(side="right", padx=20)

    # -------------------- BANNER --------------------

    def create_banner(self):

        banner = tk.Frame(
            self.root,
            bg="#321B12",
            height=145
        )
        banner.pack(fill="x", padx=22, pady=18)
        banner.pack_propagate(False)

        tk.Label(
            banner,
            text="GOOD FOOD. GOOD MOOD.",
            font=("Arial", 11, "bold"),
            bg="#321B12",
            fg="#FFC078"
        ).pack(anchor="w", padx=25, pady=(20, 5))

        tk.Label(
            banner,
            text="Your cravings, delivered!",
            font=("Arial", 25, "bold"),
            bg="#321B12",
            fg=WHITE
        ).pack(anchor="w", padx=25)

        tk.Label(
            banner,
            text="Discover delicious food near you.",
            font=("Arial", 11),
            bg="#321B12",
            fg="#E9D8CF"
        ).pack(anchor="w", padx=25, pady=5)

    # -------------------- CATEGORIES --------------------

    def create_categories(self):

        frame = tk.Frame(self.root, bg=BG)
        frame.pack(fill="x", padx=22, pady=5)

        tk.Label(
            frame,
            text="Explore Menu",
            font=("Arial", 19, "bold"),
            bg=BG,
            fg=DARK
        ).pack(anchor="w", pady=(0, 10))

        categories = [
            "All",
            "Pizza",
            "Burger",
            "Biryani",
            "South Indian",
            "Dessert",
            "Wraps",
            "Snacks",
            "Drinks"
        ]

        for category in categories:

            tk.Button(
                frame,
                text=category,
                command=lambda c=category:
                    self.select_category(c),
                bg=WHITE,
                fg=DARK,
                relief="flat",
                padx=10,
                pady=7
            ).pack(side="left", padx=(0, 5))

    def select_category(self, category):

        self.current_category = category
        self.display_foods()

    # -------------------- FOOD AREA --------------------

    def create_food_area(self):

        container = tk.Frame(self.root, bg=BG)
        container.pack(fill="both", expand=True, padx=18)

        self.canvas = tk.Canvas(
            container,
            bg=BG,
            highlightthickness=0
        )

        scrollbar = ttk.Scrollbar(
            container,
            orient="vertical",
            command=self.canvas.yview
        )

        self.food_frame = tk.Frame(
            self.canvas,
            bg=BG
        )

        self.canvas.create_window(
            (0, 0),
            window=self.food_frame,
            anchor="nw"
        )

        self.food_frame.bind(
            "<Configure>",
            lambda event:
                self.canvas.configure(
                    scrollregion=self.canvas.bbox("all")
                )
        )

        self.canvas.configure(
            yscrollcommand=scrollbar.set
        )

        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    # -------------------- DISPLAY FOODS --------------------

    def display_foods(self):

        for widget in self.food_frame.winfo_children():
            widget.destroy()

        query = self.search.get().strip().lower()

        filtered = []

        for food in foods:

            if (
                self.current_category != "All"
                and food["category"] != self.current_category
            ):
                continue

            text = (
                food["name"]
                + " "
                + food["restaurant"]
                + " "
                + food["category"]
            ).lower()

            if query and query not in text:
                continue

            filtered.append(food)

        for index, food in enumerate(filtered):

            row = index // 3
            column = index % 3

            card = tk.Frame(
                self.food_frame,
                bg=WHITE,
                highlightbackground="#E7D8CC",
                highlightthickness=1
            )

            card.grid(
                row=row,
                column=column,
                padx=9,
                pady=9,
                sticky="nsew"
            )

            self.food_frame.grid_columnconfigure(
                column,
                weight=1
            )

            tk.Label(
                card,
                text=food["emoji"],
                font=("Segoe UI Emoji", 48),
                bg="#FFE8D0",
                width=10,
                pady=15
            ).pack(fill="x")

            tk.Label(
                card,
                text=food["name"],
                font=("Arial", 12, "bold"),
                bg=WHITE,
                fg=DARK
            ).pack(anchor="w", padx=12, pady=(10, 3))

            tk.Label(
                card,
                text=food["restaurant"],
                font=("Arial", 10),
                bg=WHITE,
                fg="#777777"
            ).pack(anchor="w", padx=12)

            tk.Label(
                card,
                text=f"★ {food['rating']}  •  {food['category']}",
                font=("Arial", 10),
                bg=WHITE,
                fg=GREEN
            ).pack(anchor="w", padx=12, pady=5)

            bottom = tk.Frame(card, bg=WHITE)
            bottom.pack(fill="x", padx=12, pady=10)

            tk.Label(
                bottom,
                text=f"₹{food['price']}",
                font=("Arial", 15, "bold"),
                bg=WHITE
            ).pack(side="left")

            tk.Button(
                bottom,
                text="+ Add",
                command=lambda f=food:
                    self.add_to_cart(f),
                bg=ORANGE,
                fg=WHITE,
                relief="flat",
                padx=15,
                pady=6
            ).pack(side="right")

            tk.Button(
                card,
                text=(
                    "♥ Saved"
                    if food["id"] in self.favorites
                    else "♡ Favorite"
                ),
                command=lambda f=food:
                    self.toggle_favorite(f),
                bg=WHITE,
                fg=ORANGE,
                relief="flat"
            ).pack(anchor="e", padx=8, pady=(0, 8))

            # Hover effect
            card.bind(
                "<Enter>",
                lambda event, c=card:
                    c.configure(highlightbackground=ORANGE,
                                highlightthickness=2)
            )

            card.bind(
                "<Leave>",
                lambda event, c=card:
                    c.configure(highlightbackground="#E7D8CC",
                                highlightthickness=1)
            )

    # -------------------- FAVORITES --------------------

    def toggle_favorite(self, food):

        if food["id"] in self.favorites:
            self.favorites.remove(food["id"])
        else:
            self.favorites.add(food["id"])

        self.display_foods()

    def show_favorites(self):

        if not self.favorites:
            messagebox.showinfo(
                "Favorites",
                "Save a food using the Favorite button first."
            )
            return

        win = tk.Toplevel(self.root)
        win.title("My Favorites")
        win.geometry("400x450")
        win.configure(bg=BG)

        tk.Label(
            win,
            text="My Favorite Foods",
            font=("Arial", 19, "bold"),
            bg=BG
        ).pack(pady=15)

        for food in foods:
            if food["id"] in self.favorites:
                tk.Label(
                    win,
                    text=f"{food['emoji']}  {food['name']} — ₹{food['price']}",
                    font=("Arial", 11),
                    bg=BG
                ).pack(anchor="w", padx=20, pady=7)

    # -------------------- CART --------------------

    def add_to_cart(self, food):

        food_id = food["id"]

        self.cart[food_id] = self.cart.get(food_id, 0) + 1

        self.update_cart_button()
        self.display_foods()

        self.set_status(
            f"Added {food['name']} to your cart."
        )

    def update_cart_button(self):

        quantity = sum(self.cart.values())

        self.cart_button.configure(
            text=f"🛒 Cart ({quantity})"
        )

    def calculate_total(self):

        subtotal = sum(
            next(f["price"] for f in foods if f["id"] == food_id)
            * quantity
            for food_id, quantity in self.cart.items()
        )

        delivery = 0 if subtotal == 0 or subtotal >= 499 else 35

        return subtotal, delivery, subtotal + delivery

    def open_cart(self):

        win = tk.Toplevel(self.root)
        win.title("Your Cart")
        win.geometry("550x600")
        win.configure(bg=BG)

        tk.Label(
            win,
            text="Your Shopping Cart 🛒",
            font=("Arial", 20, "bold"),
            bg=BG
        ).pack(anchor="w", padx=20, pady=20)

        body = tk.Frame(win, bg=BG)
        body.pack(fill="both", expand=True, padx=20)

        if not self.cart:

            tk.Label(
                body,
                text="Your cart is empty!",
                font=("Arial", 13),
                bg=BG
            ).pack(pady=30)

        for food_id, quantity in list(self.cart.items()):

            food = next(f for f in foods if f["id"] == food_id)

            row = tk.Frame(body, bg=WHITE, padx=10, pady=10)
            row.pack(fill="x", pady=5)

            tk.Label(
                row,
                text=f"{food['emoji']}  {food['name']}",
                font=("Arial", 10, "bold"),
                bg=WHITE
            ).pack(side="left")

            tk.Button(
                row,
                text="−",
                command=lambda fid=food_id, w=win:
                    self.change_quantity(fid, -1, w)
            ).pack(side="right")

            tk.Label(
                row,
                text=str(quantity),
                bg=WHITE,
                width=3
            ).pack(side="right")

            tk.Button(
                row,
                text="+",
                command=lambda fid=food_id, w=win:
                    self.change_quantity(fid, 1, w)
            ).pack(side="right")

            tk.Label(
                row,
                text=f"₹{food['price'] * quantity}",
                bg=WHITE,
                fg=ORANGE
            ).pack(side="right", padx=10)

        subtotal, delivery, total = self.calculate_total()

        summary = tk.Frame(win, bg=WHITE, padx=18, pady=15)
        summary.pack(fill="x", padx=20, pady=10)

        tk.Label(
            summary,
            text=f"Subtotal: ₹{subtotal}",
            bg=WHITE,
            font=("Arial", 11)
        ).pack(anchor="w")

        tk.Label(
            summary,
            text=f"Delivery: ₹{delivery}",
            bg=WHITE,
            font=("Arial", 11)
        ).pack(anchor="w", pady=3)

        tk.Label(
            summary,
            text=f"Total: ₹{total}",
            bg=WHITE,
            fg=ORANGE,
            font=("Arial", 15, "bold")
        ).pack(anchor="w", pady=5)

        tk.Button(
            win,
            text="Proceed to Checkout →",
            command=lambda: self.checkout(win),
            bg=ORANGE,
            fg=WHITE,
            font=("Arial", 11, "bold"),
            relief="flat",
            pady=12
        ).pack(fill="x", padx=20, pady=15)

    def change_quantity(self, food_id, change, win):

        self.cart[food_id] = self.cart.get(food_id, 0) + change

        if self.cart[food_id] <= 0:
            self.cart.pop(food_id, None)

        self.update_cart_button()
        win.destroy()
        self.open_cart()
        self.display_foods()

    # -------------------- CHECKOUT --------------------

    def checkout(self, cart_window):

        if not self.cart:
            messagebox.showwarning(
                "Empty Cart",
                "Please add food to your cart first."
            )
            return

        win = tk.Toplevel(self.root)
        win.title("Checkout")
        win.geometry("480x580")
        win.configure(bg=BG)

        tk.Label(
            win,
            text="Checkout",
            font=("Arial", 22, "bold"),
            bg=BG
        ).pack(anchor="w", padx=25, pady=20)

        fields = {}

        for label, placeholder in [
            ("Name", "Enter your name"),
            ("Mobile", "10-digit mobile number"),
            ("Address", "Enter delivery address")
        ]:

            tk.Label(
                win,
                text=label,
                font=("Arial", 10, "bold"),
                bg=BG
            ).pack(anchor="w", padx=25, pady=(8, 4))

            entry = tk.Entry(
                win,
                font=("Arial", 11),
                relief="flat"
            )
            entry.pack(fill="x", padx=25, ipady=9)
            entry.insert(0, placeholder)

            entry.bind(
                "<FocusIn>",
                lambda event, p=placeholder:
                    event.widget.delete(0, "end")
                    if event.widget.get() == p else None
            )

            fields[label] = entry

        tk.Label(
            win,
            text="Payment method",
            font=("Arial", 10, "bold"),
            bg=BG
        ).pack(anchor="w", padx=25, pady=(12, 4))

        payment = tk.StringVar(value="Cash on delivery")

        ttk.Combobox(
            win,
            textvariable=payment,
            values=[
                "Cash on delivery",
                "UPI demo",
                "Card demo"
            ],
            state="readonly"
        ).pack(fill="x", padx=25, ipady=5)

        _, _, total = self.calculate_total()

        tk.Label(
            win,
            text=f"Order total: ₹{total}",
            font=("Arial", 16, "bold"),
            fg=ORANGE,
            bg=BG
        ).pack(anchor="w", padx=25, pady=20)

        def place_order():

            name = fields["Name"].get().strip()
            mobile = fields["Mobile"].get().strip()
            address = fields["Address"].get().strip()

            if (
                not name
                or name == "Enter your name"
                or not mobile.isdigit()
                or len(mobile) != 10
                or not address
                or address == "Enter delivery address"
            ):
                messagebox.showwarning(
                    "Invalid Details",
                    "Enter your name, a valid 10-digit mobile number, and address.",
                    parent=win
                )
                return

            _, _, total_amount = self.calculate_total()

            order = {
                "id": f"QB{random.randint(100000, 999999)}",
                "name": name,
                "mobile": mobile,
                "address": address,
                "payment": payment.get(),
                "total": total_amount,
                "created": datetime.now().strftime("%d %b %Y, %I:%M %p"),
                "items": [
                    (
                        next(f["name"] for f in foods if f["id"] == fid),
                        qty
                    )
                    for fid, qty in self.cart.items()
                ],
                "step": 0,
                "steps": [
                    "Order placed",
                    "Restaurant confirmed",
                    "Preparing your food",
                    "Picked up by delivery partner",
                    "Delivered"
                ]
            }

            self.orders.insert(0, order)
            self.active_order = order
            self.cart.clear()
            self.update_cart_button()
            self.display_foods()

            cart_window.destroy()
            win.destroy()

            self.open_tracking(order)

        tk.Button(
            win,
            text="Place Order ✓",
            command=place_order,
            bg=ORANGE,
            fg=WHITE,
            font=("Arial", 11, "bold"),
            relief="flat",
            pady=12
        ).pack(fill="x", padx=25, pady=10)

    # -------------------- ORDER TRACKING --------------------

    def open_tracking(self, order):

        win = tk.Toplevel(self.root)
        win.title("Track Your Order")
        win.geometry("600x620")
        win.configure(bg=BG)

        tk.Label(
            win,
            text="Track Your Order 📍",
            font=("Arial", 22, "bold"),
            bg=BG
        ).pack(anchor="w", padx=24, pady=(20, 5))

        tk.Label(
            win,
            text=f"Order ID: {order['id']}",
            font=("Arial", 10),
            bg=BG,
            fg="#777777"
        ).pack(anchor="w", padx=24)

        hero = tk.Frame(
            win,
            bg="#321B12",
            padx=20,
            pady=18
        )
        hero.pack(fill="x", padx=22, pady=18)

        tk.Label(
            hero,
            text="Estimated delivery",
            font=("Arial", 10),
            bg="#321B12",
            fg="#FFD3A8"
        ).pack(anchor="w")

        tk.Label(
            hero,
            text="25–35 minutes",
            font=("Arial", 24, "bold"),
            bg="#321B12",
            fg=WHITE
        ).pack(anchor="w", pady=3)

        tk.Label(
            hero,
            text=f"Delivering to: {order['address']}",
            font=("Arial", 9),
            bg="#321B12",
            fg=WHITE,
            wraplength=520
        ).pack(anchor="w")

        status_box = tk.Frame(
            win,
            bg=WHITE,
            padx=20,
            pady=18
        )
        status_box.pack(fill="x", padx=22)

        tk.Label(
            status_box,
            text="ORDER STATUS",
            font=("Arial", 10, "bold"),
            bg=WHITE,
            fg=ORANGE
        ).pack(anchor="w", pady=(0, 12))

        progress = ttk.Progressbar(
            status_box,
            maximum=4,
            value=order["step"],
            length=500
        )
        progress.pack(fill="x", pady=(0, 12))

        status_labels = []

        for index, step in enumerate(order["steps"]):

            row = tk.Frame(status_box, bg=WHITE)
            row.pack(fill="x", pady=5)

            icon = tk.Label(
                row,
                text="✓" if index <= order["step"] else "○",
                font=("Arial", 13, "bold"),
                bg=WHITE,
                fg=GREEN if index <= order["step"] else "#AAAAAA",
                width=3
            )
            icon.pack(side="left")

            label = tk.Label(
                row,
                text=step,
                font=("Arial", 10),
                bg=WHITE,
                fg=DARK if index <= order["step"] else "#999999"
            )
            label.pack(side="left")

            status_labels.append((icon, label))

        tk.Label(
            win,
            text="Demo tracking updates every 5 seconds.",
            font=("Arial", 9),
            bg=BG,
            fg="#777777"
        ).pack(anchor="w", padx=24, pady=12)

        def advance_status():

            if not win.winfo_exists():
                return

            if order["step"] >= len(order["steps"]) - 1:
                return

            order["step"] += 1
            progress.configure(value=order["step"])

            for index, (icon, label) in enumerate(status_labels):

                if index <= order["step"]:
                    icon.configure(text="✓", fg=GREEN)
                    label.configure(fg=DARK)
                else:
                    icon.configure(text="○", fg="#AAAAAA")
                    label.configure(fg="#999999")

            if order["step"] == len(order["steps"]) - 1:
                messagebox.showinfo(
                    "Order Delivered",
                    "Your demo order has been delivered!",
                    parent=win
                )
            else:
                win.after(5000, advance_status)

        if order["step"] < len(order["steps"]) - 1:
            win.after(5000, advance_status)

    # -------------------- ORDER HISTORY --------------------

    def show_history(self):

        win = tk.Toplevel(self.root)
        win.title("Order History")
        win.geometry("600x500")
        win.configure(bg=BG)

        tk.Label(
            win,
            text="Order History",
            font=("Arial", 22, "bold"),
            bg=BG
        ).pack(anchor="w", padx=20, pady=20)

        if not self.orders:
            tk.Label(
                win,
                text="No orders yet. Place your first order!",
                font=("Arial", 12),
                bg=BG
            ).pack(pady=30)
            return

        for order in self.orders:

            row = tk.Frame(
                win,
                bg=WHITE,
                padx=14,
                pady=12
            )
            row.pack(fill="x", padx=20, pady=6)

            tk.Label(
                row,
                text=f"{order['id']}  •  ₹{order['total']}",
                font=("Arial", 11, "bold"),
                bg=WHITE
            ).pack(anchor="w")

            tk.Label(
                row,
                text=f"{order['created']}  |  {order['steps'][order['step']]}",
                font=("Arial", 9),
                bg=WHITE,
                fg="#777777"
            ).pack(anchor="w", pady=4)

            tk.Button(
                row,
                text="Track order",
                command=lambda o=order: self.open_tracking(o),
                bg=ORANGE,
                fg=WHITE,
                relief="flat",
                padx=12,
                pady=5
            ).pack(anchor="e")

    # -------------------- FOOTER / STATUS --------------------

    def create_footer(self):

        footer = tk.Frame(self.root, bg="#FFF0E2")
        footer.pack(fill="x", side="bottom")

        self.status = tk.Label(
            footer,
            text="Made with ♥ for food lovers • Demo application",
            font=("Arial", 9),
            bg="#FFF0E2",
            fg="#8A4B22",
            anchor="w",
            padx=20,
            pady=7
        )
        self.status.pack(side="left", fill="x", expand=True)

        tk.Button(
            footer,
            text="Order History",
            command=self.show_history,
            bg="#FFF0E2",
            fg=DARK,
            relief="flat"
        ).pack(side="right", padx=15)

    def set_status(self, message):
        self.status.configure(text=message)


# -------------------- RUN APP --------------------

if __name__ == "__main__":
    root = tk.Tk()
    app = QuickBite(root)
    root.mainloop()
# '''
# main_path = os.path.join(base, "main.py")
# with open(main_path, "w", encoding="utf-8") as f:
#     f.write(code)

# readme = """QuickBite Python Food Ordering Desktop App
# ===========================================
# Requirements: Python 3.10+, Pillow
# Install: pip install pillow
# Run: python main.py

# Features:
# - Search and food categories
# - Food cards and hover effects
# - Favorites
# - Cart and quantity controls
# - Checkout form
# - Simulated order tracking
# - Order history

# Food photos are downloaded on first run if internet is available.
# This is a learning demo: it does not process real payments or provide live delivery data.
# """
# with open(os.path.join(base, "README.txt"), "w", encoding="utf-8") as f:
#     f.write(readme)

# zip_path = "/mnt/data/QuickBite_Python_Project.zip"
# with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
#     z.write(main_path, arcname="QuickBite/main.py")
#     z.write(os.path.join(base, "README.txt"), arcname="QuickBite/README.txt")

# # Basic syntax validation before providing the project.
# compile(code, main_path, "exec")
# print("Project created and syntax-checked successfully.")
# print(f"Python source: {main_path}")
# print(f"Project ZIP: {zip_path}")
# print(f"Source lines: {len(code.splitlines())}")
# print("Note: Tkinter app requires a desktop Python environment to run.")