import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# Configuración de página
st.set_page_config(page_title="Goldsky Dashboard - mysubgraph", layout="wide")

# 1. Configuración de API y Endpoint
API_KEY = st.secrets["GOLDSKY_API_KEY"]
GOLDSKY_URL = "https://api.goldsky.com/api/public/project_cmkljro9cflkv01wh7po6an10/subgraphs/mysubgraph/1.0.0/gn"

def run_query(query):
    headers = {"Authorization": f"Bearer {API_KEY}"}
    request = requests.post(GOLDSKY_URL, json={'query': query}, headers=headers)
    if request.status_code == 200:
        return request.json()
    else:
        st.error(f"Error en la consulta: {request.status_code}")
        return None

# --- UI: Encabezado y Métricas ---
st.title("🚀 Goldsky Subgraph Monitor")
st.caption(f"Endpoint: {GOLDSKY_URL}")

# Simulación de métricas basadas en tu reporte actual
col1, col2, col3, col4 = st.columns(4)
col1.metric("Bloque Actual", "41,110,043", "Live")
col2.metric("Entidades Totales", "489")
col3.metric("Nuevas (24h)", "230", "+15%")
col4.metric("Latencia API", "70.5ms")

st.divider()

# --- UI: Consultas a Entidades ---
st.subheader("🔍 Explorador de Datos")

# Nota: Como no conozco tu esquema exacto, usaremos un ejemplo genérico. 
# Debes reemplazar 'entities' por el nombre de tu tabla (ej. 'transfers', 'mints', etc.)
entity_name = st.text_input("Nombre de la Entidad a consultar:", "transfers") 

query_string = f"""
{{
  {entity_name}(first: 10, orderBy: blockNumber, orderDirection: desc) {{
    id
    blockNumber
    timestamp
  }}
}}
"""

if st.button('Ejecutar Consulta GraphQL'):
    with st.spinner('Obteniendo datos...'):
        result = run_query(query_string)
        if result and 'data' in result:
            data_list = result['data'][entity_name]
            if data_list:
                df = pd.DataFrame(data_list)
                st.table(df)
            else:
                st.warning("No se encontraron registros para esta entidad.")

# --- UI: Logs de Sincronización ---
with st.expander("Ver Logs de Depuración (Debug Logs)"):
    st.code("""
    [Info] 1/21/2026 · 16:29:36 - Committed write batch, block: 41110013
    [Debug] 1/21/2026 · 16:29:36 - Processing 1255 triggers
    [Info] 1/21/2026 · 16:29:33 - Committed write batch, block: 41110012
    """, language="bash")
