# Supermarket Inventory Management System with WatsonX Orchestra

This system provides comprehensive automated inventory management for supermarkets using IBM WatsonX Orchestra. It automatically checks for low stock, analyzes trending products, adjusts stock levels based on sales performance, and handles reordering.

## System Overview

The system consists of multiple agents and tools that work together to manage inventory:

### Main Orchestrator Agent
**`supply_manager_orchestrator_agent.yaml`** - The main agent that coordinates all inventory management tasks.

### Key Features

1. **Low Stock Detection & Auto-Reorder**
   - Automatically checks for products below threshold (default: 50 units)
   - Calculates optimal reorder quantities based on sales velocity
   - Places automatic reorders with 7-day delivery expectation

2. **Christmas Trending Products Analysis**
   - Analyzes Christmas sales CSV file (`simulated_christmas_sales_top5000.csv`)
   - Compares trending products with current inventory
   - **For products found in both files**: Increases stock and places reorders
   - **For products NOT in inventory**: Sends suggestions to supply manager

3. **Sales Performance Analysis by Category**
   - Analyzes top 5 selling products per category
   - Analyzes bottom 5 selling products per category
   - **Top 5**: Increases stock by 50%
   - **Bottom 5**: Decreases stock by 30% (minimum 10 units)

4. **Automatic Reordering**
   - After all adjustments, automatically reorders all products needing restocking
   - Finds cheapest supplier and transport options
   - Updates inventory and creates order records

## Tools Available

### Tool 1: `check_low_stock`
- **Location**: `backend/tools/tool1/check_low_stock.py`
- **Purpose**: Identifies products below reorder threshold
- **Data**: `data/products.csv`

### Tool 2: `analyze_simulated_sales` (analyze_trending_products)
- **Location**: `backend/tools/tool2/analyze_trending_products.py`
- **Purpose**: Analyzes Christmas CSV and compares with inventory
- **Data**: 
  - `data/simulated_christmas_sales_top5000.csv`
  - `data/products.csv`

### Tool 3: `get_lowest_sales`
- **Location**: `backend/tools/tool3/get_lowest_sales.py`
- **Purpose**: Gets bottom 5 selling products per category
- **Data**: `data/sales.csv`

### Tool 4: `get_top_sales_by_category`
- **Location**: `backend/tools/tool4/get_top_sales_by_category.py`
- **Purpose**: Gets top 5 selling products per category
- **Data**: `data/sales.csv`

### Tool 5: `reorder_products`
- **Location**: `backend/tools/tool5/reorder_products.py`
- **Purpose**: Creates reorder requests and updates inventory
- **Data**: 
  - `data/products.csv`
  - `data/orders.csv`

### Tool 6: `find_cheapest_transport`
- **Location**: `backend/tools/tool6/transport_analytics.py`
- **Purpose**: Finds cheapest supplier and transport options
- **Data**: 
  - `data/simulated_transport.csv`
  - `data/simulated_suppliers.csv`

### Tool 7: `send_supply_manager_suggestion` (NEW)
- **Location**: `backend/tools/tool7/send_supply_manager_suggestion.py`
- **Purpose**: Sends product suggestions to supply manager for products not in inventory
- **Data**: `data/supply_manager_suggestions.csv`

### Tool 8: `adjust_stock_levels` (NEW)
- **Location**: `backend/tools/tool8/adjust_stock_levels.py`
- **Purpose**: Adjusts stock levels (increase/decrease) based on sales performance
- **Data**: `data/products.csv`

## Workflow

The `supply_manager_orchestrator_agent` follows this workflow:

1. **Low Stock Check**: Identifies products below threshold and reorders them
2. **Christmas Analysis**: 
   - Compares Christmas trending products with inventory
   - Increases stock for matching products
   - Sends suggestions for non-matching products
3. **Category Analysis**:
   - Gets top 5 per category → increases stock
   - Gets bottom 5 per category → decreases stock
4. **Final Reorder**: Rechecks and reorders any remaining low stock items

## Usage

### Running the Orchestrator Agent

The orchestrator agent can be invoked through WatsonX Orchestra. It will automatically:

1. Check for low stock items
2. Analyze Christmas trending products
3. Adjust stock levels based on sales performance
4. Send suggestions to supply manager
5. Automatically reorder everything

### Example Agent Invocation

```yaml
# The agent is configured in:
# backend/agent/supply_manager_orchestrator_agent.yaml

# It uses these tools:
tools:
  - check_low_stock
  - analyze_simulated_sales
  - adjust_stock_levels
  - send_supply_manager_suggestion
  - get_top_sales_by_category
  - get_lowest_sales
  - reorder_products
```

## Data Files

### Required CSV Files

1. **products.csv** - Current inventory with columns:
   - `product_id`, `product_name`, `category`, `price`, `stock_level` (or `stock`), `purchased_date`

2. **sales.csv** - Sales transactions with columns:
   - `sale_id`, `product_id`, `product_name`, `category`, `price`, `sale_date`

3. **simulated_christmas_sales_top5000.csv** - Christmas trending products with columns:
   - `product_name`, `units_sold`, `revenue`, etc.

4. **orders.csv** - Order records (auto-generated)

5. **supply_manager_suggestions.csv** - Suggestions for new products (auto-generated)

## Configuration

### Stock Threshold
Default threshold for low stock: **50 units**

### Stock Adjustments
- **Top sellers**: Increase by 50% of current stock
- **Low sellers**: Decrease by 30% of current stock (minimum 10 units)
- **Trending products**: Based on recommended quantity from analysis

### Delivery Time
Expected delivery for all reorders: **7 days from order date**

## Output Files

The system generates/updates:

1. **products.csv** - Updated with new stock levels
2. **orders.csv** - New reorder records
3. **supply_manager_suggestions.csv** - Product suggestions for review

## Notes

- All tools use relative paths from their tool directory
- Products are matched by name (case-insensitive)
- Stock adjustments ensure minimum stock of 10 units
- Failed operations are logged in tool responses
- The system processes products in batches to avoid timeouts

## Dependencies

- `pandas>=2.0.0`
- `ibm_watsonx_orchestrate`
- Python 3.12+

## Agent Architecture

```
supply_manager_orchestrator_agent
├── check_low_stock
├── analyze_simulated_sales
├── adjust_stock_levels
├── send_supply_manager_suggestion
├── get_top_sales_by_category
├── get_lowest_sales
└── reorder_products
```

Each tool is self-contained and can be used independently or as part of the orchestrator workflow.

