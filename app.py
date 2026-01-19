import streamlit as st
import pandas as pd

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(
    page_title="Goldsky Solutions Engineer Demo",
    page_icon="☀️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. CARGA DE SECRETS
try:
    GOLDSKY_API_KEY = st.secrets["GOLDSKY_API_KEY"]
except Exception:
    GOLDSKY_API_KEY = "DEMO_MODE_NO_KEY"

# 3. DATOS Y TEMAS
THEME = {"primary": "#F7931A", "bg": "#0E1117", "secondary": "#1E2127"}

USE_CASES = [
    {
        "title": "Real-time DeFi Dashboard",
        "description": "Streaming de datos de swaps de Uniswap V3 con latencia cero.",
        "customers": ["Uniswap", "PancakeSwap"],
        "features": ["Mirror Pipelines", "Real-time Indexing"]
    },
    {
        "title": "NFT Rarity Engine",
        "description": "Indexación de metadatos y ventas para calcular rareza dinámica.",
        "customers": ["OpenSea", "Blur"],
        "features": ["Subgraphs", "Webhooks"]
    }
]

# 4. CSS PARA ESTILO PREMIUM
st.markdown(f"""
<style>
    .main-header {{
        background: linear-gradient(135deg, #F7931A 0%, #FF6B00 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        color: white;
    }}
    .feature-card {{
        background: #1E2127;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #F7931A;
        margin-bottom: 1rem;
        height: 100%;
    }}
</style>
""", unsafe_allow_html=True)

# 5. BARRA LATERAL (NAVEGACIÓN REAL)
with st.sidebar:
    st.image("https://goldsky.com/wp-content/uploads/2023/10/goldsky_logo_white.png", width=150)
    st.markdown("---")
    
    # Selector de navegación
    menu_option = st.selectbox(
        "🚀 EXPLORAR PLATAFORMA",
        ["🏠 Inicio", "🔍 Subgraph Analytics", "⚡ Mirror Pipelines", "💾 SQL Playground", "📊 Real-time Dashboard"]
    )
    
    st.markdown("---")
    st.markdown("### ℹ️ API Status")
    if GOLDSKY_API_KEY != "DEMO_MODE_NO_KEY":
        st.success(f"✅ API Key: ...{GOLDSKY_API_KEY[-6:]}")
    else:
        st.warning("⚠️ Modo Demo (Sin Key)")

# 6. LÓGICA DE NAVEGACIÓN (Controla qué se muestra)

# --- HEADER (Siempre visible) ---
st.markdown(f"""
<div class="main-header">
    <h1>☀️ Goldsky: {menu_option}</h1>
    <p>Solutions Engineer Technical Demonstration | Roberto 2026</p>
</div>
""", unsafe_allow_html=True)

if menu_option == "🏠 Inicio":
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("## 👋 Bienvenido a la Demo de Goldsky")
        st.markdown("""
        Esta herramienta demuestra cómo Goldsky soluciona el acceso a datos on-chain a escala. 
        Tradicionalmente, indexar datos es lento y costoso; Goldsky lo hace en tiempo real.
        
        ### ¿Qué puedes hacer aquí?
        - **Probar queries GraphQL** en vivo.
        - **Visualizar pipelines** de datos (Mirror).
        - **Transformar datos** mediante SQL.
        """)
        
    with col2:
        st.markdown("### 🎯 Key Features")
        for icon, f in [("⚡", "6x Faster"), ("🔄", "Auto-reorg"), ("🌐", "130+ Chains")]:
            st.write(f"{icon} **{f}**")
            
    st.divider()
    st.markdown("### 🎯 Casos de Uso")
    cols = st.columns(2)
    for i, uc in enumerate(USE_CASES):
        with cols[i % 2]:
            st.markdown(f"""
            <div class="feature-card">
                <h3>{uc['title']}</h3>
                <p>{uc['description']}</p>
                <small><b>Clientes:</b> {', '.join(uc['customers'])}</small>
            </div>
            """, unsafe_allow_html=True)

elif menu_option == "🔍 Subgraph Analytics":
    st.markdown("## 🔍 Consultas GraphQL")
    st.write("Ejecuta consultas sobre subgraphs alojados en la infraestructura de alta disponibilidad de Goldsky.")
    
    query_example = """query {
  pools(first: 5, orderBy: totalValueLockedUSD, orderDirection: desc) {
    id
    token0 { symbol }
    token1 { symbol }
    totalValueLockedUSD
  }
}"""
    st.code(query_example, language="graphql")
    if st.button("Ejecutar Query"):
        st.info("Simulando respuesta de la API de Goldsky...")
        st.json({"data": {"pools": [{"id": "0x123...", "token0": {"symbol": "WETH"}, "token1": {"symbol": "USDC"}, "totalValueLockedUSD": "150000000"}]}})

elif menu_option == "⚡ Mirror Pipelines":
    st.markdown("## ⚡ Mirror Pipelines")
    st.markdown("""
    Mirror permite llevar datos de blockchain directamente a tu base de datos (Postgres, Clickhouse, S3) 
    con una latencia de milisegundos.
    """)
    st.image("https://docs.goldsky.com/img/mirror-architecture.png") # Imagen oficial si existe o similar
    
    st.success("Configuración recomendada para pipelines de alta carga detectada.")

elif menu_option == "💾 SQL Playground":
    st.markdown("## 💾 SQL Transformations")
    st.write("Aplica lógica de negocio a los datos de blockchain antes de que lleguen a tu destino.")
    st.code("""
    SELECT 
        DATE_TRUNC('hour', block_timestamp) as hour,
        sum(value) / 1e18 as total_eth_transferred
    FROM ethereum.traces
    GROUP BY 1 ORDER BY 1 DESC;
    """, language="sql")
    st.table(pd.DataFrame({
        "hour": ["2026-01-19 20:00", "2026-01-19 19:00"],
        "total_eth_transferred": [1450.2, 1280.5]
    }))

elif menu_option == "📊 Real-time Dashboard":
    st.markdown("## 📊 Métricas en Tiempo Real")
    c1, c2, c3 = st.columns(3)
    c1.metric("Blocks Indexed", "18.5M", "+12")
    c2.metric("Avg Latency", "140ms", "-10ms")
    c3.metric("Active Pipelines", "24", "Stable")
    
    st.line_chart(pd.DataFrame({"TPS": [25, 30, 45, 40, 55, 60]}))

# 7. FOOTER
st.markdown("---")
st.markdown("<div style='text-align: center; color: #888;'>Roberto | Solutions Engineer Candidate | 2026</div>", unsafe_allow_html=True)
