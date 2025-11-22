from ibm_watsonx_orchestrate.agent_builder.tools import tool
import pandas as pd
import os

@tool(
    description="Analyzes transport and supplier CSV data to find cheapest options with detailed reasoning"
)
def find_cheapest_transport(product_name: str) -> dict:
    """
    Analyzes transport/supplier data and returns cheapest option with detailed explanation.
    
    Returns:
        dict: Contains 'supplier', 'transport', 'cost', and 'explanation' fields
    """
    # Get path to CSV files relative to this tool file
    base_path = os.path.dirname(os.path.abspath(__file__))
    transport_csv_path = os.path.join(base_path, 'data', 'transport_data.csv')
    supplier_csv_path = os.path.join(base_path, 'data', 'supplier_data.csv')
    
    # Read CSV files
    transport_df = pd.read_csv(transport_csv_path)
    supplier_df = pd.read_csv(supplier_csv_path)
    
    # Filter suppliers for this product
    product_suppliers = supplier_df[supplier_df['product_name'] == product_name].copy()
    
    if product_suppliers.empty:
        return {
            "error": f"No suppliers found for product: {product_name}",
            "supplier": None,
            "transport": None,
            "total_cost": 0,
            "explanation": f"Product '{product_name}' not found in supplier database."
        }
    
    # Merge with transport options
    options = product_suppliers.merge(transport_df, on='supplier_id')
    options['total_cost'] = options['unit_price'] + options['shipping_cost']
    
    # Find cheapest option
    cheapest = options.loc[options['total_cost'].idxmin()]
    
    # Build detailed explanation
    explanation = f"""
**Decision Rationale for {product_name}:**
- Selected Supplier: {cheapest['supplier_name']} (${cheapest['unit_price']:.2f}/unit)
- Chose Transport: {cheapest['transport_method']}
  * Shipping cost: ${cheapest['shipping_cost']:.2f}
  * Delivery time: {cheapest['delivery_days']} days
  * Reliability: {cheapest['reliability_score']}%
- Total cost: ${cheapest['total_cost']:.2f}
- Compared {len(options)} alternatives
    """
    
    # Use a numeric scalar for total_cost to avoid pandas Series -> float typing issues
    total_cost = float(options['total_cost'].min())

    result = {
        "supplier": str(cheapest['supplier_name']),
        "transport": str(cheapest['transport_method']),
        "total_cost": total_cost,
        "explanation": explanation
    }
    
    return result