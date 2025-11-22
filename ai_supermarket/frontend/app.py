import streamlit as st
import requests

# Session state initialization
if 'api_url' not in st.session_state:
    st.session_state.api_url = "https://your-orchestrate-endpoint"
if 'api_key' not in st.session_state:
    st.session_state.api_key = "YOUR_API_KEY"
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
        /* Dark theme with accent colors */
        .stApp {
            background: linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 100%);
        }
        
        /* Card styling */
        .agent-card {
            background: rgba(0, 255, 127, 0.05);
            border: 1px solid #00FF7F;
            border-radius: 12px;
            padding: 20px;
            margin: 10px 0;
        }
        
        /* Button styling */
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
        
        /* Input styling */
        .stTextInput>div>div>input, .stTextArea textarea {
            background-color: #1a1a1a;
            color: #00FF7F;
            border: 1px solid #00FF7F;
            border-radius: 8px;
        }
        
        /* Sidebar */
        [data-testid="stSidebar"] {
            background-color: #0f0f0f;
        }
        
        /* Headers */
        h1, h2, h3 {
            color: #00FF7F !important;
        }
    </style>
""", unsafe_allow_html=True)

# Utility function
def call_agent(agent_id: str, prompt: str):
    try:
        response = requests.post(
            f"{st.session_state.api_url}/api/v1/orchestrate/{agent_id}/chat/completions",
            headers={"Authorization": f"Bearer {st.session_state.api_key}"},
            json={"messages": [{"role": "user", "content": prompt}]},
            timeout=15
        )
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"❌ Error: {str(e)}"

# Sidebar
with st.sidebar:
    st.title("⚙️ Settings")
    
    with st.expander("🔗 API Configuration", expanded=False):
        st.session_state.api_url = st.text_input("API URL", st.session_state.api_url)
        st.session_state.api_key = st.text_input("API Key", st.session_state.api_key, type="password")
    
    with st.expander("🤖 Agent IDs", expanded=False):
        st.session_state.product_agent_id = st.text_input("Product Agent", st.session_state.product_agent_id)
        st.session_state.reorder_agent_id = st.text_input("Reorder Agent", st.session_state.reorder_agent_id)
        st.session_state.suggest_agent_id = st.text_input("Suggestion Agent", st.session_state.suggest_agent_id)
        st.session_state.shipping_agent_id = st.text_input("Shipping Agent", st.session_state.shipping_agent_id)

# Main content
st.title("🛒 AI Supermarket Dashboard")
st.caption("AI-powered inventory management & logistics")

# Tabs for better organization
tab1, tab2, tab3, tab4 = st.tabs(["📦 Products", "♻️ Reorder", "💡 Suggestions", "🚚 Shipping"])

with tab1:
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔍 Show All Products", use_container_width=True):
            with st.spinner("Fetching products..."):
                result = call_agent(st.session_state.product_agent_id, "Show all products")
                st.text_area("Results", result, height=300)
    
    with col2:
        query = st.text_input("🔎 Search Product")
        if st.button("Search", use_container_width=True):
            with st.spinner("Searching..."):
                result = call_agent(st.session_state.product_agent_id, f"Search product: {query}")
                st.text_area("Search Results", result, height=300)

with tab2:
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Reorder Low Stock", use_container_width=True):
            with st.spinner("Processing..."):
                result = call_agent(st.session_state.reorder_agent_id, "Reorder low stock products")
                st.success("Reorder initiated!")
                st.text_area("Details", result, height=300)
    
    with col2:
        if st.button("📊 Show Inventory", use_container_width=True):
            with st.spinner("Loading..."):
                result = call_agent(st.session_state.reorder_agent_id, "Show inventory levels")
                st.text_area("Inventory", result, height=300)

with tab3:
    if st.button("🧠 Generate Suggestions", use_container_width=True):
        with st.spinner("Analyzing trends..."):
            result = call_agent(st.session_state.suggest_agent_id, "Suggest new products based on sales trends")
            st.text_area("AI Suggestions", result, height=400)

with tab4:
    with st.form("shipping_form"):
        origin = st.text_input("📍 Origin Address")
        destination = st.text_input("📍 Destination Address")
        weight = st.number_input("⚖️ Weight (kg)", min_value=0.1, value=1.0)
        
        if st.form_submit_button("Find Cheapest Option", use_container_width=True):
            with st.spinner("Comparing rates..."):
                prompt = f"Find cheapest shipping from {origin} to {destination} for {weight}kg"
                result = call_agent(st.session_state.shipping_agent_id, prompt)
                st.text_area("Shipping Options", result, height=300)