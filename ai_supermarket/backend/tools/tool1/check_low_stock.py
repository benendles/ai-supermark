from ibm_watsonx_orchestrate.agent_builder.tools import tool
import pandas as pd
import os

@tool(
    description="Checks products with stock below reorder threshold and returns products needing reorder"
)
def check_low_stock(threshold: int = 50) -> dict:
    """
    Checks inventory for products below stock threshold.
    
    Args:
        threshold: Minimum stock level (default: 50)
    
    Returns:
        List of products needing reorder with their details
    """
    # Get path relative to this Python file
    base_path = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_path, 'data')
    csv_path = os.path.join(data_dir, 'products.csv')
    
    # Ensure data directory exists
    os.makedirs(data_dir, exist_ok=True)
    
    # Check if file exists
    if not os.path.exists(csv_path):
        return {
            'message': f'Products CSV file not found: {csv_path}',
            'low_stock_products': [],
            'threshold': threshold,
            'count': 0,
            'error': f'Products file missing at {csv_path}'
        }
    
    # Read the CSV file
    df = pd.read_csv(csv_path)
    
    # Use whichever column exists
    stock_col = 'stock_level' if 'stock_level' in df.columns else 'stock'
    
    # Filter products below threshold
    low_stock_products = df[df[stock_col] < threshold]
    
    # Limit to first 20 products for processing
    total_count = len(low_stock_products)
    low_stock_products = low_stock_products.head(5)
    
    # Convert to dictionary format
    result = {
        'message': f'Found {total_count} products below threshold of {threshold}. Processing first 20 products.',
        'low_stock_products': low_stock_products.to_dict('records'),
        'threshold': threshold,
        'count': len(low_stock_products),
        'total_found': total_count
    }
    
    return result