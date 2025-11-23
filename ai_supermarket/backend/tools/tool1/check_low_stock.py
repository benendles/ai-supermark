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
    csv_path = os.path.join(base_path, 'data', 'products.csv')
    
    # Read the CSV file
    df = pd.read_csv(csv_path)
    
    # Use whichever column exists
    stock_col = 'stock_level' if 'stock_level' in df.columns else 'stock'
    
    # Filter products below threshold
    low_stock_products = df[df[stock_col] < threshold]
    
    # Convert to dictionary format
    result = {
        'message': f'Found {len(low_stock_products)} products below threshold of {threshold}',
        'low_stock_products': low_stock_products.to_dict('records'),
        'threshold': threshold,
        'count': len(low_stock_products)
    }
    
    return result