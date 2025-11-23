import streamlit as st
import requests
import os
from datetime import datetime
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

# Get credentials from .env file
WO_INSTANCE = os.getenv("WO_INSTANCE", "")
WO_API_KEY = os.getenv("WO_API_KEY", "")
SUPERMARKET_AGENT_ID = os.getenv("SUPERMARKET_AGENT_ID", "supermarket_inventory_manager_agent")

# Page config
st.set_page_config(
    page_title="AI Supermarket Inventory Manager",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="🛒"
)

# Modern CSS styling with professional design
st.markdown("""
    <style>
        .stApp {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }
        .main-header {
            background: rgba(255, 255, 255, 0.95);
            padding: 2rem;
            border-radius: 15px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            margin-bottom: 2rem;
        }
        .agent-card {
            background: rgba(255, 255, 255, 0.95);
            border: 2px solid #667eea;
            border-radius: 15px;
            padding: 1.5rem;
            margin: 1rem 0;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
            transition: transform 0.3s;
        }
        .agent-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 24px rgba(102, 126, 234, 0.3);
        }
        .stButton>button {
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 10px;
            padding: 0.75rem 2rem;
            font-weight: 600;
            font-size: 1rem;
            transition: all 0.3s;
            width: 100%;
        }
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
        }
        .stTextInput>div>div>input, .stTextArea textarea {
            background-color: white;
            color: #333;
            border: 2px solid #667eea;
            border-radius: 10px;
            padding: 0.5rem;
        }
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
        }
        .sidebar .sidebar-content {
            color: white;
        }
        h1, h2, h3 {
            color: #333 !important;
        }
        .status-success {
            background: #10b981;
            color: white;
            padding: 1rem;
            border-radius: 10px;
            margin: 1rem 0;
        }
        .status-error {
            background: #ef4444;
            color: white;
            padding: 1rem;
            border-radius: 10px;
            margin: 1rem 0;
        }
        .phase-indicator {
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 0.5rem 1rem;
            border-radius: 20px;
            display: inline-block;
            margin: 0.5rem 0;
        }
    </style>
""", unsafe_allow_html=True)

# Session state initialization
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'api_url' not in st.session_state:
    # Use instance URL directly (without /api suffix) - WatsonX handles routing
    st.session_state.api_url = WO_INSTANCE if WO_INSTANCE else ""
if 'api_key' not in st.session_state:
    st.session_state.api_key = WO_API_KEY if WO_API_KEY else ""
if 'agent_id' not in st.session_state:
    st.session_state.agent_id = SUPERMARKET_AGENT_ID

# Utility function to call WatsonX Orchestrate agent
def call_watsonx_agent(prompt: str):
    """Call the WatsonX Orchestrate agent API"""
    try:
        api_url = st.session_state.api_url
        api_key = st.session_state.api_key.strip() if st.session_state.api_key else ""
        agent_id = st.session_state.agent_id
        
        # Validate configuration
        if not api_url:
            return {"error": "API URL not configured. Please set it in the sidebar or .env file."}
        
        if not api_key:
            return {"error": "API Key not configured. Please set it in the sidebar or .env file."}
        
        if not agent_id:
            return {"error": "Agent ID not configured. Please set it in the sidebar or .env file."}
        
        # Clean API URL - remove trailing slashes
        api_url = api_url.rstrip('/')
        
        # WatsonX Orchestrate API endpoint format
        # The instance URL should be: https://api.{region}.dl.watson-orchestrate.ibm.com/instances/{id}
        # API endpoint is: {instance_url}/api/v1/orchestrate/runs
        if '/instances/' in api_url:
            # If it's an instance URL, add /api
            if not api_url.endswith('/api'):
                api_url = f"{api_url}/api"
        elif not api_url.endswith('/api'):
            # If it doesn't have /api, add it
            api_url = f"{api_url}/api"
        
        # WatsonX Orchestrate API endpoint
        url = f"{api_url}/v1/orchestrate/runs"
        
        # Ensure API key is not empty and properly formatted
        if not api_key or api_key.strip() == "" or api_key == "your_api_key_here":
            return {"error": "Invalid API Key. Please provide a valid API key in the sidebar or .env file. The API key cannot be empty."}
        
        # Remove any whitespace from API key
        api_key = api_key.strip()
        
        # Build headers - ensure Authorization header is properly formatted
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        # Verify header is set correctly
        if "Authorization" not in headers or not headers["Authorization"].startswith("Bearer "):
            return {"error": "Failed to set Authorization header. Please check API key configuration."}
        
        payload = {
            "agent_id": agent_id,
            "input": prompt
        }
        
        response = requests.post(url, headers=headers, json=payload, timeout=120)
        response.raise_for_status()
        return response.json()
        
    except requests.exceptions.Timeout:
        return {"error": "Request timed out. The agent is processing a large task. Please wait and try again."}
    except requests.exceptions.HTTPError as e:
        error_text = e.response.text if hasattr(e, 'response') and e.response else str(e)
        return {"error": f"HTTP Error {e.response.status_code}: {error_text}"}
    except Exception as e:
        return {"error": f"Error calling agent: {str(e)}"}

