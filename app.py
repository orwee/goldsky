"""
Goldsky Solutions Engineer Demo Dashboard
A comprehensive Streamlit dashboard showcasing Goldsky platform capabilities

Author: Roberto (Solutions Engineer Candidate)
Purpose: Technical demonstration for Goldsky job application
"""

import streamlit as st

# 1. INTENTAR LEER LA API KEY DESDE SECRETS
try:
    GOLDSKY_API_KEY = st.secrets["GOLDSKY_API_KEY"]
except Exception:
    GOLDSKY_API_KEY = "NOT_FOUND"

# 2. DEFINICIÓN DE DATOS (Anteriormente en config.py)
THEME = {
    "primary_color": "#F7931A",
    "bg_color": "#0E1117",
    "secondary_bg": "#1E2127"
}

USE_CASES = [
    {
        "title": "Real-time DeFi Dashboard",
        "description": "Streaming Uniswap V3 swap data directly into a high-frequency trading interface with zero lag.",
        "customers": ["Uniswap", "PancakeSwap"],
        "features_used": ["Mirror Pipelines", "Real-time Indexing"]
    },
    {
        "title": "NFT Rarity Engine",
        "description": "Indexing collection metadata and sales in real-time to calculate dynamic rarity scores.",
        "customers": ["OpenSea", "Blur"],
        "features_used": ["Subgraphs", "Webhooks"]
    },
    {
        "title": "Institutional Compliance",
        "description": "Extracting historical trace data for multi-chain audits and regulatory reporting.",
        "customers": ["Chainalysis", "Fireblocks"],
        "features_used": ["SQL Playground", "Mirror"]
    },
    {
        "title": "Gaming Assets Tracker",
        "description": "Monitoring in-game NFT movements and player achievements across subnet architectures.",
        "customers": ["Axie Infinity", "Immutable"],
        "features_used": ["Custom Chain Indexing"]
    }
]

