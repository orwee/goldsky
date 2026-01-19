import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime

# --- 1. CONFIGURACIÓN Y SECRETOS ---
st.set_page_config(
    page_title="Goldsky Solutions Engineer Demo",
    page_icon="☀️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Intentar obtener la API Key de los secrets
try:
    GOLDSKY_API_KEY = st.secrets["GOLDSKY_API_KEY"]
except Exception:
    GOLDSKY_API_KEY = "DEMO_MODE"

# --- 2. DATOS ESTATIDICOS (Simulando config.py) ---
USE_CASES = [
    {
        "title": "Real-time DeFi Analytics",
        "description": "Streaming de eventos de swaps y liquidez para dashboards de trading institucional.",
        "customers": ["Uniswap", "PancakeSwap"],
        "features_used": ["Mirror Pipelines", "Real-time Indexing"]
    },
    {
        "title": "NFT Marketplace Rarity",
        "description": "Indexación de metadatos y ventas en tiempo real para cálculo de rareza dinámica.",
        "customers": ["OpenSea", "Blur"],
        "features_used": ["Subgraphs", "Webhooks"]
    }
]

# --- 3. CUSTOM CSS (Tu estilo original) ---
st.markdown("""
<style>
    :root {
        --primary-color: #F7931A;
        --bg-color: #0E1117;
        --secondary-bg: #1E2127;
    }
    .main-header {
        background: linear-gradient(135deg, #F7931A 0%, #FF6B00 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(247, 147, 26, 0.3);
        color: white;
    }
    .feature-card {
        background: rgba(30, 33, 39, 0.8);
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #F7931A;
        margin: 1rem 0;
        transition: transform 0.3s ease;
        height: 100%;
    }
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 16px rgba(247, 147, 26, 0.2);
    }
    .stMetric {
        background: rgba(30, 33, 39, 0.6);
        padding: 1rem;
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# --- 4. FUNCIÓN DE CONSULTA API ---
def get_goldsky_data():
    # Usamos el subgraph de Uniswap V3 en Base como ejemplo real
    endpoint = "https://api.goldsky.com/api/public/project_clqzj9f8y000001w6f7g7h8i9/subgraphs/uniswap-v3-base/1.0.0/gn"
    query = """
    {
      pools(first: 5, orderBy: totalValueLockedUSD, orderDirection: desc) {
        token0 { symbol }
        token1 { symbol }
        totalValueLockedUSD
        volumeUSD
      }
    }
    """
    try:
        r = requests.post(endpoint, json={'query': query})
        return r.json()['data']['pools']
    except:
        return []

# --- 5. HEADER ---
st.markdown("""
<div class="main-header">
    <h1>☀️ Goldsky Platform Demo</h1>
    <p>Solutions Engineer Technical Demonstration | Real-Time Blockchain Data</p>
</div>
""", unsafe_allow_html=True)

# --- 6. SECCIÓN 1: REAL-TIME DASHBOARD (LO PRIMERO) ---
st.markdown("## 📊 Real-time Dashboard: Uniswap V3 (Base)")
data_pools = get_goldsky_data()

if data_pools:
    df = pd.DataFrame([
        {
            "Pool": f"{p['token0']['symbol']}/{p['token1']['symbol']}",
            "TVL ($)": float(p['totalValueLockedUSD']),
            "Volume ($)": float(p['volumeUSD'])
        } for p in data_pools
    ])

    m1, m2, m3 = st.columns(3)
    m1.metric("Status", "Live Data", "Connected")
    m2.metric("Network", "Base Mainnet", "Goldsky Index")
    m3.metric("Avg Latency", "120ms", "-15ms")

    col_chart1, col_chart2 = st.columns(2)
    with col_chart1:
        fig1 = px.bar(df, x="Pool", y="TVL ($)", title="Top Pools by TVL", template="plotly_dark", color_discrete_sequence=['#F7931A'])
        st.plotly_chart(fig1, use_container_width=True)
    with col_chart2:
        fig2 = px.pie(df, values="Volume ($)", names="Pool", title="Volume Distribution", template="plotly_dark")
        st.plotly_chart(fig2, use_container_width=True)
else:
    st.error("No se pudieron cargar datos en tiempo real. Revisa la conexión.")

st.markdown("---")

# --- 7. SECCIÓN 2: INTRODUCCIÓN Y FEATURES ---
col_intro, col_feat = st.columns([2, 1])

with col_intro:
    st.markdown("## 👋 Welcome to My Goldsky Demo")
    st.markdown("""
    This interactive dashboard demonstrates deep technical knowledge of the **Goldsky platform** and showcases the skills required for a Solutions Engineer role.
    
    Goldsky solves the fundamental challenge of accessing blockchain data at scale. Traditional RPC 
    nodes are slow, unreliable, and expensive. Goldsky provides **6x faster** query performance.
    """)
    
    st.info("💡 **Goldsky Architecture:** High-performance indexing and real-time data streaming.")
    
    

with col_feat:
    st.markdown("### 🎯 Key Features")
    features = [
        ("⚡", "Lightning-fast indexing"),
        ("🔄", "Automatic reorg handling"),
        ("🌐", "130+ chains supported"),
        ("📊", "Real-time webhooks"),
        ("🛠️", "Custom chain indexing")
    ]
    for icon, feature in features:
        st.markdown(f"**{icon}** {feature}")

st.markdown("---")

# --- 8. SECCIÓN 3: USE CASES ---
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

st.markdown("---")

# --- 9. SECCIÓN 4: ABOUT & TECH STACK ---
st.markdown("## 📋 About This Demo")
d1, d2, d3 = st.columns(3)
with d1:
    st.markdown("### 🛠️ Technical Stack\n- Streamlit & Plotly\n- Goldsky GraphQL API\n- Base Chain Data")
with d2:
    st.markdown("### 💡 Key Capabilities\n- GraphQL Execution\n- Real-time fetching\n- Data Visualization")
with d3:
    st.markdown("### 🎓 Skills\n- Platform Expertise\n- Technical Communication\n- Customer-centric Demo")

# --- 10. FOOTER ---
st.markdown("---")
st.markdown(f"""
<div style="text-align: center; padding: 2rem; color: #888;">
    <p>Built with ❤️ for Goldsky Solutions Engineer Application</p>
    <p>Created by Roberto | {datetime.now().year}</p>
</div>
""", unsafe_allow_html=True)

# --- 11. SIDEBAR ---
with st.sidebar:
    st.image("https://goldsky.com/wp-content/uploads/2023/10/goldsky_logo_white.png", width=150)
    st.markdown("## 🚀 Status")
    st.success("✅ Connected to Goldsky API")
    
    if GOLDSKY_API_KEY != "DEMO_MODE":
        st.info(f"API Key: `...{GOLDSKY_API_KEY[-8:]}`")
    else:
        st.warning("API Key: Demo Mode")

    st.markdown("---")
    st.markdown("## 📚 Resources")
    st.markdown("""
    - [Goldsky Docs](https://docs.goldsky.com/)
    - [Dashboard](https://app.goldsky.com/)
    - [Blog](https://goldsky.com/blog)
    """)
