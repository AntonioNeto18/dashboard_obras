import pandas as pd
import streamlit as st

@st.cache_data
def load_data():
    df = pd.read_excel("df_diarios.xlsx")
    return df

df = load_data()

tipo_colunas = [
    {"coluna": "classe", "tipo": "Qualitativa nominal", "descricao": "Tipo geral da atividade executada na obra (ex: furação, concretagem, escavação)."},
    {"coluna": "caderno", "tipo": "Qualitativa nominal", "descricao": "Categoria ou agrupamento de atividades dentro do planejamento ou orçamento da obra."},
    {"coluna": "grupo", "tipo": "Qualitativa nominal", "descricao": "Agrupamento de atividades semelhantes dentro do processo construtivo."},
    {"coluna": "codigo_cc", "tipo": "Qualitativa nominal", "descricao": "Código identificador da composição de custos associada à atividade."},
    {"coluna": "descricao", "tipo": "Qualitativa nominal", "descricao": "Descrição textual detalhada da atividade executada."},
    {"coluna": "unid", "tipo": "Qualitativa nominal", "descricao": "Unidade de medida utilizada para mensurar a atividade (ex: m², m³, m, unidade)."},
    {"coluna": "nova", "tipo": "Quantitativa discreta", "descricao": "Indicador numérico utilizado para identificar ou classificar registros no sistema."},
    {"coluna": "codins", "tipo": "Qualitativa nominal", "descricao": "Código identificador do insumo utilizado na atividade."},
    {"coluna": "insumo", "tipo": "Qualitativa nominal", "descricao": "Nome ou identificação do insumo utilizado na atividade (material, mão de obra ou equipamento)."},
    {"coluna": "unidins", "tipo": "Qualitativa nominal", "descricao": "Unidade de medida utilizada para o insumo (ex: hora, kg, m³)."},
    {"coluna": "tipo_insumo", "tipo": "Qualitativa nominal", "descricao": "Classificação do insumo utilizado, como material, mão de obra ou equipamento."},
    {"coluna": "nome_obra", "tipo": "Qualitativa nominal", "descricao": "Nome da obra onde a atividade foi executada."},
    {"coluna": "id_ccoi_elemento", "tipo": "Qualitativa nominal", "descricao": "Identificador do elemento da composição de custos dentro do sistema."},
    {"coluna": "id_appropriation_composition", "tipo": "Qualitativa nominal", "descricao": "Identificador do registro de apropriação da composição da atividade."},
    {"coluna": "app_inicio", "tipo": "Quantitativa contínua", "descricao": "Data e horário de início da execução ou registro da atividade."},
    {"coluna": "app_fim", "tipo": "Quantitativa contínua", "descricao": "Data e horário de término da execução ou registro da atividade."},
    {"coluna": "qntd", "tipo": "Quantitativa contínua", "descricao": "Quantidade executada da atividade no período registrado."},
    {"coluna": "qs", "tipo": "Quantitativa contínua", "descricao": "Quantidade de serviço realizada na atividade, utilizada para cálculo de produtividade."},
    {"coluna": "data", "tipo": "Quantitativa contínua", "descricao": "Data em que o registro da atividade foi realizado."},
    {"coluna": "qntd_acum", "tipo": "Quantitativa contínua", "descricao": "Quantidade acumulada da atividade executada ao longo do tempo."},
    {"coluna": "qs_acum", "tipo": "Quantitativa contínua", "descricao": "Quantidade acumulada de serviço realizado ao longo do tempo."},
    {"coluna": "ip_d", "tipo": "Quantitativa contínua", "descricao": "Índice de produtividade diário da atividade."},
    {"coluna": "ip_acum", "tipo": "Quantitativa contínua", "descricao": "Índice de produtividade acumulado ao longo do tempo."},
    {"coluna": "elemento", "tipo": "Quantitativa discreta", "descricao": "Identificador numérico do elemento da obra associado à atividade."}
]

st.title("Base e variáveis")
linhas = df.dropna().shape[0]
colunas = df.dropna().shape[1]

st.header(f"Base completa (Linhas: {linhas} | Colunas: {colunas})", text_alignment="center")
st.dataframe(df.head())

st.header("Tipo de variáveis", text_alignment="center")
st.dataframe(pd.DataFrame(tipo_colunas))