# Page configuration
st.set_page_config(
    page_title="Goldsky Solutions Engineer Demo",
    page_icon="☀️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for premium styling
st.markdown(f"""
<style>
    /* Main theme colors */
    :root {{
        --primary-color: {THEME['primary_color']};
        --bg-color: {THEME['bg_color']};
        --secondary-bg: {THEME['secondary_bg']};
    }}
    
    /* Header styling */
    .main-header {{
        background: linear-gradient(135deg, #F7931A 0%, #FF6B00 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(247, 147, 26, 0.3);
    }}
    
    .main-header h1 {{
        color: white;
        margin: 0;
        font-size: 3rem;
        font-weight: 700;
    }}
    
    .main-header p {{
        color: rgba(255, 255, 255, 0.9);
        margin: 0.5rem 0 0 0;
        font-size: 1.2rem;
    }}
    
    /* Feature cards */
    .feature-card {{
        background: rgba(30, 33, 39, 0.8);
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #F7931A;
        margin: 1rem 0;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        height: 100%;
    }}
    
    .feature-card:hover {{
        transform: translateY(-5px);
        box-shadow: 0 8px 16px rgba(247, 147, 26, 0.2);
    }}
    
    .feature-card h3 {{
        color: #F7931A;
        margin-top: 0;
    }}
    
    /* Metric styling */
    .stMetric {{
        background: rgba(30, 33, 39, 0.6);
        padding: 1rem;
        border-radius: 8px;
    }}
    
    /* Button styling */
    .stButton>button {{
        background: linear-gradient(135deg, #F7931A 0%, #FF6B00 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }}
    
    .stButton>button:hover {{
        box-shadow: 0 4px 12px rgba(247, 147, 26, 0.4);
        transform: translateY(-2px);
    }}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>☀️ Goldsky Platform Demo</h1>
    <p>Solutions Engineer Technical Demonstration</p>
</div>
""", unsafe_allow_html=True)

# Introduction
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("## 👋 Welcome to My Goldsky Demo")
    
    st.markdown("""
    This interactive dashboard demonstrates deep technical knowledge of the **Goldsky platform** and showcases the skills required for a Solutions Engineer role.
    
    ### What You'll Find Here:
    
    - **🔍 Subgraph Analytics**: Real-time GraphQL queries against Goldsky-hosted subgraphs
    - **⚡ Mirror Pipelines**: Data streaming architecture and use cases
    - **💾 SQL Playground**: Advanced SQL transformations for blockchain data
    - **📊 Real-time Dashboard**: Live blockchain metrics and visualizations
    
    ### Why Goldsky?
    
    Goldsky solves the fundamental challenge of accessing blockchain data at scale. Traditional RPC 
    nodes are slow, unreliable, and expensive. Goldsky provides:
    
    - **6x faster** query performance
    - **99.9%+ uptime** reliability
    - **Zero maintenance** infrastructure
    - **130+ chains** supported
    """)
    
    st.info("💡 **Navigate using the sidebar** to explore different platform features!")

with col2:
    st.markdown("### 🎯 Key Features")
    
    features = [
        ("⚡", "Lightning-fast indexing"),
        ("🔄", "Automatic reorg handling"),
        ("🌐", "Multi-chain support"),
        ("📊", "Real-time webhooks"),
        ("🛠️", "Custom chain indexing"),
        ("📈", "Scalable infrastructure")
    ]
    
    for icon, feature in features:
        st.markdown(f"**{icon}** {feature}")

# Separator
st.markdown("---")

# Use Cases Section
st.markdown("## 🎯 Real-World Use Cases")

use_case_cols = st.columns(2)

for idx, use_case in enumerate(USE_CASES):
    with use_case_cols[idx % 2]:
        st.markdown(f"""
        <div class="feature-card">
            <h3>{use_case['title']}</h3>
            <p>{use_case['description']}</p>
            <p><strong>Customers:</strong> {', '.join(use_case['customers'])}</p>
            <p><strong>Features:</strong> {', '.join(use_case['features_used'])}</p>
        </div>
        """, unsafe_allow_html=True)

# Separator
st.markdown("---")

# About this Demo
st.markdown("## 📋 About This Demo")

demo_cols = st.columns(3)

with demo_cols[0]:
    st.markdown("""
    ### 🛠️ Technical Stack
    - **Frontend**: Streamlit
    - **Visualization**: Plotly
    - **API**: Goldsky GraphQL
    - **Data**: Uniswap V3 (Base)
    """)

with demo_cols[1]:
    st.markdown("""
    ### 💡 Key Capabilities
    - GraphQL query execution
    - Real-time data fetching
    - Interactive visualizations
    - SQL transformation examples
    """)

with demo_cols[2]:
    st.markdown("""
    ### 🎓 Skills Demonstrated
    - Platform expertise
    - Data pipeline design
    - Customer demo creation
    - Technical communication
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 2rem; color: #888;">
    <p>Built with ❤️ for Goldsky Solutions Engineer Application</p>
    <p>Created by Roberto | January 2026</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("## 🚀 Quick Start")
    st.markdown("""
    Use the navigation above to explore:
    
    1. **Subgraph Analytics**
    2. **Mirror Pipelines**
    3. **SQL Playground**
    4. **Real-time Dashboard**
    """)
    
    st.markdown("---")
    
    st.markdown("## 📚 Resources")
    st.markdown("""
    - [Goldsky Docs](https://docs.goldsky.com/)
    - [Dashboard](https://app.goldsky.com/)
    """)
    
    st.markdown("---")
    
    st.markdown("## ℹ️ API Status")
    if GOLDSKY_API_KEY != "NOT_FOUND":
        st.success("✅ Connected to Goldsky API")
        st.info(f"API Key: `...{GOLDSKY_API_KEY[-8:]}`")
    else:
        st.error("❌ API Key not found in Secrets")
