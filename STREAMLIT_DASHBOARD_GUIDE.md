# Streamlit Dashboard User Manual

## Overview

The AI Supermarket Inventory Manager Dashboard is a modern web interface that connects to your WatsonX Orchestrate agent to manage supermarket inventory. All commands from the dashboard are sent to the `supermarket_inventory_manager_agent`, and responses are displayed in real-time.

## Prerequisites

1. **Python 3.12+** installed
2. **WatsonX Orchestrate** instance and API key
3. **Agent deployed**: `supermarket_inventory_manager_agent` must be imported in WatsonX Orchestrate

## Installation

### 1. Install Dependencies

```bash
cd /Users/macbookpro2020/Desktop/ai-supermark-1
pip install -r ai_supermarket/requirements.txt
```

### 2. Configure Environment Variables

Create a `.env` file in the project root:

```bash
# Copy the example file
cp .env.example .env
```

Edit `.env` with your credentials:

```env
# WatsonX Orchestrate Configuration
WO_INSTANCE=https://api.eu-central-1.dl.watson-orchestrate.ibm.com/instances/YOUR_INSTANCE_ID
WO_API_KEY=your_api_key_here

# Agent ID
SUPERMARKET_AGENT_ID=supermarket_inventory_manager_agent
```

**How to get your credentials:**
- **WO_INSTANCE**: Your WatsonX Orchestrate instance URL (found in your WatsonX console)
- **WO_API_KEY**: Your API key (generate from WatsonX console)
- **SUPERMARKET_AGENT_ID**: The ID of your agent (usually `supermarket_inventory_manager_agent`)

### 3. Run the Dashboard

```bash
cd /Users/macbookpro2020/Desktop/ai-supermark-1
streamlit run ai_supermarket/frontend/app.py
```

The dashboard will open in your browser at `http://localhost:8501`

## Dashboard Features

### Main Interface

The dashboard has a modern, professional design with:

- **Gradient Background**: Purple-blue gradient theme
- **Chat Interface**: Interactive chat with the inventory manager agent
- **Quick Actions**: Pre-configured buttons for common tasks
- **Configuration Panel**: Sidebar for API settings

### Quick Actions

Located in the sidebar, these buttons execute common inventory management tasks:

1. **🔍 Check Low Stock**
   - Checks for products below 50 units
   - Processes first 20 products
   - Returns list of low stock items

2. **📊 Get Lowest Sales**
   - Gets 20 products with lowest sales by category
   - Helps identify underperforming products

3. **📈 Get Top Sales**
   - Gets 20 top selling products by category
   - Identifies best performers

4. **🎄 Analyze Christmas Trends**
   - Analyzes Christmas sales CSV
   - Compares with inventory
   - Suggests new products

5. **🔄 Reorder Low Stock**
   - Reorders first 20 low stock products
   - Finds cheapest transport
   - Places orders automatically

6. **📦 Full Inventory Management**
   - Executes complete 4-phase workflow:
     - Phase 1: Low Stock Detection
     - Phase 2: Christmas Trends
     - Phase 3: Sales Performance
     - Phase 4: Final Check

### Chat Interface

The main chat interface allows you to:

- **Ask questions** in natural language
- **Send commands** to the agent
- **View responses** in formatted JSON
- **Track conversation** history

**Example Commands:**
- "Check low stock products"
- "Reorder the first 20 low stock products"
- "Analyze Christmas trending products"
- "Get top 5 sellers in each category"
- "Run complete inventory management workflow"

### Configuration Sidebar

The sidebar allows you to:

1. **Set API Credentials**:
   - API URL: Your WatsonX Orchestrate instance URL
   - API Key: Your authentication key
   - Agent ID: The agent to connect to

2. **Save Configuration**: Click "💾 Save Configuration" to persist settings

3. **Quick Actions**: Access pre-configured commands

## Workflow Phases

When you run "Full Inventory Management", the agent executes:

