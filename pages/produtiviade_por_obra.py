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

sidebar = st.sidebar

sidebar.header("Filtro")
obras_selecionadas = sidebar.multiselect(label="Obra", options=df_mao["nome_obra"].unique().tolist(), default=df_mao["nome_obra"].unique().tolist())

tab1, tab2 = st.tabs(["Dashboard", "Conclusão"])

with tab1:
    st.title("Dashboard de produtividade")
    st.warning("Esta análise considera apenas registros de mão de obra. Esse filtro é importante para evitar comparações incoerentes com materiais ou equipamentos.")

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
                media="mean",
                mediana="median"
            ).reset_index().melt(
                id_vars="nome_obra",
                value_vars=["media", "mediana"],
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

with tab2:
    st.title("Conclusão")
    st.warning("Esta análise considera apenas registros de mão de obra. Esse filtro é importante para evitar comparações incoerentes com materiais ou equipamentos.")
    st.warning("O ip_d é a quantidade de recursos gastos dividido pela quantidade de serviço, quanto maior o ip_d, menos produtivo.")

    df_conclusao = [
        {
            "obra": "OBRA_C",
            "produtividade": "Muito alta (menor ip_d)",
            "estabilidade": "Muito estável",
            "analise": "É a obra mais produtiva e consistente. Utiliza poucos recursos para gerar serviço."
        },
        {
            "obra": "OBRA_AER",
            "produtividade": "Alta",
            "estabilidade": "Estável",
            "analise": "Apresenta boa eficiência no uso de recursos e comportamento relativamente consistente."
        },
        {
            "obra": "OBRA_D",
            "produtividade": "Média",
            "estabilidade": "Moderada",
            "analise": "Possui produtividade intermediária, com alguma variação nos dados."
        },
        {
            "obra": "OBRA_AUTO",
            "produtividade": "Baixa",
            "estabilidade": "Instável",
            "analise": "Possui ip_d relativamente alto e presença de outliers, indicando momentos de baixa eficiência."
        },
        {
            "obra": "OBRA_A",
            "produtividade": "Baixa",
            "estabilidade": "Instável",
            "analise": "Apresenta valores extremos que elevam a média, indicando inconsistência na produtividade."
        },
        {
            "obra": "OBRA_B",
            "produtividade": "Muito baixa (maior ip_d)",
            "estabilidade": "Muito instável",
            "analise": "É a obra menos eficiente, com alto consumo de recursos e grande dispersão nos dados."
        }
    ]

    st.dataframe(df_conclusao, use_container_width=True)

    st.success("""
    Conclusão geral: As obras **OBRA_C** e **OBRA_AER** apresentam os melhores desempenhos, 
    combinando alta produtividade e estabilidade. Já **OBRA_B** apresenta o pior desempenho,
    com maior consumo de recursos por quantidade de serviço e alta variabilidade.
    """)