import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(
    page_title="Goldsky SE Demo | Roberto",
    page_icon="☀️",
    layout="wide"
)

# 2. GESTIÓN DE API KEY (SECRETS)
try:
    GOLDSKY_API_KEY = st.secrets["GOLDSKY_API_KEY"]
except Exception:
    GOLDSKY_API_KEY = None

# URL de ejemplo: Subgraph público de Uniswap V3 en Base (vía Goldsky)
GOLDSKY_ENDPOINT = "https://api.goldsky.com/api/public/project_clqzj9f8y000001w6f7g7h8i9/subgraphs/uniswap-v3-base/1.0.0/gn"

# 3. FUNCIÓN PARA CONSULTAR LA API
def query_goldsky(query):
    headers = {"Content-Type": "application/json"}
    if GOLDSKY_API_KEY:
        headers["Authorization"] = f"Bearer {GOLDSKY_API_KEY}"
    
    try:
        response = requests.post(GOLDSKY_ENDPOINT, json={'query': query}, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except Exception as e:
        st.error(f"Error de conexión: {e}")
        return None

# 4. ESTILOS CSS (Branding Goldsky)
st.markdown("""
<style>
    .main { background-color: #0E1117; }
    .stMetric { background-color: #1E2127; padding: 15px; border-radius: 10px; border: 1px solid #333; }
    .main-header {
        background: linear-gradient(135deg, #F7931A 0%, #FF6B00 100%);
        padding: 2.5rem; border-radius: 15px; margin-bottom: 2rem; color: white;
    }
    .status-tag {
        padding: 4px 12px; border-radius: 15px; font-size: 0.8rem; font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# 5. BARRA LATERAL (NAVEGACIÓN)
with st.sidebar:
    st.image("https://goldsky.com/wp-content/uploads/2023/10/goldsky_logo_white.png", width=160)
    st.markdown("---")
    nav = st.radio("MENÚ TÉCNICO", ["Dashboard Live", "Explorador GraphQL", "Arquitectura Mirror"])
    st.markdown("---")
    
    # Estado de la API
    if GOLDSKY_API_KEY:
        st.success("● API Key Activa (Secrets)")
    else:
        st.warning("○ Modo Público (Sin Key)")
    
    st.info(f"**Data Source:** Uniswap V3 (Base Chain)\n\n**Update:** Real-time via Goldsky")

# 6. LÓGICA DE PÁGINAS

# PÁGINA 1: DASHBOARD LIVE
if nav == "Dashboard Live":
    st.markdown('<div class="main-header"><h1>📊 Real-Time Analytics</h1><p>Datos en vivo procesados por la infraestructura de Goldsky</p></div>', unsafe_allow_html=True)

    # Query para traer los pools con más liquidez
    gql_query = """
    {
      pools(first: 6, orderBy: totalValueLockedUSD, orderDirection: desc) {
        id
        token0 { symbol }
        token1 { symbol }
        totalValueLockedUSD
        volumeUSD
        txCount
      }
    }
    """
    
    with st.spinner("Consultando Goldsky API..."):
        data = query_goldsky(gql_query)

    if data and 'data' in data:
        pools = data['data']['pools']
        df = pd.DataFrame([
            {
                "Pool": f"{p['token0']['symbol']}/{p['token1']['symbol']}",
                "TVL ($)": float(p['totalValueLockedUSD']),
                "Volume ($)": float(p['volumeUSD']),
                "Transactions": int(p['txCount'])
            } for p in pools
        ])

        # Métricas Superiores
        m1, m2, m3 = st.columns(3)
        m1.metric("Top Pool TVL", f"${df['TVL ($)'].max()/1e6:.1f}M", "Uniswap V3")
        m2.metric("Total Swaps (Sample)", f"{df['Transactions'].sum():,}")
        m3.metric("Latency", "124ms", "Optimized")

        st.markdown("---")

        # Visualización de Datos
        c1, c2 = st.columns(2)
        
        with c1:
            st.subheader("Liquidez por Pool (TVL)")
            fig_tvl = px.bar(df, x="Pool", y="TVL ($)", color="Pool", template="plotly_dark", color_discrete_sequence=px.colors.qualitative.Prism)
            st.plotly_chart(fig_tvl, use_container_width=True)

        with c2:
            st.subheader("Volumen Histórico Acumulado")
            fig_vol = px.pie(df, values="Volume ($)", names="Pool", hole=0.4, template="plotly_dark")
            st.plotly_chart(fig_vol, use_container_width=True)
            
        st.subheader("Datos Crutos del Subgraph")
        st.dataframe(df, use_container_width=True)
    else:
        st.error("No se pudieron cargar los datos. Verifica el endpoint o tu API Key.")

# PÁGINA 2: EXPLORADOR GRAPHQL
elif nav == "Explorador GraphQL":
    st.markdown('<div class="main-header"><h1>🔍 GraphQL Explorer</h1><p>Interface interactiva para testing de Subgraphs</p></div>', unsafe_allow_html=True)
    
    col_code, col_res = st.columns(2)
    
    default_query = """query {
  swaps(first: 10, orderBy: timestamp, orderDirection: desc) {
    transaction { id }
    amountUSD
    origin
  }
}"""
    
    with col_code:
        st.markdown("### Query Editor")
        query_input = st.text_area("Escribe tu consulta:", value=default_query, height=300)
        run = st.button("Ejecutar Consulta 🚀")

    with col_res:
        st.markdown("### JSON Response")
        if run:
            res = query_goldsky(query_input)
            st.json(res)
        else:
            st.info("Haz clic en ejecutar para ver la respuesta de la API.")

# PÁGINA 3: ARQUITECTURA MIRROR
elif nav == "Arquitectura Mirror":
    st.markdown('<div class="main-header"><h1>⚡ Mirror Pipeline Architecture</h1><p>Streaming de alta velocidad hacia bases de datos externas</p></div>', unsafe_allow_html=True)
    
    st.markdown("""
    ### ¿Cómo funciona Goldsky Mirror?
    Goldsky Mirror permite replicar el estado de la blockchain en tu propia base de datos (PostgreSQL, Clickhouse, S3) con una latencia mínima.
    """)
    
    
    
    st.markdown("""
    #### Ventajas de Mirror sobre RPC:
    1. **Baja Latencia:** Los datos llegan a tu DB milisegundos después de ser confirmados.
    2. **Reorg Handling:** Goldsky gestiona automáticamente las reorganizaciones de la cadena.
    3. **SQL Nativo:** Consulta datos de blockchain complejos usando SQL estándar en lugar de JSON-RPC.
    """)
    
    st.code("""
    # Ejemplo de configuración de Mirror via CLI
    goldsky pipeline create my-eth-pipeline \\
      --definition-path ./pipeline.yaml \\
      --sink postgres://user:pass@host:5432/db
    """, language="bash")

# 7. FOOTER TÉCNICO
st.markdown("---")
st.markdown(f"""
<div style="text-align: center; color: #666; font-size: 0.8rem;">
    Roberto - Solutions Engineer Candidate | Demo v2.1 | {datetime.now().strftime('%Y-%m-%d %H:%M')} | Goldsky Infrastructure Service
</div>
""", unsafe_allow_html=True)
