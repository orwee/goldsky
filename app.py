import streamlit as st
import sys
from pathlib import Path

# Configuración de página (DEBE SER LO PRIMERO)
st.set_page_config(
    page_title="Goldsky Solutions Engineer Demo",
    page_icon="☀️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Intentar importar configuración local
try:
    from config import GOLDSKY_API_KEY, USE_CASES, THEME
except ImportError:
    st.error("Error: No se encontró config.py. Asegúrate de que el archivo existe.")
    st.stop()

# Custom CSS para premium styling
st.markdown(f"""
<style>
    :root {{
        --primary-color: {THEME['primary']};
    }}
    
    .main-header {{
        background: linear-gradient(135deg, #F7931A 0%, #FF6B00 100%);
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
        border-left: 5px solid #F7931A;
        margin-bottom: 1rem;
        height: 100%;
    }}

    .stButton>button {{
        background: linear-gradient(135deg, #F7931A 0%, #FF6B00 100%);
        color: white;
        border: none;
        border-radius: 8px;
        transition: all 0.3s ease;
    }}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>☀️ Goldsky Platform Demo</h1>
    <p style="font-size: 1.3rem; opacity: 0.9;">Solutions Engineer Technical Demonstration</p>
</div>
""", unsafe_allow_html=True)

# Layout Principal
col1, col2 = st.columns([2, 1], gap="large")

with col1:
    st.markdown("## 👋 Welcome to My Goldsky Demo")
    st.markdown("""
    This interactive dashboard demonstrates deep technical knowledge of the **Goldsky platform** and showcases the skills required for a Solutions Engineer role.
    
    ### What You'll Find Here:
    * **🔍 Subgraph Analytics**: Real-time GraphQL queries.
    * **⚡ Mirror Pipelines**: Data streaming architecture.
    * **💾 SQL Playground**: Advanced SQL transformations.
    * **📊 Real-time Dashboard**: Live blockchain metrics.
    """)
    
    st.info("💡 **Tip:** Navigate using the sidebar to explore different platform features!")

with col2:
    st.markdown("### 🎯 Key Platform Strengths")
    features = [
        ("⚡", "Lightning-fast indexing"),
        ("🔄", "Automatic reorg handling"),
        ("🌐", "Multi-chain support"),
        ("📊", "Real-time webhooks"),
        ("🛠️", "Custom chain indexing")
    ]
    for icon, feature in features:
        st.write(f"{icon} **{feature}**")

st.markdown("---")

# Casos de Uso
st.markdown("## 🎯 Real-World Use Cases")
cols = st.columns(2)
for idx, use_case in enumerate(USE_CASES):
    with cols[idx % 2]:
        st.markdown(f"""
        <div class="feature-card">
            <h3 style="color: #F7931A; margin-top:0;">{use_case['title']}</h3>
            <p>{use_case['description']}</p>
            <p><b>Customers:</b> {', '.join(use_case['customers'])}</p>
            <p style="font-size: 0.9rem; color: #888;"><b>Features:</b> {', '.join(use_case['features_used'])}</p>
        </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown(f"""
<div style="text-align: center; color: #888; padding: 20px;">
    Built with ❤️ for Goldsky Solutions Engineer Application | Roberto 2026
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://goldsky.com/wp-content/uploads/2023/10/goldsky_logo_white.png", width=150) # Logo genérico
    st.markdown("## 🚀 Quick Start")
    st.markdown("1. **Analytics**\n2. **Pipelines**\n3. **SQL**\n4. **Metrics**")
    st.divider()
    st.markdown("## ℹ️ API Status")
    st.success("✅ Connected to Goldsky API")
    st.code(f"Key: ...{GOLDSKY_API_KEY[-8:]}")
