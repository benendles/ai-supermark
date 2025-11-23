"""
Flask Backend for WatsonX Orchestrate Agent UI
Provides REST API endpoints for the frontend to interact with WatsonX Orchestrate
"""
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv
from datetime import datetime
import json

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__, static_folder='static', static_url_path='')
CORS(app)  # Enable CORS for frontend

# Get credentials from .env file
WO_INSTANCE = os.getenv("WO_INSTANCE", "")
WO_API_KEY = os.getenv("WO_API_KEY", "")
SUPERMARKET_AGENT_ID = os.getenv("SUPERMARKET_AGENT_ID", "supermarket_inventory_manager_agent")

# In-memory configuration (can be updated via API)
config = {
    "api_url": WO_INSTANCE,
    "api_key": WO_API_KEY,
    "agent_id": SUPERMARKET_AGENT_ID
}


def format_api_url(instance_url: str) -> str:
    """Format the instance URL to the correct API endpoint"""
    if not instance_url:
        return ""
    
    # Remove trailing slashes
    instance_url = instance_url.rstrip('/')
    
    # Add /api if it's an instance URL
    if '/instances/' in instance_url:
        if not instance_url.endswith('/api'):
            instance_url = f"{instance_url}/api"
    elif not instance_url.endswith('/api'):
        instance_url = f"{instance_url}/api"
    
    return f"{instance_url}/v1/orchestrate/runs"


def call_watsonx_agent(prompt: str, api_url: str = None, api_key: str = None, agent_id: str = None) -> dict:
    """Call the WatsonX Orchestrate agent API"""
    try:
        # Use provided params or fall back to config
        api_url = api_url or config["api_url"]
        api_key = api_key or config["api_key"]
        agent_id = agent_id or config["agent_id"]
        
        # Validate configuration
        if not api_url:
            return {"error": "API URL not configured. Please set it in the configuration."}
        
        if not api_key:
            return {"error": "API Key not configured. Please set it in the configuration."}
        
        # Clean and validate API key
        api_key = str(api_key).strip()
        
        if not api_key or api_key == "" or api_key == "your_api_key_here" or api_key.lower() == "none":
            return {"error": "API Key is empty or invalid. Please provide a valid API key in the configuration."}
        
        if not agent_id:
            return {"error": "Agent ID not configured. Please set it in the configuration."}
        
        # Format API URL
        url = format_api_url(api_url)
        
        if not url:
            return {"error": "Invalid API URL format. Please check your instance URL."}
        
        # Build headers
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        # Verify header is set correctly
        if "Authorization" not in headers:
            return {"error": "Failed to set Authorization header."}
        
        auth_header = headers["Authorization"]
        if not auth_header.startswith("Bearer ") or len(auth_header) < 15:  # "Bearer " + at least 8 chars
            return {"error": "API Key appears to be invalid or too short. Please check your API key."}
        
        # Build payload
        payload = {
            "agent_id": agent_id,
            "input": prompt
        }
        
        # Make request
        response = requests.post(url, headers=headers, json=payload, timeout=120)
        response.raise_for_status()
        return response.json()
        
    except requests.exceptions.Timeout:
        return {"error": "Request timed out. The agent is processing a large task. Please wait and try again."}
    except requests.exceptions.HTTPError as e:
        error_text = ""
        status_code = 500
        
        if hasattr(e, 'response') and e.response:
            status_code = e.response.status_code
            try:
                error_text = e.response.text
            except:
                error_text = str(e)
            
            # Provide helpful error messages for common issues
            if status_code == 401:
                return {
                    "error": f"401 Unauthorized: Invalid API key or authentication failed. Please check:\n"
                             f"1. Your API key is correct and not expired\n"
                             f"2. The API key is properly set in the configuration\n"
                             f"3. Generate a new API key from WatsonX Orchestrate console if needed\n"
                             f"Original error: {error_text[:200]}"
                }
            elif status_code == 404:
                return {
                    "error": f"404 Not Found: Agent '{agent_id}' not found. Please check:\n"
                             f"1. The agent ID is correct\n"
                             f"2. The agent is deployed in WatsonX Orchestrate\n"
                             f"Original error: {error_text[:200]}"
                }
        else:
            error_text = str(e)
        
        return {"error": f"HTTP Error {status_code}: {error_text[:500]}"}
    except Exception as e:
        return {"error": f"Error calling agent: {str(e)}"}


