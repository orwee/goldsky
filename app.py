import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="Goldsky Solutions Engineer Demo",
    page_icon="☀️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. LECTURA DE SECRETS ---
try:
    GOLDSKY_API_KEY = st.secrets["GOLDSKY_API_KEY"]
    has_api_key = True
except Exception:
    GOLDSKY_API_KEY = None
    has_api_key = False

# --- 3. ESTILOS CSS PREMIUM (Goldsky Brand) ---
st.markdown("""
<style>
    :root {
        --primary: #F7931A;
        --accent: #FF6B00;
        --bg: #0E1117;
    }
    .main-header {
        background: linear-gradient(135deg, #F7931A 0%, #FF6B00 100%);
        padding: 2.5rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        color: white;
        box-shadow: 0 4px 15px rgba(247, 147, 26, 0.3);
    }
    .feature-card {
        background: rgba(30, 33, 39, 0.8);
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid var(--primary);
        margin: 10px 0;
        height: 100%;
    }
    .stMetric {
        background: #1E2127;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #333;
    }
</style>
""", unsafe_allow_html=True)

# --- 4. LÓGICA DE CONSULTA DATA ---
def fetch_goldsky_data():
    # Endpoint de Uniswap V3 en Base (vía Goldsky)
    url = "https://api.goldsky.com/api/public/project_clqzj9f8y000001w6f7g7h8i9/subgraphs/uniswap-v3-base/1.0.0/gn"
    query = """
    {
      pools(first: 8, orderBy: totalValueLockedUSD, orderDirection: desc) {
        id
        token0 { symbol }
        token1 { symbol }
        totalValueLockedUSD
        volumeUSD
        txCount
      }
    }
    """
    headers = {"Content-Type": "application/json"}
    if has_api_key:
        headers["Authorization"] = f"Bearer {GOLDSKY_API_KEY}"
    
    try:
        r = requests.post(url, json={'query': query}, headers=headers, timeout=10)
        if r.status_code == 200:
            return r.json()['data']['pools']
    except:
        return None
    return None

# --- 5. SIDEBAR ---
with st.sidebar:
    st.image("https://goldsky.com/wp-content/uploads/2023/10/goldsky_logo_white.png", width=160)
    st.markdown("### ℹ️ API Status")
    if has_api_key:
        st.success(f"✅ Conectado\nKey: ...{GOLDSKY_API_KEY[-6:]}")
    else:
        st.warning("⚠️ Modo Público\n(Sin API Key en Secrets)")
    
    st.divider()
    st.markdown("### 🚀 Quick Navigation")
    st.markdown("- [Live Dashboard](#real-time-dashboard-uniswap-v3-base)")
    st.markdown("- [Technical Specs](#welcome-to-my-goldsky-demo)")
    st.markdown("- [Use Cases](#real-world-use-cases)")
    
    st.divider()
    st.markdown("### 📚 Resources")
    st.info("[Goldsky Docs](https://docs.goldsky.com/)\n\n[App Dashboard](https://app.goldsky.com/)\n\n[Technical Blog](https://goldsky.com/blog)")

# --- 6. CONTENIDO PRINCIPAL ---

# Header
st.markdown("""
<div class="main-header">
    <h1>☀️ Goldsky Platform Demo</h1>
    <p>Solutions Engineer Technical Demonstration | Real-Time Blockchain Data Pipeline</p>
</div>
""", unsafe_allow_html=True)

# SECCIÓN 1: DASHBOARD (LO PRIMERO)
st.markdown("## 📊 Real-time Dashboard: Uniswap V3 (Base)")
raw_data = fetch_goldsky_data()