# Sidebar Configuration
with st.sidebar:
    st.title("⚙️ Configuration")
    st.markdown("---")
    
    with st.expander("🔗 WatsonX Orchestrate Settings", expanded=True):
        st.markdown("**Configure your WatsonX Orchestrate connection:**")
        
        api_url = st.text_input(
            "API URL (Instance URL)", 
            value=st.session_state.api_url,
            help="Your WatsonX Orchestrate instance URL (e.g., https://api.eu-central-1.dl.watson-orchestrate.ibm.com/instances/xxx)",
            placeholder="https://api.eu-central-1.dl.watson-orchestrate.ibm.com/instances/YOUR_INSTANCE_ID"
        )
        
        api_key = st.text_input(
            "API Key", 
            value=st.session_state.api_key if st.session_state.api_key else "",
            type="password",
            help="Your WatsonX Orchestrate API key (from Settings > API Keys)",
            placeholder="Enter your API key"
        )
        
        agent_id = st.text_input(
            "Agent ID", 
            value=st.session_state.agent_id,
            help="The ID or name of your agent (usually: supermarket_inventory_manager_agent)",
            placeholder="supermarket_inventory_manager_agent"
        )
        
        # Show current configuration status
        st.markdown("---")
        if api_url and api_key and agent_id:
            st.success("✅ Configuration looks good!")
        else:
            st.warning("⚠️ Please fill in all fields")
        
        if st.button("💾 Save Configuration", use_container_width=True):
            if api_url and api_key and agent_id:
                st.session_state.api_url = api_url.strip()
                st.session_state.api_key = api_key.strip()
                st.session_state.agent_id = agent_id.strip()
                st.success("✅ Configuration saved successfully!")
                st.rerun()
            else:
                st.error("❌ Please fill in all fields before saving")
    
    st.markdown("---")
    st.markdown("### 📋 Quick Actions")
    
    quick_actions = {
        "🔍 Check Low Stock": "Check for products with low stock (below 50 units)",
        "📊 Get Lowest Sales": "Get the 20 products with lowest sales by category",
        "📈 Get Top Sales": "Get the 20 top selling products by category",
        "🎄 Analyze Christmas Trends": "Analyze Christmas trending products",
        "🔄 Reorder Low Stock": "Reorder the first 20 low stock products",
        "📦 Full Inventory Management": "Run complete inventory management workflow (all 4 phases)"
    }
    
    for action, description in quick_actions.items():
        if st.button(action, use_container_width=True, key=f"quick_{action}"):
            st.session_state.quick_action = action
            st.rerun()

# Main content
st.markdown('<div class="main-header">', unsafe_allow_html=True)
st.title("🛒 AI Supermarket Inventory Manager")
st.caption("Powered by WatsonX Orchestrate - Comprehensive Inventory Management System")
st.markdown('</div>', unsafe_allow_html=True)

