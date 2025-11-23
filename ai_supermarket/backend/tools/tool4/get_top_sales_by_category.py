from ibm_watsonx_orchestrate.agent_builder.tools import tool
import pandas as pd
import os

@tool(
    description="Gets top 5 selling products per category per month from supermarket database"
)
def get_top_sales_by_category() -> dict:
    """Retrieves highest sales data from CSV file."""
    
    # Get path to CSV file relative to this tool file
    base_path = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_path, 'data')
    csv_path = os.path.join(data_dir, 'sales.csv')
    
    # Ensure data directory exists
    os.makedirs(data_dir, exist_ok=True)
    
    # Check if file exists
    if not os.path.exists(csv_path):
        return {
            'message': f'Sales CSV file not found: {csv_path}',
            'top_sales_by_category': [],
            'count': 0,
            'error': f'Sales file missing at {csv_path}'
        }
    
    # Read the CSV file
    df = pd.read_csv(csv_path)
    
    # Count sales per product and category
    sales_summary = df.groupby(['product_id', 'product_name', 'category']).agg(
        sales_count=('sale_id', 'count'),
        total_revenue=('price', 'sum')
    ).reset_index()
    
    # Group by category and get top 5 by sales count
    top_sales = sales_summary.groupby('category').apply(
        lambda x: x.nlargest(5, 'sales_count')
    ).reset_index(drop=True)
    
    # Limit to first 20 products for processing
    total_count = len(top_sales)
    top_sales = top_sales.head(20)
    
    # Convert to dictionary format
    result = {
        'message': f'Found top {total_count} selling products across all categories. Processing first 20 products.',
        'top_sales_by_category': top_sales.to_dict('records'),
        'count': len(top_sales),
        'total_found': total_count
    }
    
    return result