# ☕ **Coffee Shop API** - Beginner's Guide to REST APIs  
This project is a simple **REST API** that simulates a **coffee shop ordering system**. It is designed to teach **non-technical users** how APIs work using easy-to-follow commands.

---

## 🚀 **Features**
- 📋 **View Menu** – See available drinks and sizes  
- ☕ **Place an Order** – Order a coffee with your name  
- 📜 **View Orders** – List all placed orders  
- ✏️ **Update an Order** – Modify your drink or size  
- ❌ **Cancel an Order** – Remove an order  

---

## 🔧 **Installation & Setup**
### 1️⃣ **Clone the Repository**
```bash
git clone https://github.com/YOUR_GITHUB_USERNAME/CoffeeShopAPI.git
cd CoffeeShopAPI
```

### 2️⃣ **Install Dependencies**
Ensure you have **Python 3+** installed, then install Flask:
```bash
pip install flask
```

### 3️⃣ **Run the API**
Start the Flask server:
```bash
python app.py
```
🚀 The API is now running at **http://127.0.0.1:5000**

---

## 📌 **API Endpoints & Usage**
### 📋 **1. View the Menu (GET)**
Retrieves all available drinks and sizes.  
```bash
curl -X GET http://127.0.0.1:5000/menu
```
✅ **Example Response:**
```json
{
  "coffee": {
    "Espresso": { "small": 2.50, "medium": 3.00, "large": 3.50 },
    "Latte": { "small": 3.50, "medium": 4.00, "large": 4.50 }
  },
  "tea": {
    "Green Tea": { "small": 2.00, "medium": 2.50, "large": 3.00 }
  }
}
```

---

### ☕ **2. Place an Order (POST)**
Submit an order by providing your **name, drink, and size**.  
```bash
curl -X POST http://127.0.0.1:5000/order \
     -H "Content-Type: application/json" \
     -d '{"name": "Alice", "drink": "Latte", "size": "medium"}'
```
✅ **Example Response:**
```json
{
  "message": "Order placed",
  "order_id": 1,
  "details": {
    "name": "Alice",
    "drink": "Latte",
    "size": "medium",
    "price": 4.00
  }
}
```

---

### 📜 **3. View All Orders (GET)**
Lists all orders placed by customers.  
```bash
curl -X GET http://127.0.0.1:5000/orders
```
✅ **Example Response:**
```json
{
  "1": { "name": "Alice", "drink": "Latte", "size": "medium", "price": 4.00 }
}
```

---

### ✏️ **4. Update an Order (PUT)**
Modify an existing order by changing the drink or size.  
```bash
curl -X PUT http://127.0.0.1:5000/order/1 \
     -H "Content-Type: application/json" \
     -d '{"drink": "Cappuccino", "size": "large"}'
```
✅ **Example Response:**
```json
{
  "message": "Order updated",
  "order_id": 1,
  "details": {
    "name": "Alice",
    "drink": "Cappuccino",
    "size": "large",
    "price": 4.50
  }
}
```

---

### ❌ **5. Cancel an Order (DELETE)**
Removes an order by **order ID**.  
```bash
curl -X DELETE http://127.0.0.1:5000/order/1
```
✅ **Example Response:**
```json
{
  "message": "Order cancelled",
  "order_id": 1
}
```

---

## 🎯 **Key Learning Points**
- APIs **allow applications to communicate**
- HTTP methods:
  - **GET** (Retrieve data)
  - **POST** (Create data)
  - **PUT** (Update data)
  - **DELETE** (Remove data)
- JSON **format is used** to exchange data between client and server

---

## 🛠️ **Troubleshooting**
| Issue | Solution |
|--------|---------|
| `ModuleNotFoundError: No module named 'flask'` | Run `pip install flask` |
| API not starting? | Ensure `app.py` is running: `python app.py` |
| `curl: command not found` | Install curl: `sudo apt install curl` or use Postman |

---

## 🎉 **Contributing**
- Feel free to submit **issues** or **pull requests**.
- Improve the project by adding **a frontend, authentication, or a leaderboard**.

---

## 🔗 **Resources**
📄 **[Download API Handout](sandbox:/mnt/data/Coffee_Shop_API_Handout.pdf)**  
📊 **[Download API Presentation](sandbox:/mnt/data/Coffee_Shop_API_Presentation.pptx)**  

---

🚀 **Enjoy learning APIs with the Coffee Shop Demo!** ☕🎉

---
