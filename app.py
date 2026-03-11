import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(
    page_title="Dashboard de Produtividade - Mão de Obra",
    layout="wide"
)

pg = st.navigation([
    st.Page("pages/base.py", title="Base de Dados"),
    st.Page("pages/produtiviade_por_obra.py", title="Produtividade por obra"),
    st.Page("pages/produtiviade_por_grupo.py", title="Produtividade por grupo"),
])

pg.run()