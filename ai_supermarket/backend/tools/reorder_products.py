from ibm_watsonx_orchestrate.agent_builder.tools import tool
import pandas as pd
import os
from typing import List
from datetime import datetime
from transport_analytics import find_cheapest_transport  # Import your transport tool

@tool(
    description="Creates reorder requests using cheapest supplier and transport"
)
def reorder_products(product_ids: List[str], quantities: List[int], expected_delivery: str) -> dict:
    """
    Reorders products after finding cheapest supplier and transport for each.
    """
    # Get path to CSV file relative to this tool file
    base_path = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(base_path, 'data', 'product.csv')
    orders_csv_path = os.path.join(base_path, 'data', 'orders.csv')
    
    # Read the product CSV file
    df = pd.read_csv(csv_path)
    
    orders = []
    for product_id, quantity in zip(product_ids, quantities):
        # Call transport tool
        transport_result = find_cheapest_transport(product_id)
        
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
        df.loc[df['product_id'] == product_id, 'stock'] += quantity
    
    # Save updated product inventory
    df.to_csv(csv_path, index=False)
    
    # Append orders to orders CSV
    orders_df = pd.DataFrame(orders)
    if os.path.exists(orders_csv_path):
        existing_orders = pd.read_csv(orders_csv_path)
        orders_df = pd.concat([existing_orders, orders_df], ignore_index=True)
    orders_df.to_csv(orders_csv_path, index=False)
    
    return {"success": True, "orders": orders}