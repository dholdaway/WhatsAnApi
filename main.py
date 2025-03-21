from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional, Dict

app = FastAPI()

# 🔓 Allow frontend access (adjust origins in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to specific domain in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🌐 Serve HTML/CSS/JS from static/
app.mount("/static", StaticFiles(directory="static"), name="static")

# ☕ Menu & Order Data (in-memory)
menu: Dict[str, Dict[str, Dict[str, float]]] = {
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
orders: Dict[int, Dict] = {}
valid_sizes = {"small", "medium", "large"}

# 🧾 Data Models
class Order(BaseModel):
    name: str
    drink: str
    size: str

class UpdateOrder(BaseModel):
    drink: Optional[str] = None
    size: Optional[str] = None

# 🏠 Serve Frontend
@app.get("/", include_in_schema=False)
async def serve_home():
    return FileResponse("static/index.html")

# 📋 Get Menu
@app.get("/menu")
def get_menu():
    return JSONResponse(content=menu)

# 🛒 Place Order
@app.post("/order")
def place_order(order: Order):
    size = order.size.lower()
    drink = order.drink

    category = next((cat for cat in menu if drink in menu[cat]), None)
    if not category:
        raise HTTPException(status_code=400, detail=f"Drink '{drink}' not found in menu")
    if size not in valid_sizes:
        raise HTTPException(status_code=400, detail=f"Invalid size '{size}'")

    order_id = len(orders) + 1
    price = menu[category][drink][size]

    orders[order_id] = {
        "name": order.name,
        "drink": drink,
        "size": size,
        "price": price
    }

    return {
        "message": "Order placed",
        "order_id": order_id,
        "details": orders[order_id]
    }

# 📜 View Orders
@app.get("/orders")
def list_orders():
    return orders

# ✏️ Update Order
@app.put("/order/{order_id}")
def update_order(order_id: int, update: UpdateOrder):
    if order_id not in orders:
        raise HTTPException(status_code=404, detail="Order not found")

    current = orders[order_id]

    if update.drink:
        category = next((cat for cat in menu if update.drink in menu[cat]), None)
        if not category:
            raise HTTPException(status_code=400, detail=f"Invalid drink '{update.drink}'")
        current["drink"] = update.drink
        current["price"] = menu[category][update.drink][current["size"]]

    if update.size:
        size = update.size.lower()
        if size not in valid_sizes:
            raise HTTPException(status_code=400, detail=f"Invalid size '{size}'")
        current["size"] = size
        category = next((cat for cat in menu if current["drink"] in menu[cat]), None)
        current["price"] = menu[category][current["drink"]][size]

    return {
        "message": "Order updated",
        "order_id": order_id,
        "details": current
    }

# ❌ Cancel Order
@app.delete("/order/{order_id}")
def cancel_order(order_id: int):
    if order_id not in orders:
        raise HTTPException(status_code=404, detail="Order not found")

    del orders[order_id]
    return {"message": "Order cancelled", "order_id": order_id}
