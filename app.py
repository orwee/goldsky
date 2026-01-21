import streamlit as st
import requests
import pandas as pd

# Configuración
st.set_page_config(page_title="Goldsky Debugger", layout="wide")

# API y Endpoint (Extraídos de tu mensaje anterior)
API_KEY = st.secrets["GOLDSKY_API_KEY"]
GOLDSKY_URL = "https://api.goldsky.com/api/public/project_cmkljro9cflkv01wh7po6an10/subgraphs/mysubgraph/1.0.0/gn"

def run_query(query):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    # Aseguramos que el json esté bien formado
    response = requests.post(GOLDSKY_URL, json={'query': query}, headers=headers)
    return response

st.title("🛠 Goldsky Query Debugger")

# 1. Entrada de la entidad (Asegúrate de que este nombre exista en tu subgraph)
# Nota: Si tu subgraph es nuevo, prueba con nombres comunes o revisa tu schema.graphql
entity_name = st.text_input("Nombre de la entidad (ej. transfers, users, swaps):", "transfers").strip()

# 2. Construcción de la consulta con limpieza de espacios
# Usamos triple comilla y verificamos que no falten llaves
query_string = """
{
  %s(first: 10) {
    id
  }
}
""" % entity_name

# --- SECCIÓN DE DEPURACIÓN ---
with st.expander("🔍 Ver consulta generada (Debug)"):
    st.code(query_string, language="graphql")

if st.button('Ejecutar Consulta'):
    if not entity_name:
        st.warning("Por favor, introduce el nombre de una entidad.")
    else:
        with st.spinner('Consultando Goldsky...'):
            response = run_query(query_string)
            
            if response.status_code == 200:
                data = response.json()
                if "errors" in data:
                    st.error(f"Error de GraphQL: {data['errors'][0]['message']}")
                    st.json(data['errors']) # Muestra el error completo para debug
                elif "data" in data and data["data"][entity_name] is not None:
                    df = pd.DataFrame(data["data"][entity_name])
                    st.success("¡Datos recibidos!")
                    st.dataframe(df, use_container_width=True)
                else:
                    st.info("Consulta exitosa, pero no se encontraron datos o la entidad no existe.")
            else:
                st.error(f"Error de conexión (HTTP {response.status_code})")
                st.write(response.text)

# --- TIP: Descubrir entidades ---
st.divider()
st.subheader("💡 ¿No sabes el nombre de tus entidades?")
if st.button("Listar todas las entidades disponibles"):
    schema_query = """
    {
      __schema {
        queryType {
          fields {
            name
          }
        }
      }
    }
    """
    res = run_query(schema_query)
    if res.status_code == 200:
        fields = res.json()['data']['__schema']['queryType']['fields']
        names = [f['name'] for f in fields if not f['name'].startswith('_')]
        st.write("Tus entidades son:", names)
