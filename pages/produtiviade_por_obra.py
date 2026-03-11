import pandas as pd
import streamlit as st
import plotly.express as px

@st.cache_data
def load_data():
    df = pd.read_excel("df_diarios.xlsx")
    return df

df = load_data()

# Filtrar por mao de obra
df_mao = df[df["tipo_insumo"] == "MAO DE OBRA"].dropna()
st.title("Dashboard de produtividade")
st.warning("Esta análise considera apenas registros de mão de obra. Esse filtro é importante para evitar comparações incoerentes com materiais ou equipamentos.")

sidebar = st.sidebar

sidebar.header("Filtro")
obras_selecionadas = sidebar.multiselect(label="Obra", options=df_mao["nome_obra"].unique().tolist(), default=df_mao["nome_obra"].unique().tolist())

df_filtered = df_mao.copy()
df_filtered = df_filtered[df_filtered["nome_obra"].isin(obras_selecionadas)]

if len(df_filtered) > 0:
    ipd = df_filtered["ip_d"]
    
    # Métricas
    media = ipd.mean()
    mediana = ipd.median()
    amplitude = ipd.max() - ipd.min()
    desvio = ipd.std()
    registros = ipd.count()

    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric(label="Média (ip_d)", value=f"{media:.2f}")
    col2.metric(label="Mediana (ip_d)", value=f"{mediana:.2f}")
    col3.metric(label="Amplitude (ip_d)", value=f"{amplitude:.2f}")
    col4.metric(label="Desvio (ip_d)", value=f"{desvio:.2f}")
    col5.metric(label="Registros (ip_d)", value=f"{registros}")

    fig_box = px.box(
        df_filtered,
        x="nome_obra",
        y="ip_d",
        color="nome_obra",
        points="outliers",
        title="Produtividade por obra"
    )

    df_stats = df_filtered.groupby(["nome_obra"])["ip_d"].agg(
            ["mean", "median"]
        ).reset_index().melt(
            id_vars="nome_obra",
            value_vars=["mean", "median"],
            var_name="metricas",
            value_name="ip_d"
        )

    fig_bar = px.bar(
        df_stats,
        x="nome_obra",
        y="ip_d",
        barmode="group",
        color="metricas",
        title="Média e mediana por obra"
    )
    st.plotly_chart(fig_box, use_container_width=True)
    st.plotly_chart(fig_bar, use_container_width=True)
else:
    st.error("Nenhuma obra foi selecionada")