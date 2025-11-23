from ibm_watsonx_orchestrate.agent_builder.tools import tool
import pandas as pd
import os
from typing import List, Dict
from datetime import datetime

@tool(
    description="Sends product suggestions to the supply manager for products not in inventory but trending in Christmas sales"
)
def send_supply_manager_suggestion(suggestions: List[Dict]) -> dict:
    """
    Sends suggestions to supply manager for new products to consider adding to inventory.
    
    Args:
        suggestions: List of dictionaries with product_name, simulated_units_sold, 
                    avg_daily_sales, recommended_initial_order
    
    Returns:
        Confirmation message with details of suggestions sent
    """
    base_path = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_path, 'data')
    suggestions_csv_path = os.path.join(data_dir, 'supply_manager_suggestions.csv')
    
    # Ensure data directory exists
    os.makedirs(data_dir, exist_ok=True)
    
    # Prepare suggestions data
    suggestions_data = []
    for suggestion in suggestions:
        suggestion_record = {
            'product_name': suggestion.get('product_name', ''),
            'simulated_units_sold': suggestion.get('simulated_units_sold', 0),
            'avg_daily_sales': suggestion.get('avg_daily_sales', 0),
            'recommended_initial_order': suggestion.get('recommended_initial_order', 0),
            'suggestion_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'status': 'pending_review'
        }
        suggestions_data.append(suggestion_record)
    
    # Create DataFrame and save to CSV
    suggestions_df = pd.DataFrame(suggestions_data)
    
    # Append to existing suggestions file if it exists
    if os.path.exists(suggestions_csv_path):
        existing_suggestions = pd.read_csv(suggestions_csv_path)
        suggestions_df = pd.concat([existing_suggestions, suggestions_df], ignore_index=True)
    
    suggestions_df.to_csv(suggestions_csv_path, index=False)
    
    return {
        'success': True,
        'message': f'Sent {len(suggestions)} product suggestions to supply manager',
        'suggestions': suggestions_data,
        'file_path': suggestions_csv_path
    }

