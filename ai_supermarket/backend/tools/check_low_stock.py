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
    # Get path to CSV file relative to this tool file
    base_path = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(base_path, 'data', 'product.csv')
    
    # Read the CSV file
    df = pd.read_csv(csv_path)
    
    # Filter products below threshold
    low_stock_products = df[df['stock'] < threshold]
    
    # Convert to dictionary format
    result = {
        'low_stock_products': low_stock_products.to_dict('records'),
        'threshold': threshold,
        'count': len(low_stock_products)
    }
    
    return result