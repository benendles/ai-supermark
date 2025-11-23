# Quick Start - Flask UI

## 🚀 Run in 3 Steps

### Step 1: Install Dependencies
```bash
pip install flask flask-cors
```

### Step 2: Configure (if not already done)
```bash
# Edit .env file with your credentials
WO_INSTANCE=https://api.eu-central-1.dl.watson-orchestrate.ibm.com/instances/YOUR_ID
WO_API_KEY=your_api_key_here
SUPERMARKET_AGENT_ID=supermarket_inventory_manager_agent
```

### Step 3: Run
```bash
./run_flask_ui.sh
```

Or directly:
```bash
cd ai_supermarket/frontend
python flask_app.py
```

## 🌐 Access

Open browser: **http://localhost:5000**

## ⚙️ First Time Setup

1. Click **"⚙️ Configuration"** button
2. Enter your API URL, API Key, and Agent ID
3. Click **"💾 Save Configuration"**
4. Start using the UI!

## 🎯 Quick Actions

- **Check Low Stock** - Find products below 50 units
- **Get Top Sales** - Top 20 sellers by category
- **Get Lowest Sales** - Bottom 20 sellers
- **Analyze Christmas Trends** - Trending products
- **Reorder Low Stock** - Reorder low stock items
- **Full Workflow** - Complete 4-phase workflow

## 💬 Chat

Type any command in the chat:
- "Check low stock"
- "What are the top selling products?"
- "Run full inventory workflow"

That's it! Enjoy your new UI! 🎉

