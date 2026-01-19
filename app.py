import streamlit as st
import pandas as pd

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(
    page_title="Goldsky Solutions Engineer Demo",
    page_icon="☀️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. INTENTAR LEER LA API KEY DESDE SECRETS
# Si no existe, mostrará un error amigable
try:
    GOLDSKY_API_KEY = st.secrets["GOLDSKY_API_KEY"]
    api_connected = True
except Exception:
    api_connected = False

# 3. DATOS ESTATIDICOS
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
    }
]

# 4. ESTILOS CSS
st.markdown(f"""
<style>
    .main-header {{
        background: linear-gradient(135deg, {THEME['primary']} 0%, {THEME['accent']} 100%);
        padding: 2.5rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        color: white;
    }}
    .feature-card {{
        background: #1E2127;
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 5px solid {THEME['primary']};
        margin-bottom: 1rem;
        height: 100%;
    }}
</style>
""", unsafe_allow_html=True)

# 5. BARRA LATERAL
with st.sidebar:
    st.image("https://goldsky.com/wp-content/uploads/2023/10/goldsky_logo_white.png", width=150)
    st.markdown("### 📊 Estado de Conexión")
    
    if api_connected:
        st.success("✅ API Key cargada desde Secrets")
        st.caption(f"Key activa: `...{GOLDSKY_API_KEY[-6:]}`")
    else:
        st.error("❌ API Key no encontrada")
        st.info("Configura `GOLDSKY_API_KEY` en tus Secrets de Streamlit.")

    st.divider()
    st.markdown("### 🚀 Recursos")
    st.markdown("- [Documentación Goldsky](https://docs.goldsky.com/)")
    st.markdown("- [Explorador de Subgraphs](https://app.goldsky.com/)")

# 6. CONTENIDO PRINCIPAL
st.markdown("""
<div class="main-header">
    <h1>☀️ Goldsky Platform Demo</h1>
    <p style="font-size: 1.2rem; opacity: 0.9;">Solutions Engineer Technical Demonstration | Candidate: Roberto</p>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([2, 1], gap="large")

with col1:
    st.markdown("## 👋 Bienvenido")
    st.markdown("""
    Este dashboard demuestra la capacidad de **Goldsky** para transformar datos crudos de blockchain en 
    información procesable en tiempo real. 
    
    Como candidato a **Solutions Engineer**, mi enfoque es resolver los cuellos de botella de datos 
    utilizando pipelines de alto rendimiento.
    """)
    
    st.image("https://img.freepik.com/free-vector/blockchain-technology-concept-background_1017-14227.jpg?size=626&ext=jpg", use_container_width=True)

with col2:
    st.markdown("### ⚡ Capacidades Clave")
    features = [
        "6x más rápido que RPCs",
        "Reorg handling automático",
        "Soporte para 130+ cadenas",
        "Ecosistema multi-cloud"
    ]
    for f in features:
        st.write(f"✅ {f}")

st.markdown("---")

# 7. CASOS DE USO
st.markdown("## 🎯 Casos de Uso")
cols = st.columns(2)
for idx, use_case in enumerate(USE_CASES):
    with cols[idx % 2]:
        st.markdown(f"""
        <div class="feature-card">
            <h3 style="color: {THEME['primary']}; margin-top:0;">{use_case['title']}</h3>
            <p>{use_case['description']}</p>
            <p><b>Clientes:</b> {', '.join(use_case['customers'])}</p>
        </div>
        """, unsafe_allow_html=True)

# 8. PLAYGROUND TÉCNICO (Solo si hay API Key)
if api_connected:
    st.markdown("---")
    st.markdown("## 💾 Sandbox Técnico")
    tab1, tab2 = st.tabs(["GraphQL", "SQL"])
    
    with tab1:
        st.code("query { pools(first: 5) { id token0 { symbol } } }", language="graphql")
        if st.button("Probar Query"):
            st.toast("Conectando con Goldsky API...")
            # Aquí se usaría GOLDSKY_API_KEY para el request real
    
    with tab2:
        st.code("SELECT * FROM goldsky.mirror_pipeline WHERE status = 'active';", language="sql")

# Footer
st.markdown("---")
st.markdown("<div style='text-align: center; color: #888;'>Roberto | Solutions Engineer Candidate 2026</div>", unsafe_allow_html=True)