### Phase 1: Low Stock Detection & Reordering
- Checks products below threshold (50 units)
- Processes first 20 products
- Finds cheapest transport
- Places reorders

### Phase 2: Christmas Trending Products
- Analyzes Christmas sales CSV
- Compares with inventory
- Increases stock for trending products
- Sends suggestions for new products

### Phase 3: Sales Performance Analysis
- Gets top 20 sellers by category
- Gets bottom 20 sellers by category
- Increases stock for top sellers
- Decreases stock for low sellers

### Phase 4: Final Reorder & Summary
- Final low stock check
- Reorders remaining items
- Provides comprehensive summary

## Usage Examples

### Example 1: Quick Low Stock Check

1. Click **🔍 Check Low Stock** in sidebar
2. Wait for agent response
3. View list of low stock products

### Example 2: Reorder Low Stock Products

1. Click **🔄 Reorder Low Stock** in sidebar
2. Agent will:
   - Check low stock
   - Find transport for each product
   - Place orders
3. View order confirmation

### Example 3: Full Workflow

1. Click **📦 Full Inventory Management**
2. Agent executes all 4 phases sequentially
3. View comprehensive summary at the end

### Example 4: Custom Command via Chat

1. Type in chat: "Get top 10 selling products in Energy Drinks category"
2. Agent processes request
3. View formatted response

## Troubleshooting

### Error: "API URL or API Key not configured"

**Solution**: 
1. Check your `.env` file exists
2. Verify credentials in sidebar
3. Click "💾 Save Configuration"

### Error: "Request timed out"

**Solution**:
- The agent is processing a large task
- Wait a few minutes and try again
- Use specific commands instead of full workflow

### Error: "HTTP Error: 404"

**Solution**:
- Verify your API URL is correct
- Check that the agent ID exists in WatsonX Orchestrate
- Ensure agent is deployed and active

### Error: "HTTP Error: 401"

**Solution**:
- Verify your API key is correct
- Check API key hasn't expired
- Regenerate API key if needed

### Agent Not Responding

**Solution**:
1. Check WatsonX Orchestrate console - is agent running?
2. Verify agent has all tools imported
3. Check agent logs for errors
4. Try a simpler command first

## Best Practices

1. **Start Simple**: Begin with quick actions before running full workflow
2. **Check Configuration**: Verify API credentials before use
3. **Monitor Responses**: Review agent responses for errors
4. **Use Chat**: For custom queries, use the chat interface
5. **Save Settings**: Always save configuration after changes

## Dashboard Design

The dashboard features:

- **Modern UI**: Purple-blue gradient theme
- **Responsive Layout**: Works on desktop and tablet
- **Real-time Updates**: Live agent responses
- **Error Handling**: Clear error messages
- **Status Indicators**: Visual feedback for success/error
- **Chat History**: Conversation tracking

## API Endpoints

The dashboard uses WatsonX Orchestrate API:

- **Endpoint**: `/v1/orchestrate/runs`
- **Method**: POST
- **Headers**: 
  - `Authorization: Bearer {API_KEY}`
  - `Content-Type: application/json`
- **Payload**:
  ```json
  {
    "agent_id": "supermarket_inventory_manager_agent",
    "input": "your command here"
  }
  ```

## Security Notes

- **Never commit `.env` file** to version control
- **Keep API keys secure**
- **Use environment variables** for production
- **Rotate API keys** regularly

## Support

For issues:
1. Check agent logs in WatsonX Orchestrate console
2. Verify all tools are imported correctly
3. Test agent directly in WatsonX console first
4. Review error messages in dashboard

## Next Steps

After setup:
1. Test with "Check Low Stock" command
2. Try "Reorder Low Stock" to test full workflow
3. Use chat for custom queries
4. Monitor agent performance
5. Adjust inventory thresholds as needed

Enjoy managing your supermarket inventory with AI! 🛒🤖