@app.route('/')
def index():
    """Serve the main HTML page"""
    return send_from_directory('static', 'index.html')


@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "config_loaded": bool(config["api_url"] and config["api_key"])
    })


@app.route('/api/config', methods=['GET'])
def get_config():
    """Get current configuration (without sensitive data)"""
    return jsonify({
        "api_url": config["api_url"],
        "agent_id": config["agent_id"],
        "api_key_set": bool(config["api_key"] and config["api_key"].strip())
    })


@app.route('/api/config', methods=['POST'])
def update_config():
    """Update configuration"""
    try:
        data = request.get_json()
        
        if "api_url" in data:
            config["api_url"] = data["api_url"].strip()
        if "api_key" in data:
            config["api_key"] = data["api_key"].strip()
        if "agent_id" in data:
            config["agent_id"] = data["agent_id"].strip()
        
        return jsonify({
            "success": True,
            "message": "Configuration updated successfully",
            "config": {
                "api_url": config["api_url"],
                "agent_id": config["agent_id"],
                "api_key_set": bool(config["api_key"] and config["api_key"].strip())
            }
        })
    except Exception as e:
        return jsonify({"error": f"Failed to update configuration: {str(e)}"}), 400


@app.route('/api/chat', methods=['POST'])
def chat():
    """Send a message to the WatsonX Orchestrate agent"""
    try:
        data = request.get_json()
        prompt = data.get("message", "")
        
        if not prompt:
            return jsonify({"error": "Message is required"}), 400
        
        # Get optional overrides from request
        api_url = data.get("api_url")
        api_key = data.get("api_key")
        agent_id = data.get("agent_id")
        
        # Call WatsonX agent
        result = call_watsonx_agent(prompt, api_url, api_key, agent_id)
        
        return jsonify({
            "success": "error" not in result,
            "response": result,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({"error": f"Failed to process request: {str(e)}"}), 500


@app.route('/api/quick-action', methods=['POST'])
def quick_action():
    """Execute a quick action"""
    try:
        data = request.get_json()
        action = data.get("action", "")
        
        # Map actions to prompts
        action_map = {
            "check_low_stock": "Check for products with low stock (below 50 units). Process first 20 products.",
            "get_lowest_sales": "Get the 20 products with lowest sales by category",
            "get_top_sales": "Get the 20 top selling products by category",
            "analyze_christmas": "Analyze Christmas trending products and compare with inventory",
            "reorder_low_stock": "Reorder the first 20 low stock products. Find cheapest transport for each and place orders.",
            "full_workflow": "Execute the complete inventory management workflow: Phase 1 (Low Stock), Phase 2 (Christmas Trends), Phase 3 (Sales Performance), Phase 4 (Final Check). Process maximum 20 products per phase."
        }
        
        prompt = action_map.get(action, action)
        
        if not prompt:
            return jsonify({"error": "Invalid action"}), 400
        
        # Call WatsonX agent
        result = call_watsonx_agent(prompt)
        
        return jsonify({
            "success": "error" not in result,
            "action": action,
            "response": result,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({"error": f"Failed to execute action: {str(e)}"}), 500


if __name__ == '__main__':
    port = int(os.getenv("FLASK_PORT", 5000))
    debug = os.getenv("FLASK_DEBUG", "False").lower() == "true"
    
    print(f"""
    🚀 Starting WatsonX Orchestrate Agent UI Server
    ================================================
    📍 Server: http://localhost:{port}
    🔧 Debug Mode: {debug}
    ⚙️  Configuration:
        - API URL: {config['api_url'] or 'Not set'}
        - Agent ID: {config['agent_id']}
        - API Key: {'Set' if config['api_key'] else 'Not set'}
    
    💡 Open your browser to http://localhost:{port} to access the UI
    """)
    
    app.run(host='0.0.0.0', port=port, debug=debug)

