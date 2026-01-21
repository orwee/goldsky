import streamlit as st
import requests
import pandas as pd

# Configuración de la página
st.set_page_config(page_title="Goldsky Dashboard", layout="wide")

# 1. Obtener la API Key desde secrets
API_KEY = st.secrets["GOLDSKY_API_KEY"]

# 2. Configurar el endpoint de tu subgraph (cambia esto por tu URL real)
# Ejemplo: https://api.goldsky.com/api/public/project_id/subgraphs/name/version/gn
GOLDSKY_URL = "https://api.goldsky.com/api/public/project_cmkljro9cflkv01wh7po6an10/subgraphs/mysubgraph/1.0.0/gn"

def fetch_goldsky_data(query):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    response = requests.post(GOLDSKY_URL, json={'query': query}, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error {response.status_code}: {response.text}")
        return None

# 3. Definir tu consulta GraphQL
# Personaliza esta consulta según las entidades de tu subgraph
gql_query = """
{
  transfers(first: 10, orderBy: blockTimestamp, orderDirection: desc) {
    id
    from
    to
    value
    blockTimestamp
  }
}
"""

st.title("📊 Panel de Datos Goldsky")

if st.button('Actualizar Datos'):
    with st.spinner('Consultando Goldsky...'):
        data = fetch_goldsky_data(gql_query)
        
        if data and 'data' in data:
            # Extraer la lista de datos (ajustar según tu esquema)
            records = data['data']['transfers']
            df = pd.DataFrame(records)
            
            # Mostrar métricas rápidas
            col1, col2 = st.columns(2)
            col1.metric("Total Registros", len(df))
            col2.metric("Último ID", df['id'].iloc[0] if not df.empty else "N/A")
            
            # Mostrar tabla
            st.subheader("Últimas Transferencias")
            st.dataframe(df, use_container_width=True)
            
            # Ejemplo de gráfico simple si hay valores numéricos
            if 'value' in df.columns:
                df['value'] = pd.to_numeric(df['value'])
                st.line_chart(df['value'])
