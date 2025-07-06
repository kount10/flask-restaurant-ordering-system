from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session management

# Sample menu (You can replace this with a dynamic database later)
menu = [
    {'id': 1, 'name': 'Clear Corn Soup', 'price': 110.0},
    {'id': 2, 'name': 'Chicken Soup', 'price': 140.0},
    {'id': 3, 'name': 'Tandoori Roti', 'price': 40.0},
    {'id': 4, 'name': 'Butter Naan', 'price': 50.0},
    {'id': 5, 'name': 'Garlic Naan', 'price': 60.0},
    {'id': 6, 'name': 'Aloo Gobi', 'price': 150.0},
    {'id': 7, 'name': 'Veg Biryani', 'price': 200.0},
    {'id': 8, 'name': 'Mixed Vegetable Curry', 'price': 220.0},
    {'id': 9, 'name': 'Paneer Butter Masala', 'price': 250.0},
    {'id': 10, 'name': 'Dal Tadka', 'price': 180.0},
    {'id': 11, 'name': 'Fish Fry', 'price': 280.0},
    {'id': 12, 'name': 'Mutton Biryani', 'price': 350.0},
    {'id': 13, 'name': 'Chicken Curry', 'price': 300.0},
    {'id': 14, 'name': 'Fresh Lime Soda', 'price': 90.0},
    {'id': 15, 'name': 'Masala Dosa', 'price': 120.0},
    {'id': 16, 'name': 'Gulab Jamun', 'price': 100.0},
    {'id': 17, 'name': 'Ice Cream', 'price': 120.0},
    {'id': 18, 'name': 'Chocolate Brownie', 'price': 150.0}
]

@app.route('/')
def index():
    return render_template('menu.html', menu=menu)

@app.route('/add_to_cart/<int:item_id>', methods=['POST'])
def add_to_cart(item_id):
    item = next((dish for dish in menu if dish['id'] == item_id), None)
    if item is None:
        return redirect(url_for('index'))

    quantity = int(request.form.get('quantity', 1))

    if 'cart' not in session:
        session['cart'] = []

    cart_item = next((cart for cart in session['cart'] if cart['id'] == item_id), None)
    if cart_item:
        cart_item['quantity'] += quantity
    else:
        session['cart'].append({'id': item_id, 'name': item['name'], 'price': item['price'], 'quantity': quantity})

    session.modified = True
    flash(f"{item['name']} x {quantity} has been added to your cart!")
    return redirect(url_for('index'))  # Stay on the menu page after adding

@app.route('/cart')
def cart():
    total = sum(item['price'] * item['quantity'] for item in session.get('cart', []))
    return render_template('cart.html', cart=session.get('cart', []), total=total)

@app.route('/remove_from_cart/<int:item_id>', methods=['POST'])
def remove_from_cart(item_id):
    session['cart'] = [item for item in session['cart'] if item['id'] != item_id]
    session.modified = True
    return redirect(url_for('cart'))

@app.route('/checkout')
def checkout():
    cart = session.get('cart', [])
    total = sum(item['price'] * item['quantity'] for item in cart)
    tax = total * 0.08  # 8% tax
    discount = total * 0.15  # 15% discount
    final_total = total + tax - discount
    return render_template('checkout.html', total=total, tax=tax, discount=discount, final_total=final_total)

if __name__ == '__main__':
    app.run(debug=True)
