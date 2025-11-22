from ibm_watsonx_orchestrate.agent_builder.tools import tool
import pandas as pd
import os

@tool(
    description="Gets bottom 3 selling products per category per month"
)
def get_lowest_sales() -> dict:
    """Retrieves lowest sales data from CSV file."""
    
    # Get the path to the CSV file relative to this tool file
    base_path = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(base_path, 'data', 'product.csv')
    
    # Read the CSV file
    df = pd.read_csv(csv_path)
    
    # Process your data here (example logic)
    # Group by category and get bottom 3 by sales
    result = df.groupby('category').apply(
        lambda x: x.nsmallest(3, 'sales')
    ).to_dict('records')
    
    return {'lowest_sales': result}