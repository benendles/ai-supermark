from ibm_watsonx_orchestrate.agent_builder.tools import tool
import pandas as pd
import os

@tool(
    description="Gets bottom 5 selling products per category per month from sales data"
)
def get_lowest_sales() -> dict:
    """Retrieves lowest sales data from CSV file."""
    
    base_path = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_path, 'data')
    csv_path = os.path.join(data_dir, 'sales.csv')
    
    # Ensure data directory exists
    os.makedirs(data_dir, exist_ok=True)
    
    # Check if file exists
    if not os.path.exists(csv_path):
        return {
            'message': f'Sales CSV file not found: {csv_path}',
            'lowest_sales': [],
            'error': f'Sales file missing at {csv_path}'
        }
    
    df = pd.read_csv(csv_path)
    
    # Count sales per product and category
    sales_summary = df.groupby(['product_id', 'product_name', 'category']).agg(
        sales_count=('sale_id', 'count'),
        total_revenue=('price', 'sum')
    ).reset_index()
    
    # Group by category and get bottom 5 by sales count
    lowest_sales = sales_summary.groupby('category').apply(
        lambda x: x.nsmallest(5, 'sales_count')
    ).reset_index(drop=True)
    
    # Limit to first 20 products for processing
    total_count = len(lowest_sales)
    lowest_sales = lowest_sales.head(20)
    
    result = {
        'message': f'Found {total_count} products with lowest sales across all categories. Processing first 20 products.',
        'lowest_sales': lowest_sales.to_dict('records'),
        'total_found': total_count
    }
    
    return result