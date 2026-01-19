import streamlit as st
import pandas as pd
import plotly.express as px

# 1. CONFIGURACIÓN DE PÁGINA (Debe ser lo primero)
st.set_page_config(
    page_title="Goldsky Solutions Engineer Demo",
    page_icon="☀️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. DATOS ESTATIDICOS (Antes en config.py)
THEME = {
    "primary": "#F7931A",
    "secondary": "#1E2127",
    "accent": "#FF6B00"
}

USE_CASES = [
    {
        "title": "DeFi Analytics",
        "description": "Seguimiento en tiempo real de volumen y liquidez en DEXs multichain.",
        "customers": ["Uniswap", "PancakeSwap"],
        "features_used": ["Subgraphs", "Mirror Pipelines"]
    },
    {
        "title": "NFT Marketplaces",
        "description": "Actualizaciones instantáneas de floor price y monitoreo de mints.",
        "customers": ["OpenSea", "Blur"],
        "features_used": ["Webhooks", "Real-time Indexing"]
    },
    {
        "title": "Institutional Reporting",
        "description": "Extracción de datos históricos para cumplimiento y reportes fiscales.",
        "customers": ["Fireblocks", "Chainalysis"],
        "features_used": ["SQL Playground", "Mirror"]
    },
    {
        "title": "Gaming & P2E",
        "description": "Tracking de activos in-game y logros de jugadores on-chain.",
        "customers": ["Axie Infinity", "Immutable"],
        "features_used": ["Custom Chain Indexing"]
    }
]

# 3. BARRA LATERAL (ENTRADA DE CREDENCIALES)
with st.sidebar:
    st.image("https://goldsky.com/wp-content/uploads/2023/10/goldsky_logo_white.png", width=150)
    st.markdown("### 🔐 Autenticación")
    
    # Aquí el usuario ingresa su API Key
    api_key_input = st.text_input(
        "Goldsky API Key", 
        type="password", 
        placeholder="gs_..."
    )
    
    # Campo adicional por si necesitas un password de acceso a la propia App
    app_password = st.text_input(
        "Password de Acceso", 
        type="password"
    )

    st.divider()
    
    if api_key_input:
        st.success("✅ API Key detectada")
    else:
        st.warning("⚠️ Introduce tu API Key para habilitar funciones")

    st.markdown("### 🚀 Navegación")
    st.info("1. Analytics\n2. Mirror Pipelines\n3. SQL Playground\n4. Real-time Dashboard")

# 4. ESTILOS CSS PERSONALIZADOS
st.markdown(f"""
<style>
    .main-header {{
        background: linear-gradient(135deg, {THEME['primary']} 0%, {THEME['accent']} 100%);
        padding: 2.5rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        color: white;
        box-shadow: 0 4px 15px rgba(247, 147, 26, 0.3);
    }}
    .feature-card {{
        background: #1E2127;
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 5px solid {THEME['primary']};
        margin-bottom: 1rem;
        height: 100%;
    }}
    .stMetric {{
        background: rgba(30, 33, 39, 0.6);
        padding: 1rem;
        border-radius: 10px;
    }}
</style>
""", unsafe_allow_html=True)

# 5. CONTENIDO PRINCIPAL
st.markdown("""
<div class="main-header">
    <h1>☀️ Goldsky Platform Demo</h1>
    <p style="font-size: 1.2rem; opacity: 0.9;">Solutions Engineer Technical Demonstration | Candidate: Roberto</p>
</div>
""", unsafe_allow_html=True)

# Sección de Introducción
col1, col2 = st.columns([2, 1], gap="large")

with col1:
    st.markdown("## 👋 Bienvenido a la Demo de Goldsky")
    st.markdown("""
    Esta plataforma demuestra cómo **Goldsky** elimina la complejidad de indexar datos de blockchain. 
    A diferencia de los nodos RPC tradicionales, Goldsky ofrece una infraestructura de alta disponibilidad y baja latencia.
    """)
    
    

    st.markdown("""
    ### ¿Por qué Goldsky?
    - **Rendimiento 6x superior** en consultas complejas.
    - **Uptime del 99.9%** garantizado.
    - **Soporte para 130+ cadenas** incluyendo L2s emergentes.
    """)

with col2:
    st.markdown("### 📊 Estado de Conexión")
    if api_key_input:
        st.metric(label="Status", value="Conectado", delta="API Activa")
        st.caption(f"Usando llave: `...{api_key_input[-6:]}`")
    else:
        st.error("No hay conexión con la API")
        st.info("Por favor, ingresa tu API Key en la barra lateral para ver los datos en vivo.")

st.markdown("---")

# 6. CASOS DE USO DINÁMICOS
st.markdown("## 🎯 Casos de Uso del Mundo Real")
cols = st.columns(2)
for idx, use_case in enumerate(USE_CASES):
    with cols[idx % 2]:
        st.markdown(f"""
        <div class="feature-card">
            <h3 style="color: {THEME['primary']}; margin-top:0;">{use_case['title']}</h3>
            <p>{use_case['description']}</p>
            <p><b>Clientes:</b> {', '.join(use_case['customers'])}</p>
            <p style="font-size: 0.85rem; color: #888;"><b>Tecnología:</b> {', '.join(use_case['features_used'])}</p>
        </div>
        """, unsafe_allow_html=True)

# 7. ÁREA TÉCNICA (Solo visible si hay API Key)
if api_key_input:
    st.markdown("---")
    st.markdown("## 💾 SQL & GraphQL Playground")
    tab1, tab2 = st.tabs(["GraphQL Query", "SQL Mirror Pipeline"])
    
    with tab1:
        st.code("""
query GetLatestSwaps {
  swaps(first: 5, orderBy: timestamp, orderDirection: desc) {
    id
    amount0
    amount1
    symbol
  }
}
        """, language="graphql")
        if st.button("Ejecutar Consulta"):
            st.info("Consultando datos de Uniswap V3 en Base...")
            # Aquí iría tu lógica de requests.post() usando api_key_input
            
    with tab2:
        st.code("""
SELECT 
    block_number,
    transaction_hash,
    from_address,
    value / pow(10, 18) as eth_value
FROM ethereum.traces
WHERE status = 1
LIMIT 10;
        """, language="sql")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #888; padding: 10px;">
    Creado por Roberto para el proceso de selección de Goldsky | 2026
</div>
""", unsafe_allow_html=True)
