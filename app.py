import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime

# --- 1. CONFIGURACIÓN ---
st.set_page_config(
    page_title="Goldsky Custom Subgraph Lab | Roberto",
    page_icon="☀️",
    layout="wide"
)

# --- 2. LÓGICA DE TU SUBGRAPH ESPECÍFICO ---
# Tu URL proporcionada
MY_GOLDSKY_ENDPOINT = "https://api.goldsky.com/api/public/project_cmkljro9cflkv01wh7po6an10/subgraphs/mysubgraph/1.0.0/gn"

def fetch_my_subgraph_data():
    # NOTA: Ajusta esta consulta GraphQL según las entidades reales de tu subgraph
    # Ejemplo genérico: consultamos los primeros 5 elementos de la primera entidad
    query = """
    {
      _meta {
        block {
          number
          hash
        }
        deployment
      }
      # Reemplaza 'pools' o 'transfers' por el nombre de tu entidad real
      # pools(first: 5) { 
      #   id 
      # }
    }
    """
    try:
        r = requests.post(MY_GOLDSKY_ENDPOINT, json={'query': query}, timeout=8)
        if r.status_code == 200:
            res = r.json()
            return res.get('data', {}), "LIVE_PRODUCTION", r.elapsed.total_seconds() * 1000
    except Exception as e:
        return None, f"ERROR: {str(e)}", 0
    return None, "NO_DATA", 0

# --- 3. ESTILOS GOLDSKY ---
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1E2127 0%, #F7931A 100%);
        padding: 2.5rem; border-radius: 12px; color: white; margin-bottom: 2rem;
    }
    .status-box {
        padding: 15px; border-radius: 8px; border: 1px solid #444; background: #1E2127;
    }
</style>
""", unsafe_allow_html=True)

# --- 4. HEADER ESTRATÉGICO ---
st.markdown(f"""
<div class="main-header">
    <h1>☀️ Goldsky Solutions Engineering Demo</h1>
    <p><b>Candidate:</b> Roberto Fajardo Duro (Orwee Squad) | <b>Status:</b> Live Subgraph Integration</p>
</div>
""", unsafe_allow_html=True)

# --- 5. PANEL DE CONTROL Y DIAGNÓSTICO ---
st.subheader("📡 Subgraph Health Monitor")
data, status_code, latency = fetch_my_subgraph_data()

col_status, col_lat, col_meta = st.columns(3)

with col_status:
    if data:
        st.success(f"Endpoint: {status_code}")
    else:
        st.error(f"Endpoint: {status_code}")

with col_lat:
    st.metric("Latency", f"{latency:.0f} ms" if latency > 0 else "N/A")

with col_meta:
    if data and '_meta' in data:
        block_num = data['_meta']['block']['number']
        st.metric("Last Indexed Block", block_num)

st.divider()

# --- 6. DEMOSTRACIÓN DE CAPACIDADES (SOLUTIONS ENGINEER) ---
st.markdown("## 🛠️ Technical Implementation Details")

c1, c2 = st.columns([2, 1])

with c1:
    st.markdown("### Why this Subgraph matters")
    st.write("""
    Esta demo no utiliza datos estáticos. Está conectada a un **Goldsky Subgraph personalizado** que yo mismo he desplegado. Como parte de la propuesta de **Strategic Engineering Partnership**, 
    demuestro mi capacidad para:
    """)
    st.markdown(f"""
    - **Custom Indexing:** Gestión de esquemas complejos y mappings en AssemblyScript. [cite: 13, 22]
    - **Architecture:** Integración de este flujo en pipelines de datos de alto rendimiento. [cite: 13, 42]
    - **Real-time API:** Consumo directo mediante GraphQL para aplicaciones descentralizadas. [cite: 23]
    """)
    
    st.info(f"**Target URL:** `{MY_GOLDSKY_ENDPOINT}`")

with c2:
    st.markdown("### 🔍 Raw Query Sandbox")
    st.code(f"""
# GraphQL Query used:
query {{
  _meta {{
    block {{ number }}
  }}
}}
    """, language="graphql")

# --- 7. FOOTER ---
st.markdown("---")
st.markdown(f"<div style='text-align: center; color: #888;'>Roberto Fajardo Duro | Co-Founder at Orwee | {datetime.now().year}</div>", unsafe_allow_html=True)
