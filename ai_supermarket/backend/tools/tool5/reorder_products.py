from ibm_watsonx_orchestrate.agent_builder.tools import tool
import pandas as pd
import os
from typing import List
from datetime import datetime

@tool(
    description="Creates reorder requests using cheapest supplier and transport"
)
def reorder_products(product_ids: List[str], quantities: List[int], expected_delivery: str) -> dict:
    """
    Reorders products after finding cheapest supplier and transport for each.
    """
    # Self-contained function to simulate finding cheapest transport
    def find_cheapest_transport(product_id: str) -> dict:
        # Simulated logic — replace with real logic if needed
        return {
            "supplier": "Supplier A",
            "transport": "Truck",
            "total_cost": round(20 + hash(product_id) % 50, 2)  # random-ish cost
        }

    # Get path to CSV files relative to this tool file
    base_path = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(base_path, 'data', 'products.csv')
    orders_csv_path = os.path.join(base_path, 'data', 'orders.csv')
    
    # Read the product CSV file
    df = pd.read_csv(csv_path)
    
    # Ensure column consistency
    df.columns = df.columns.str.strip()
    if 'stock_level' in df.columns:
        df.rename(columns={'stock_level': 'stock'}, inplace=True)
    elif 'stock' not in df.columns:
        df['stock'] = 0  # create stock column if missing
    
    orders = []
    for product_id, quantity in zip(product_ids, quantities):
        # Call internal transport function
        transport_result = find_cheapest_transport(product_id)
        
        # Get current stock
        current_stock_row = df[df['product_id'] == int(product_id)]
        current_stock = int(current_stock_row['stock'].iloc[0]) if not current_stock_row.empty else 0
        
        # Create order record
        order = {
            "product_id": product_id,
            "quantity": quantity,
            "expected_delivery": expected_delivery,
            "supplier": transport_result["supplier"],
            "transport_method": transport_result["transport"],
            "cost": transport_result["total_cost"],
            "order_date": datetime.now().strftime("%Y-%m-%d"),
            "status": "pending"
        }
        orders.append(order)
        
        # Update stock in product CSV (add quantity to current stock)
        if not current_stock_row.empty:
            df.loc[df['product_id'] == int(product_id), 'stock'] += quantity
        else:
            # If product not in CSV, create new row
            new_row = {
                "product_id": int(product_id),
                "product_name": f"Product {product_id}",
                "category": "Unknown",
                "price": 0.0,
                "stock": quantity,
                "purchased_date": ""
            }
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    
    # Save updated product inventory
    df.to_csv(csv_path, index=False)
    
    # Append orders to orders CSV
    orders_df = pd.DataFrame(orders)
    if os.path.exists(orders_csv_path):
        existing_orders = pd.read_csv(orders_csv_path)
        orders_df = pd.concat([existing_orders, orders_df], ignore_index=True)
    orders_df.to_csv(orders_csv_path, index=False)
    
    return {"success": True, "orders": orders}