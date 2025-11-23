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
    data_dir = os.path.join(base_path, 'data')
    transport_csv_path = os.path.join(data_dir, 'simulated_transport.csv')
    supplier_csv_path = os.path.join(data_dir, 'simulated_suppliers.csv')
    
    # Ensure data directory exists
    os.makedirs(data_dir, exist_ok=True)
    
    # Check if files exist
    if not os.path.exists(transport_csv_path):
        return {
            "error": f"Transport CSV file not found: {transport_csv_path}",
            "supplier": None,
            "transport": None,
            "total_cost": 0,
            "explanation": f"Transport data file missing at {transport_csv_path}"
        }
    
    if not os.path.exists(supplier_csv_path):
        return {
            "error": f"Supplier CSV file not found: {supplier_csv_path}",
            "supplier": None,
            "transport": None,
            "total_cost": 0,
            "explanation": f"Supplier data file missing at {supplier_csv_path}"
        }
    
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
    options = product_suppliers.merge(transport_df, on='supplier_id', suffixes=('_supplier', '_transport'))
    
    # Calculate total cost: supplier cost per unit + transport cost per unit + fixed cost
    # Note: fixed_cost is a one-time shipping cost, so we include it in total
    options['total_cost'] = options['cost_per_unit_supplier'] + options['cost_per_unit_transport'] + options['fixed_cost']
    
    # Find cheapest option
    cheapest = options.loc[options['total_cost'].idxmin()]
    
    # Build detailed explanation
    explanation = f"""
**Decision Rationale for {product_name}:**
- Selected Supplier: {cheapest['supplier']} (${cheapest['cost_per_unit_supplier']:.2f}/unit)
- Chose Transport: {cheapest['transport_method']}
  * Transport cost per unit: ${cheapest['cost_per_unit_transport']:.2f}
  * Fixed shipping cost: ${cheapest['fixed_cost']:.2f}
- Total cost: ${cheapest['total_cost']:.2f}
- Compared {len(options)} alternatives
    """
    
    # Use a numeric scalar for total_cost to avoid pandas Series -> float typing issues
    total_cost = float(options['total_cost'].min())

    result = {
        "supplier": str(cheapest['supplier']),
        "transport": str(cheapest['transport_method']),
        "total_cost": total_cost,
        "explanation": explanation
    }
    
    return result