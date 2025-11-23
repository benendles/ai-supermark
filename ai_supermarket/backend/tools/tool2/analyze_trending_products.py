from ibm_watsonx_orchestrate.agent_builder.tools import tool
import pandas as pd
import os
from typing import Dict

@tool(
    description="Analyzes Christmas sales CSV, compares with backend inventory, and identifies products to reorder with business justification"
)
def analyze_simulated_sales() -> Dict:
    """
    Loads CSV, compares with inventory.
    Returns matching products with detailed business reasoning for reorder recommendations.
    """
    # Get path to CSV files relative to this tool file
    base_path = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_path, 'data')
    sales_csv_path = os.path.join(data_dir, 'simulated_christmas_sales_top5000.csv')
    inventory_csv_path = os.path.join(data_dir, 'products.csv')
    
    # Ensure data directory exists
    os.makedirs(data_dir, exist_ok=True)
    
    # Check if files exist
    if not os.path.exists(sales_csv_path):
        return {
            'products_to_reorder': [],
            'new_product_suggestions': [],
            'error': f'Christmas sales CSV file not found: {sales_csv_path}'
        }
    
    if not os.path.exists(inventory_csv_path):
        return {
            'products_to_reorder': [],
            'new_product_suggestions': [],
            'error': f'Inventory CSV file not found: {inventory_csv_path}'
        }
    
    # Read CSV files
    df_sales = pd.read_csv(sales_csv_path)
    df_inventory = pd.read_csv(inventory_csv_path)
    
    # Calculate detailed sales metrics
    sales_analysis = df_sales.groupby('product_name').agg({
        'units_sold': ['sum', 'mean', 'count'],
        'revenue': 'sum'
    }).reset_index()
    sales_analysis.columns = ['product_name', 'total_units', 'avg_daily_sales', 'days_sold', 'total_revenue']
    
    # Compare with inventory
    products_to_reorder = []
    new_product_suggestions = []
    
    for _, sales_row in sales_analysis.iterrows():
        product_name = sales_row['product_name']
        total_units = sales_row['total_units']
        
        # Check if product exists in inventory (case-insensitive comparison)
        inventory_match = df_inventory[df_inventory['product_name'].str.strip().str.lower() == product_name.strip().lower()]
        
        if not inventory_match.empty:
            # Product exists in inventory
            if total_units > 100:
                # Handle both 'stock' and 'stock_level' column names
                stock_col = 'stock_level' if 'stock_level' in inventory_match.columns else 'stock'
                current_stock = inventory_match.iloc[0][stock_col]
                product_id = inventory_match.iloc[0]['product_id']
                
                products_to_reorder.append({
                    'product_id': product_id,
                    'product_name': product_name,
                    'current_stock': current_stock,
                    'recommended_quantity': int(total_units * 0.5),  # Recommend 50% of simulated sales
                    'business_justification': f"""
**Reorder Recommendation for {product_name}:**
- Sales Performance: Sold {int(sales_row['total_units'])} units generating ${sales_row['total_revenue']:,.2f} in revenue
- Demand Pattern: Average {sales_row['avg_daily_sales']:.1f} units/day over {int(sales_row['days_sold'])} days
- Current Stock Status: {current_stock} units remaining
- Risk Assessment: High demand product with potential stockout risk
- Business Impact: Restocking prevents lost sales and maintains customer satisfaction
- Recommended Action: Immediate reorder of {int(total_units * 0.5)} units
                    """
                })
        else:
            # Product doesn't exist in inventory
            if total_units > 50:
                new_product_suggestions.append({
                    'product_name': product_name,
                    'simulated_units_sold': int(total_units),
                    'avg_daily_sales': sales_row['avg_daily_sales'],
                    'recommended_initial_order': int(total_units * 0.3)
                })
    
    # Limit to first 20 products for each category
    total_to_reorder = len(products_to_reorder)
    total_suggestions = len(new_product_suggestions)
    products_to_reorder = products_to_reorder[:5]
    new_product_suggestions = new_product_suggestions[:5]
    
    return {
        'products_to_reorder': products_to_reorder,
        'new_product_suggestions': new_product_suggestions,
        'total_to_reorder_found': total_to_reorder,
        'total_suggestions_found': total_suggestions,
        'message': f'Found {total_to_reorder} products to reorder and {total_suggestions} suggestions. Processing first 20 of each.'
    }