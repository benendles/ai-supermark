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
    csv_path = os.path.join(base_path, 'data', 'product.csv')
    
    # Read the CSV file
    df = pd.read_csv(csv_path)
    
    # Group by category and get top 5 by sales
    top_sales = df.groupby('category').apply(
        lambda x: x.nlargest(5, 'sales')
    ).reset_index(drop=True)
    
    # Convert to dictionary format
    result = {
        'top_sales_by_category': top_sales.to_dict('records'),
        'count': len(top_sales)
    }
    
    return result