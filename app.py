from flask import Flask, jsonify, request, send_from_directory

app = Flask(__name__, static_folder='static')

# Coffee shop menu with predefined drinks and sizes
menu = {
    "coffee": {
        "Espresso": {"small": 2.50, "medium": 3.00, "large": 3.50},
        "Latte": {"small": 3.50, "medium": 4.00, "large": 4.50},
        "Cappuccino": {"small": 3.00, "medium": 3.50, "large": 4.00},
        "Americano": {"small": 2.00, "medium": 2.50, "large": 3.00}
    },
    "tea": {
        "Green Tea": {"small": 2.00, "medium": 2.50, "large": 3.00},
        "Black Tea": {"small": 1.50, "medium": 2.00, "large": 2.50},
        "Chai": {"small": 2.50, "medium": 3.00, "large": 3.50}
    }
}

@app.route('/api-docs')
def serve_api_docs():
    return send_from_directory('static', 'api.html')

# Store orders in memory
orders = {}
valid_sizes = {"small", "medium", "large"}

@app.route('/')
def serve_index():
    return send_from_directory('static', 'index.html')

@app.route('/menu', methods=['GET'])
def get_menu():
    return jsonify(menu), 200

@app.route('/order', methods=['POST'])
def place_order():
    data = request.json

    # Validate request
    if "name" not in data or "drink" not in data or "size" not in data:
        return jsonify({"error": "Missing 'name', 'drink', or 'size'"}), 400

    drink_name = data["drink"]
    size = data["size"].lower()

    # Check if drink exists
    drink_category = next((cat for cat in menu if drink_name in menu[cat]), None)
    if not drink_category:
        return jsonify({"error": f"Invalid drink name: {drink_name}"}), 400

    # Check if size is valid
    if size not in valid_sizes:
        return jsonify({"error": f"Invalid size: {size}. Choose from {list(valid_sizes)}"}), 400

    # Generate order ID and store order
    order_id = len(orders) + 1
    price = menu[drink_category][drink_name][size]
    orders[order_id] = {"name": data["name"], "drink": drink_name, "size": size, "price": price}

    return jsonify({"message": "Order placed", "order_id": order_id, "details": orders[order_id]}), 201

@app.route('/orders', methods=['GET'])
def get_orders():
    return jsonify(orders), 200

@app.route('/order/<int:order_id>', methods=['PUT'])
def update_order(order_id):
    if order_id not in orders:
        return jsonify({"error": "Order not found"}), 404

    data = request.json
    if "drink" in data:
        drink_name = data["drink"]
        drink_category = next((cat for cat in menu if drink_name in menu[cat]), None)
        if not drink_category:
            return jsonify({"error": f"Invalid drink name: {drink_name}"}), 400
        orders[order_id]["drink"] = drink_name
        orders[order_id]["price"] = menu[drink_category][drink_name][orders[order_id]["size"]]

    if "size" in data:
        size = data["size"].lower()
        if size not in valid_sizes:
            return jsonify({"error": f"Invalid size: {size}. Choose from {list(valid_sizes)}"}), 400
        orders[order_id]["size"] = size
        drink_name = orders[order_id]["drink"]
        drink_category = next((cat for cat in menu if drink_name in menu[cat]), None)
        orders[order_id]["price"] = menu[drink_category][drink_name][size]

    return jsonify({"message": "Order updated", "order_id": order_id, "details": orders[order_id]}), 200

@app.route('/order/<int:order_id>', methods=['DELETE'])
def cancel_order(order_id):
    if order_id in orders:
        del orders[order_id]
        return jsonify({"message": "Order cancelled", "order_id": order_id}), 200
    return jsonify({"error": "Order not found"}), 404

# Run the Flask server
if __name__ == '__main__':
    app.run(debug=True)
