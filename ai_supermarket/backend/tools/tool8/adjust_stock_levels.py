from ibm_watsonx_orchestrate.agent_builder.tools import tool
import pandas as pd
import os
from typing import List, Dict

@tool(
    description="Adjusts stock levels for products - increases stock for top sellers and decreases for low sellers"
)
def adjust_stock_levels(adjustments: List[Dict]) -> dict:
    """
    Adjusts stock levels for products based on sales performance.
    
    Args:
        adjustments: List of dictionaries with keys: product_id (str), adjustment_type (str: 'increase' or 'decrease'), quantity (int), reason (str)
    
    Returns:
        dict: Summary of stock adjustments made with adjusted_products and failed_adjustments
    """
    base_path = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_path, 'data')
    products_csv_path = os.path.join(data_dir, 'products.csv')
    
    # Ensure data directory exists
    os.makedirs(data_dir, exist_ok=True)
    
    # Check if file exists
    if not os.path.exists(products_csv_path):
        return {
            'success': False,
            'message': f'Products CSV file not found: {products_csv_path}',
            'adjusted_products': [],
            'failed_adjustments': [{'error': f'Products file missing at {products_csv_path}'}],
            'total_adjusted': 0
        }
    
    # Read products CSV
    df = pd.read_csv(products_csv_path)
    
    # Ensure stock column exists
    stock_col = 'stock_level' if 'stock_level' in df.columns else 'stock'
    if stock_col not in df.columns:
        df['stock'] = 0
        stock_col = 'stock'
    
    # Track adjustments
    adjusted_products = []
    failed_adjustments = []
    
    for adjustment in adjustments:
        product_id = adjustment.get('product_id')
        adjustment_type = adjustment.get('adjustment_type', 'increase')
        quantity = abs(adjustment.get('quantity', 0))
        reason = adjustment.get('reason', '')
        
        # Find product in dataframe
        product_row = df[df['product_id'] == int(product_id)]
        
        if not product_row.empty:
            idx = product_row.index[0]
            current_stock = int(df.loc[idx, stock_col])
            
            # Apply adjustment
            if adjustment_type == 'increase':
                new_stock = current_stock + quantity
            elif adjustment_type == 'decrease':
                new_stock = max(0, current_stock - quantity)  # Don't go below 0
            else:
                failed_adjustments.append({
                    'product_id': product_id,
                    'error': f'Invalid adjustment_type: {adjustment_type}'
                })
                continue
            
            # Update stock
            df.loc[idx, stock_col] = new_stock
            
            adjusted_products.append({
                'product_id': product_id,
                'product_name': df.loc[idx, 'product_name'] if 'product_name' in df.columns else 'Unknown',
                'old_stock': current_stock,
                'new_stock': new_stock,
                'adjustment': f'+{quantity}' if adjustment_type == 'increase' else f'-{quantity}',
                'reason': reason
            })
        else:
            failed_adjustments.append({
                'product_id': product_id,
                'error': 'Product not found in inventory'
            })
    
    # Save updated products CSV
    df.to_csv(products_csv_path, index=False)
    
    return {
        'success': True,
        'message': f'Adjusted stock for {len(adjusted_products)} products',
        'adjusted_products': adjusted_products,
        'failed_adjustments': failed_adjustments,
        'total_adjusted': len(adjusted_products)
    }

