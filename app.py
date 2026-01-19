"""
Goldsky Solutions Engineer Demo Dashboard
Technical demonstration with API fallback and real-time visualization.

Author: Roberto (Solutions Engineer Candidate)
"""

import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime

# --- 1. CONFIGURACIÓN ---
st.set_page_config(
    page_title="Goldsky Technical Demo | Roberto",
    page_icon="☀️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. GESTIÓN DE SECRETS ---
try:
    GOLDSKY_API_KEY = st.secrets["GOLDSKY_API_KEY"]
except Exception:
    GOLDSKY_API_KEY = "DEMO_KEY_FALLBACK"

# --- 3. DATOS DE PRUEBA (MOCK DATA) ---
# Usados si la API falla para no dejar el dashboard vacío
MOCK_POOLS = [
    {"token0": {"symbol": "WETH"}, "token1": {"symbol": "USDC"}, "totalValueLockedUSD": "45200000", "volumeUSD": "125000000", "txCount": "15400"},
    {"token0": {"symbol": "cbBTC"}, "token1": {"symbol": "WETH"}, "totalValueLockedUSD": "38100000", "volumeUSD": "85000000", "txCount": "8200"},
    {"token0": {"symbol": "USDC"}, "token1": {"symbol": "AERO"}, "totalValueLockedUSD": "12500000", "volumeUSD": "45000000", "txCount": "25000"},
    {"token0": {"symbol": "WETH"}, "token1": {"symbol": "DAI"}, "totalValueLockedUSD": "8200000", "volumeUSD": "12000000", "txCount": "4100"}
]

# --- 4. LÓGICA DE CONEXIÓN API ---
def fetch_goldsky_data():
    url = "https://api.goldsky.com/api/public/project_clqzj9f8y000001w6f7g7h8i9/subgraphs/uniswap-v3-base/1.0.0/gn"
    query = """
    {
      pools(first: 5, orderBy: totalValueLockedUSD, orderDirection: desc) {
        token0 { symbol }
        token1 { symbol }
        totalValueLockedUSD
        volumeUSD
        txCount
      }
    }
    """
    headers = {"Authorization": f"Bearer {GOLDSKY_API_KEY}"}
    
    try:
        r = requests.post(url, json={'query': query}, headers=headers, timeout=5)
        if r.status_code == 200 and 'data' in r.json():
            return r.json()['data']['pools'], "LIVE", r.elapsed.total_seconds() * 1000
    except:
        pass
    return MOCK_POOLS, "MOCK/DEMO", 0

# --- 5. CUSTOM CSS ---
st.markdown("""
<style>
    :root { --primary: #F7931A; }
    .main-header {
        background: linear-gradient(135deg, #F7931A 0%, #FF6B00 100%);
        padding: 2.5rem; border-radius: 12px; margin-bottom: 2rem; color: white;
        box-shadow: 0 4px 15px rgba(247, 147, 26, 0.3);
    }
    .feature-card {
        background: rgba(30, 33, 39, 0.8); padding: 1.5rem; border-radius: 10px;
        border-left: 5px solid var(--primary); margin: 10px 0; height: 100%;
    }
    .stMetric { background: #1E2127; padding: 15px; border-radius: 10px; border: 1px solid #333; }
</style>
""", unsafe_allow_html=True)

# --- 6. HEADER ---
st.markdown("""
<div class="main-header">
    <h1>☀️ Goldsky Platform Technical Demo</h1>
    <p>Solutions Engineer Assessment | Real-Time Data Pipeline & API Architecture</p>
</div>
""", unsafe_allow_html=True)

# --- 7. REAL-TIME DASHBOARD (SECCIÓN PRIORITARIA) ---
st.markdown("## 📊 API Performance & Live Analytics")

raw_data, data_mode, latency = fetch_goldsky_data()

# Mensaje de advertencia si estamos en modo Demo/Prueba
if data_mode == "MOCK/DEMO":
    st.warning("⚠️ **Nota de Demo:** La conexión con la API en vivo puede ser inestable debido a límites de rate del entorno de prueba. Mostrando datos técnicos de respaldo (Mock Data) para visualización.")
else:
    st.success(f"📡 **Live Feed:** Conectado exitosamente al indexador de Goldsky (Latencia: {latency:.0f}ms).")

# Procesamiento de Datos
df = pd.DataFrame([
    {
        "Pool": f"{p['token0']['symbol']}/{p['token1']['symbol']}",
        "TVL ($)": float(p['totalValueLockedUSD']),
        "Volume ($)": float(p['volumeUSD']),
        "Txs": int(p['txCount'])
    } for p in raw_data
])

# Métricas
m1, m2, m3, m4 = st.columns(4)
m1.metric("Data Source", data_mode)
m2.metric("Network", "Base Mainnet", "Goldsky Index")
m3.metric("Top Pool TVL", f"${df['TVL ($)'].max()/1e6:.1f}M")
m4.metric("Status", "Operational")

# Visualización
c1, c2 = st.columns(2)
with c1:
    fig1 = px.bar(df, x="Pool", y="TVL ($)", title="Liquidez por Pool (TVL)", template="plotly_dark", color_discrete_sequence=['#F7931A'])
    st.plotly_chart(fig1, use_container_width=True)
with c2:
    fig2 = px.scatter(df, x="TVL ($)", y="Volume ($)", size="Txs", color="Pool", title="Volumen vs Liquidez (Analítica de Subgraph)", template="plotly_dark")
    st.plotly_chart(fig2, use_container_width=True)

st.divider()

# --- 8. CAPACIDADES TÉCNICAS ---
col_text, col_img = st.columns([2, 1])

with col_text:
    st.markdown("## 👋 Technical Expertise")
    st.markdown("""
    Esta implementación demuestra la orquestación de datos mediante **Goldsky Subgraphs**. 
    
    A diferencia de los nodos RPC, mi enfoque utiliza el indexador de Goldsky para garantizar:
    - **Query Efficiency**: Payload reducido mediante selección granular de campos en GraphQL.
    - **Infrastructure Sinks**: Capacidad de derivar estos datos hacia Mirror Pipelines (Postgres/S3).
    - **Reorg Safety**: Filtrado automático de bloques no finalizados.
    """)
    
    with st.expander("Ver Especificación Técnica de la Consulta"):
        st.code("""
        query {
          pools(first: 5, orderBy: totalValueLockedUSD, orderDirection: desc) {
            token0 { symbol }
            token1 { symbol }
            totalValueLockedUSD
            volumeUSD
            txCount
          }
        }""", language="graphql")

with col_img:
    st.markdown("### 🎯 Key Engineering Features")
    for icon, text in [("⚡", "Sub-second indexing"), ("🔄", "Auto-reorg handling"), ("🌐", "130+ Chains"), ("🛠️", "Custom SQL Sinks")]:
        st.write(f"{icon} **{text}**")

st.divider()

# --- 9. USE CASES ---
st.markdown("## 🎯 Real-World Use Cases")
uc1, uc2 = st.columns(2)
with uc1:
    st.markdown('<div class="feature-card"><h3>🏦 DeFi Institutional Tracking</h3><p>Streaming de liquidez para protocolos de lending. Tech: Mirror Pipelines + SQL.</p></div>', unsafe_allow_html=True)
with uc2:
    st.markdown('<div class="feature-card"><h3>🎮 Web3 Gaming</h3><p>Indexación de activos NFT y logros on-chain en subnets personalizadas.</p></div>', unsafe_allow_html=True)

# --- 10. FOOTER ---
st.markdown("---")
st.markdown(f"<div style='text-align: center; color: #888;'>Roberto | Solutions Engineer Candidate | {datetime.now().year}</div>", unsafe_allow_html=True)

# --- 11. SIDEBAR ---
with st.sidebar:
    st.image("https://goldsky.com/wp-content/uploads/2023/10/goldsky_logo_white.png", width=160)
    st.markdown("### ℹ️ Diagnostic")
    if data_mode == "LIVE":
        st.success("✅ Connected to API")
    else:
        st.warning("⚠️ Running Fallback Data")
    
    st.info(f"API Key Active: `...{GOLDSKY_API_KEY[-6:]}`")
    
    st.divider()
    st.markdown("### 📚 Resources")
    st.markdown("- [Docs](https://docs.goldsky.com/)\n- [Dashboard](https://app.goldsky.com/)")
