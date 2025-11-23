# Flask-Based UI for WatsonX Orchestrate Agent

## Overview

This is a modern, lightweight web-based UI for interacting with your WatsonX Orchestrate agent. It's an alternative to the Streamlit dashboard, built with Flask backend and vanilla HTML/CSS/JavaScript frontend.

## Features

- 🎨 **Modern Design**: Beautiful gradient UI with smooth animations
- 💬 **Chat Interface**: Interactive chat with your agent
- ⚡ **Quick Actions**: Pre-configured buttons for common tasks
- ⚙️ **Easy Configuration**: Simple modal for API settings
- 📱 **Responsive**: Works on desktop and mobile devices
- 🚀 **Lightweight**: No heavy dependencies, fast loading

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

Or install Flask separately:
```bash
pip install flask flask-cors
```

### 2. Configure Environment Variables

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit `.env` with your credentials:

```env
# WatsonX Orchestrate Configuration
WO_INSTANCE=https://api.eu-central-1.dl.watson-orchestrate.ibm.com/instances/YOUR_INSTANCE_ID
WO_API_KEY=your_api_key_here
SUPERMARKET_AGENT_ID=supermarket_inventory_manager_agent

# Flask Configuration (optional)
FLASK_PORT=5000
FLASK_DEBUG=False
```

## Running the UI

### Option 1: Using the Script (Recommended)

```bash
./run_flask_ui.sh
```

### Option 2: Direct Command

```bash
cd ai_supermarket/frontend
python flask_app.py
```

### Option 3: Using Flask CLI

```bash
cd ai_supermarket/frontend
export FLASK_APP=flask_app.py
flask run
```

## Accessing the UI

Once started, open your browser to:

**http://localhost:5000**

## Usage

### 1. Configure API Settings

1. Click the **"⚙️ Configuration"** button in the top right
2. Enter your:
   - **API URL**: Your WatsonX Orchestrate instance URL (without `/api`)
   - **API Key**: Your API key from WatsonX console
   - **Agent ID**: `supermarket_inventory_manager_agent`
3. Click **"💾 Save Configuration"**

### 2. Use Quick Actions

Click any quick action button in the sidebar:
- **🔍 Check Low Stock**: Find products below 50 units
- **📊 Get Lowest Sales**: Get bottom 20 sellers by category
- **📈 Get Top Sales**: Get top 20 sellers by category
- **🎄 Analyze Christmas Trends**: Analyze trending products
- **🔄 Reorder Low Stock**: Reorder low stock products
- **📦 Full Workflow**: Execute complete 4-phase workflow

### 3. Chat with Agent

Type your message in the chat input and press Enter or click Send. Examples:
- "Check low stock products"
- "What are the top selling products?"
- "Analyze Christmas sales trends"
- "Run full inventory management workflow"

## API Endpoints

The Flask backend provides these REST API endpoints:

### `GET /api/health`
Health check endpoint

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-11-23T12:00:00",
  "config_loaded": true
}
```

### `GET /api/config`
Get current configuration (without sensitive data)

**Response:**
```json
{
  "api_url": "https://api...",
  "agent_id": "supermarket_inventory_manager_agent",
  "api_key_set": true
}
```

### `POST /api/config`
Update configuration

**Request:**
```json
{
  "api_url": "https://api...",
  "api_key": "your_key",
  "agent_id": "supermarket_inventory_manager_agent"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Configuration updated successfully",
  "config": {...}
}
```

### `POST /api/chat`
Send a message to the agent

**Request:**
```json
{
  "message": "Check low stock",
  "api_url": "https://api...",
  "api_key": "your_key",
  "agent_id": "supermarket_inventory_manager_agent"
}
```

**Response:**
```json
{
  "success": true,
  "response": {...},
  "timestamp": "2025-11-23T12:00:00"
}
```

### `POST /api/quick-action`
Execute a quick action

**Request:**
```json
{
  "action": "check_low_stock",
  "api_url": "https://api...",
  "api_key": "your_key",
  "agent_id": "supermarket_inventory_manager_agent"
}
```

**Response:**
```json
{
  "success": true,
  "action": "check_low_stock",
  "response": {...},
  "timestamp": "2025-11-23T12:00:00"
}
```

## Project Structure

```
ai_supermarket/frontend/
├── flask_app.py          # Flask backend server
└── static/
    ├── index.html        # Main HTML page
    ├── styles.css        # CSS styling
    └── app.js           # JavaScript logic
```

## Customization

### Change Port

Edit `.env`:
```env
FLASK_PORT=8080
```

Or set environment variable:
```bash
export FLASK_PORT=8080
python flask_app.py
```

### Enable Debug Mode

Edit `.env`:
```env
FLASK_DEBUG=True
```

### Modify UI Colors

Edit `static/styles.css` and change CSS variables:
```css
:root {
    --primary-color: #667eea;
    --secondary-color: #764ba2;
    /* ... */
}
```

## Troubleshooting

### Port Already in Use

If port 5000 is already in use:
```bash
export FLASK_PORT=5001
python flask_app.py
```

### CORS Errors

CORS is enabled by default. If you encounter issues, check that `flask-cors` is installed:
```bash
pip install flask-cors
```

### API Connection Issues

1. Check your `.env` file has correct credentials
2. Verify API URL format (no `/api` at the end)
3. Ensure API key is valid and not expired
4. Check agent ID matches your WatsonX console

### Static Files Not Loading

Ensure the `static/` directory exists:
```bash
ls -la ai_supermarket/frontend/static/
```

## Comparison: Flask UI vs Streamlit

| Feature | Flask UI | Streamlit |
|---------|----------|-----------|
| **Setup** | Simple | Simple |
| **Dependencies** | Lightweight | Heavier |
| **Customization** | Full control | Limited |
| **Performance** | Fast | Moderate |
| **Mobile** | Responsive | Responsive |
| **Deployment** | Easy | Easy |
| **Learning Curve** | HTML/CSS/JS | Python |

## Advantages of Flask UI

1. ✅ **Lightweight**: Minimal dependencies
2. ✅ **Fast**: No Python overhead for UI rendering
3. ✅ **Customizable**: Full control over HTML/CSS/JS
4. ✅ **Standard**: Uses standard web technologies
5. ✅ **Deployable**: Easy to deploy to any web server
6. ✅ **RESTful**: Clean API endpoints

## Next Steps

1. **Deploy to Production**: Use gunicorn or uWSGI
2. **Add Authentication**: Implement user login
3. **Add WebSockets**: For real-time updates
4. **Add Charts**: Use Chart.js or D3.js for visualizations
5. **Add Dark Mode**: Toggle between light/dark themes

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review the API endpoints documentation
3. Check WatsonX Orchestrate console for agent status

Enjoy your new UI! 🎉

