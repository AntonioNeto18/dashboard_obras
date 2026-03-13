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
min_registros = 15
df_counts = df_mao.groupby(["grupo"])["ip_d"].count()
grupos_validos = df_counts[df_counts > min_registros].index

sidebar = st.sidebar

sidebar.header("Filtro")
grupos_selecionados = sidebar.multiselect(label="Grupo", options=grupos_validos, default=grupos_validos)

tab1, tab2 = st.tabs(["Dashboard", "Conslusão"])

with tab1:
    st.title("Dashboard de produtividade")
    st.warning("Esta análise considera apenas registros de mão de obra. Esse filtro é importante para evitar comparações incoerentes com materiais ou equipamentos.")
    st.warning(f"Foram considerados para analise, apenas os grupos que possuem mais do que {min_registros} registros, para evitar distorções.")

    df_filtered = df_mao.copy()
    df_filtered = df_filtered[df_filtered["grupo"].isin(grupos_selecionados)]

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
            x="grupo",
            y="ip_d",
            color="grupo",
            points="outliers",
            title="Produtividade por grupo"
        )

        df_stats = df_filtered.groupby(["grupo"])["ip_d"].agg(
                media="mean",
                mediana="median"
            ).reset_index().melt(
                id_vars="grupo",
                value_vars=["media", "mediana"],
                var_name="metricas",
                value_name="ip_d"
            )

        fig_bar = px.bar(
            df_stats,
            x="grupo",
            y="ip_d",
            barmode="group",
            color="metricas",
            title="Média e mediana por grupo"
        )

        df_count = df_filtered.groupby(["grupo"])["ip_d"].agg(
            registros="count"
        ).reset_index()

        fig_count = px.bar(
            df_count,
            x="grupo",
            y="registros",
            color="grupo",
            title="Registros por grupo"
        )

        st.plotly_chart(fig_box, use_container_width=True)

        col1, col2 = st.columns(2)

        col1.plotly_chart(fig_bar, use_container_width=True)
        col2.plotly_chart(fig_count, use_container_width=True)
    else:
        st.error("Nenhuma grupo foi selecionada")