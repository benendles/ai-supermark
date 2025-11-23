from ibm_watsonx_orchestrate.agent_builder.tools import tool
import pandas as pd
import os

@tool(
    description="Gets bottom 3 selling products per category per month"
)
def get_lowest_sales() -> dict:
    """Retrieves lowest sales data from CSV file."""
    
    base_path = os.path.dirname(os.path.abspath(__file__))
    # Build path relative to tool location - use sale.csv not sales.csv
    csv_path = os.path.join(base_path, 'data', 'sales.csv')
    df = pd.read_csv(csv_path)
    
    # Count sales per product and category
    sales_summary = df.groupby(['product_id', 'product_name', 'category']).agg(
        sales_count=('sale_id', 'count'),
        total_revenue=('price', 'sum')
    ).reset_index()
    
    # Group by category and get bottom 3 by sales count
    lowest_sales = sales_summary.groupby('category').apply(
        lambda x: x.nsmallest(3, 'sales_count')
    ).reset_index(drop=True)
    
    result = {
        'message': f'Found {len(lowest_sales)} products with lowest sales across all categories',
        'lowest_sales': lowest_sales.to_dict('records')
    }
    
    return result