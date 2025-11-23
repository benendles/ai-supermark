import streamlit as st
import requests

# Credentials
WO_INSTANCE = "https://api.eu-central-1.dl.watson-orchestrate.ibm.com/instances/20251122-1952-5015-406d-88c46ca8b12a"
WO_API_KEY = "azE6dXNyXzcwMzczYTg0LWQwZGMtMzU1MC04N2MzLTc3MjI5MmIzNDQwZjo2NjBCWmJOQitTeCtRRWhOODFCbkNETGZldzR3Z2xJeGVqeDR4TW1udFY4PTo2VFkz"

# Session state initialization
if 'api_url' not in st.session_state:
    st.session_state.api_url = f"{WO_INSTANCE}/api"
if 'api_key' not in st.session_state:
    st.session_state.api_key = WO_API_KEY
if 'product_agent_id' not in st.session_state:
    st.session_state.product_agent_id = "agent-product"
if 'reorder_agent_id' not in st.session_state:
    st.session_state.reorder_agent_id = "agent-reorder"
if 'suggest_agent_id' not in st.session_state:
    st.session_state.suggest_agent_id = "agent-suggest"
if 'shipping_agent_id' not in st.session_state:
    st.session_state.shipping_agent_id = "agent-ship"

# Page config
st.set_page_config(
    page_title="AI Supermarket Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Modern CSS styling
st.markdown("""
    <style>
        .stApp {
            background: linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 100%);
        }
        .agent-card {
            background: rgba(0, 255, 127, 0.05);
            border: 1px solid #00FF7F;
            border-radius: 12px;
            padding: 20px;
            margin: 10px 0;
        }
        .stButton>button {
            background: linear-gradient(90deg, #00FF7F 0%, #00CC66 100%);
            color: black;
            border: none;
            border-radius: 8px;
            padding: 12px 24px;
            font-weight: 600;
            transition: all 0.3s;
        }
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0, 255, 127, 0.4);
        }
        .stTextInput>div>div>input, .stTextArea textarea {
            background-color: #1a1a1a;
            color: #00FF7F;
            border: 1px solid #00FF7F;
            border-radius: 8px;
        }
        [data-testid="stSidebar"] {
            background-color: #0f0f0f;
        }
        h1, h2, h3 {
            color: #00FF7F !important;
        }
    </style>
""", unsafe_allow_html=True)

# Utility function
def call_agent(agent_id: str, prompt: str):
    try:
        response = requests.post(
            f"{st.session_state.api_url}/v1/orchestrate/runs",
            headers={
                "Authorization": f"Bearer {st.session_state.api_key}",
                "Content-Type": "application/json"
            },
            json={
                "agent_id": agent_id,
                "input": prompt
            },
            timeout=15
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}

# Sidebar
with st.sidebar:
    st.title("⚙️ Settings")
    
    with st.expander("🔗 API Configuration", expanded=False):
        api_url = st.text_input("API URL", value=st.session_state.api_url, key="api_url_input")
        api_key = st.text_input("API Key", value=st.session_state.api_key, type="password", key="api_key_input")
        
        # Update session state when values change
        if api_url != st.session_state.api_url:
            st.session_state.api_url = api_url
        if api_key != st.session_state.api_key:
            st.session_state.api_key = api_key
    
    with st.expander("🤖 Agent IDs", expanded=False):
        product_agent = st.text_input("Product Agent", value=st.session_state.product_agent_id, key="product_agent_input")
        reorder_agent = st.text_input("Reorder Agent", value=st.session_state.reorder_agent_id, key="reorder_agent_input")
        suggest_agent = st.text_input("Suggestion Agent", value=st.session_state.suggest_agent_id, key="suggest_agent_input")
        shipping_agent = st.text_input("Shipping Agent", value=st.session_state.shipping_agent_id, key="shipping_agent_input")
        
        # Update session state
        if product_agent != st.session_state.product_agent_id:
            st.session_state.product_agent_id = product_agent
        if reorder_agent != st.session_state.reorder_agent_id:
            st.session_state.reorder_agent_id = reorder_agent
        if suggest_agent != st.session_state.suggest_agent_id:
            st.session_state.suggest_agent_id = suggest_agent
        if shipping_agent != st.session_state.shipping_agent_id:
            st.session_state.shipping_agent_id = shipping_agent

# Main content
st.title("🛒 AI Supermarket Dashboard")
st.caption("AI-powered inventory management & logistics")

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["📦 Products", "♻️ Reorder", "💡 Suggestions", "🚚 Shipping"])

with tab1:
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔍 Show All Products", use_container_width=True):
            with st.spinner("Fetching products..."):
                result = call_agent(st.session_state.product_agent_id, "Show all products")
                st.json(result)
    
    with col2:
        query = st.text_input("🔎 Search Product")
        if st.button("Search", use_container_width=True):
            with st.spinner("Searching..."):
                result = call_agent(st.session_state.product_agent_id, f"Search product: {query}")
                st.json(result)

with tab2:
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Reorder Low Stock", use_container_width=True):
            with st.spinner("Processing..."):
                result = call_agent(st.session_state.reorder_agent_id, "Reorder low stock products")
                st.success("Reorder initiated!")
                st.json(result)
    
    with col2:
        if st.button("📊 Show Inventory", use_container_width=True):
            with st.spinner("Loading..."):
                result = call_agent(st.session_state.reorder_agent_id, "Show inventory levels")
                st.json(result)

with tab3:
    if st.button("🧠 Generate Suggestions", use_container_width=True):
        with st.spinner("Analyzing trends..."):
            result = call_agent(st.session_state.suggest_agent_id, "Suggest new products based on sales trends")
            st.json(result)

with tab4:
    with st.form("shipping_form"):
        origin = st.text_input("📍 Origin Address")
        destination = st.text_input("📍 Destination Address")
        weight = st.number_input("⚖️ Weight (kg)", min_value=0.1, value=1.0)
        
        if st.form_submit_button("Find Cheapest Option", use_container_width=True):
            with st.spinner("Comparing rates..."):
                prompt = f"Find cheapest shipping from {origin} to {destination} for {weight}kg"
                result = call_agent(st.session_state.shipping_agent_id, prompt)
                st.json(result)