# Handle quick actions
if 'quick_action' in st.session_state:
    action = st.session_state.quick_action
    prompt_map = {
        "🔍 Check Low Stock": "Check for products with low stock (below 50 units). Process first 20 products.",
        "📊 Get Lowest Sales": "Get the 20 products with lowest sales by category",
        "📈 Get Top Sales": "Get the 20 top selling products by category",
        "🎄 Analyze Christmas Trends": "Analyze Christmas trending products and compare with inventory",
        "🔄 Reorder Low Stock": "Reorder the first 20 low stock products. Find cheapest transport for each and place orders.",
        "📦 Full Inventory Management": "Execute the complete inventory management workflow: Phase 1 (Low Stock), Phase 2 (Christmas Trends), Phase 3 (Sales Performance), Phase 4 (Final Check). Process maximum 20 products per phase."
    }
    
    prompt = prompt_map.get(action, action)
    del st.session_state.quick_action
    
    # Check if configuration is set
    if not st.session_state.api_url or not st.session_state.api_key:
        st.markdown(f'<div class="status-error">❌ Please configure API URL and API Key in the sidebar first!</div>', unsafe_allow_html=True)
    else:
        with st.spinner(f"Processing {action}..."):
            result = call_watsonx_agent(prompt)
            
            if "error" in result:
                st.markdown(f'<div class="status-error">❌ Error: {result["error"]}</div>', unsafe_allow_html=True)
                # Show helpful message for 401 errors
                if "401" in str(result.get("error", "")) or "unauthorized" in str(result.get("error", "")).lower():
                    st.info("💡 **Tip**: Check that your API Key is correct and not expired. You can generate a new one in WatsonX Orchestrate console → Settings → API Keys")
            else:
                st.markdown(f'<div class="status-success">✅ {action} completed successfully!</div>', unsafe_allow_html=True)
                st.json(result)

# Chat Interface
st.markdown("---")
st.markdown("### 💬 Chat with Inventory Manager Agent")

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask the inventory manager agent..."):
    # Check configuration first
    if not st.session_state.api_url or not st.session_state.api_key:
        st.error("❌ Please configure API URL and API Key in the sidebar first!")
    else:
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get agent response
        with st.chat_message("assistant"):
            with st.spinner("Agent is thinking..."):
                response = call_watsonx_agent(prompt)
                
                if "error" in response:
                    error_msg = f"❌ Error: {response['error']}"
                    st.markdown(error_msg)
                    # Show helpful message for 401 errors
                    if "401" in str(response.get("error", "")) or "unauthorized" in str(response.get("error", "")).lower():
                        st.info("💡 **Tip**: Your API Key might be incorrect or expired. Check the sidebar configuration or generate a new key in WatsonX Orchestrate console.")
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})
                else:
                    # Format response nicely
                    if isinstance(response, dict):
                        response_text = json.dumps(response, indent=2)
                    else:
                        response_text = str(response)
                    
                    st.markdown("**Agent Response:**")
                    st.code(response_text, language="json")
                    st.session_state.messages.append({"role": "assistant", "content": response_text})

# Information Section
with st.expander("ℹ️ About This Dashboard", expanded=False):
    st.markdown("""
    ### 🎯 Features
    
    This dashboard connects to your **WatsonX Orchestrate** agent to provide:
    
    - **Low Stock Detection**: Automatically identifies products below reorder threshold
    - **Christmas Trends Analysis**: Analyzes trending products from Christmas sales data
    - **Sales Performance**: Identifies top and bottom sellers by category
    - **Automatic Reordering**: Places orders with optimal transport options
    - **Stock Adjustments**: Increases stock for top sellers, decreases for low sellers
    - **Supply Manager Suggestions**: Suggests new products based on trends
    
    ### 📋 Workflow Phases
    
    1. **Phase 1**: Low Stock Detection & Reordering
    2. **Phase 2**: Christmas Trending Products Analysis
    3. **Phase 3**: Sales Performance Analysis by Category
    4. **Phase 4**: Final Reorder & Summary
    
    ### ⚙️ Configuration
    
    Set your WatsonX Orchestrate credentials in the sidebar or use a `.env` file:
    - `WO_INSTANCE`: Your WatsonX Orchestrate instance URL
    - `WO_API_KEY`: Your API key
    - `SUPERMARKET_AGENT_ID`: Agent ID (default: supermarket_inventory_manager_agent)
    """)

# Footer
st.markdown("---")
st.caption("🛒 AI Supermarket Inventory Manager | Powered by WatsonX Orchestrate")