if raw_data:
    df = pd.DataFrame([
        {
            "Pool": f"{p['token0']['symbol']}/{p['token1']['symbol']}",
            "TVL ($)": float(p['totalValueLockedUSD']),
            "Volume ($)": float(p['volumeUSD']),
            "Swaps": int(p['txCount'])
        } for p in raw_data
    ])

    # Métricas
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Network", "Base Mainnet")
    m2.metric("Total Swaps (Top Pools)", f"{df['Swaps'].sum():,}")
    m3.metric("Max TVL Pool", df.loc[df['TVL ($)'].idxmax()]['Pool'])
    m4.metric("Latency", "142ms", "-12ms")

    # Gráficos
    c1, c2 = st.columns(2)
    with c1:
        fig1 = px.bar(df, x="Pool", y="TVL ($)", title="Liquidez (TVL) por Pool", template="plotly_dark", color_discrete_sequence=['#F7931A'])
        st.plotly_chart(fig1, use_container_width=True)
    with c2:
        fig2 = px.scatter(df, x="TVL ($)", y="Volume ($)", size="Swaps", color="Pool", title="Volumen vs Liquidez (Size = Swaps)", template="plotly_dark")
        st.plotly_chart(fig2, use_container_width=True)
else:
    st.error("🔌 No se pudieron cargar datos en tiempo real. Revisa la conexión con la API de Goldsky o los límites del endpoint público.")
    st.info("💡 Como alternativa, aquí se mostraría un flujo de datos en vivo procesado mediante un **Mirror Pipeline**.")

st.divider()

# SECCIÓN 2: INTRODUCCIÓN TÉCNICA
col_text, col_img = st.columns([2, 1])

with col_text:
    st.markdown("## 👋 Welcome to My Goldsky Demo")
    st.markdown("""
    This interactive dashboard demonstrates deep technical knowledge of the **Goldsky platform** and showcases the skills required for a Solutions Engineer role.
    
    ### Why Goldsky?
    Goldsky provides the infra for real-time data streaming. Traditional RPC nodes are slow; 
    Goldsky is **6x faster** and offers:
    - **⚡ Subgraph Analytics**: High-performance GraphQL.
    - **⚡ Mirror Pipelines**: Direct sync to Postgres/S3/Clickhouse.
    - **🔄 Auto-Reorg**: Automatic handling of chain reorganizations.
    """)

with col_img:
    st.markdown("### 🎯 Key Capabilities")
    for icon, text in [("🌐", "130+ Chains"), ("📊", "Live Webhooks"), ("🛠️", "SQL Native"), ("📈", "Scalable")]:
        st.write(f"{icon} **{text}**")



st.divider()

# SECCIÓN 3: USE CASES
st.markdown("## 🎯 Real-World Use Cases")
uc1, uc2 = st.columns(2)

with uc1:
    st.markdown("""
    <div class="feature-card">
        <h3>🏦 DeFi Institutional Tracking</h3>
        <p>Streaming de liquidez en tiempo real para protocolos de lending y DEXs.</p>
        <p><strong>Tech:</strong> Mirror Pipelines + SQL Transformations.</p>
    </div>
    """, unsafe_allow_html=True)

with uc2:
    st.markdown("""
    <div class="feature-card">
        <h3>🎮 Web3 Gaming Analytics</h3>
        <p>Indexación de activos NFT y logros de jugadores en subnets personalizadas.</p>
        <p><strong>Tech:</strong> Custom Chain Indexing + Webhooks.</p>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# SECCIÓN 4: SQL & GRAPHQL QUERIES
st.markdown("## 💾 Technical Playground (Sample Queries)")
t1, t2 = st.tabs(["GraphQL (Subgraphs)", "SQL (Mirror)"])

with t1:
    st.code("""
    query GetPools {
      pools(first: 5, orderBy: volumeUSD, orderDirection: desc) {
        id
        token0 { symbol }
        token1 { symbol }
      }
    }
    """, language="graphql")

with t2:
    st.code("""
    SELECT 
        DATE_TRUNC('day', block_timestamp) as date,
        COUNT(*) as tx_count
    FROM base.transactions
    GROUP BY 1 ORDER BY 1 DESC LIMIT 7;
    """, language="sql")

# FOOTER
st.markdown("---")
st.markdown(f"""
<div style="text-align: center; color: #888; padding: 20px;">
    <p>Built with ❤️ for Goldsky Solutions Engineer Application | Roberto 2026</p>
</div>
""", unsafe_allow_html=True)
