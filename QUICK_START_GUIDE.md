# Quick Start Guide - Streamlit Dashboard

## 🚀 Quick Start (5 Minutes)

### Step 1: Configure Environment

1. **Copy environment template**:
   ```bash
   cp .env.example .env
   ```

2. **Edit `.env` file** with your credentials:
   ```env
   WO_INSTANCE=https://api.eu-central-1.dl.watson-orchestrate.ibm.com/instances/YOUR_INSTANCE_ID
   WO_API_KEY=your_api_key_here
   SUPERMARKET_AGENT_ID=supermarket_inventory_manager_agent
   ```

   **How to get credentials:**
   - **WO_INSTANCE**: Go to WatsonX Orchestrate console → Your instance URL
   - **WO_API_KEY**: WatsonX Console → Settings → API Keys → Generate/Copy
   - **SUPERMARKET_AGENT_ID**: Use `supermarket_inventory_manager_agent` (or find agent ID in console)

### Step 2: Install Dependencies

```bash
pip install -r ai_supermarket/requirements.txt
```

### Step 3: Run Dashboard

**Option A: Using the script** (Recommended)
```bash
./run_dashboard.sh
```

**Option B: Direct command**
```bash
streamlit run ai_supermarket/frontend/app.py
```

### Step 4: Access Dashboard

Open your browser to: **http://localhost:8501**

## 📋 First Steps

1. **Configure API** (if not using .env):
   - Click sidebar → "WatsonX Orchestrate Settings"
   - Enter your API URL and Key
   - Click "💾 Save Configuration"

2. **Test Connection**:
   - Click "🔍 Check Low Stock" in sidebar
   - Wait for response
   - Verify it works!

3. **Try Commands**:
   - Use quick action buttons
   - Or type in chat: "Check low stock products"

## 🎯 Common Commands

| Command | What It Does |
|---------|-------------|
| "Check low stock" | Finds products below 50 units (first 20) |
| "Reorder low stock" | Reorders first 20 low stock products |
| "Get top sales" | Shows top 20 sellers by category |
| "Get lowest sales" | Shows bottom 20 sellers by category |
| "Analyze Christmas trends" | Analyzes trending products |
| "Run full workflow" | Executes all 4 phases |

## ⚠️ Troubleshooting

### Dashboard won't start
- Check Python version: `python --version` (need 3.12+)
- Install dependencies: `pip install -r ai_supermarket/requirements.txt`

### "API URL or API Key not configured"
- Check `.env` file exists
- Verify credentials in sidebar
- Click "💾 Save Configuration"

### "Request timed out"
- Agent is processing large task
- Wait 2-3 minutes
- Try simpler command first

### "HTTP Error: 404"
- Verify agent ID is correct
- Check agent exists in WatsonX console
- Ensure agent is deployed

### "HTTP Error: 401"
- API key is invalid/expired
- Regenerate API key in WatsonX console
- Update `.env` file

## 📖 Full Documentation

See `STREAMLIT_DASHBOARD_GUIDE.md` for complete documentation.

## 🎨 Dashboard Features

- ✅ Modern purple-blue gradient design
- ✅ Interactive chat interface
- ✅ Quick action buttons
- ✅ Real-time agent responses
- ✅ Configuration panel
- ✅ Error handling
- ✅ Conversation history

## 🔗 Next Steps

1. Test all quick actions
2. Try custom commands in chat
3. Run full inventory management workflow
4. Monitor agent performance
5. Adjust inventory thresholds as needed

Enjoy! 🛒🤖

