import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="Painel da Equipe", layout="wide")


@st.cache_data
def carregar_dados():
    dados = {
        "nome": ["Ana", "Bruno", "Carlos", "Dani", "Edu"],
        "idade": [23, 35, 29, np.nan, 40],
        "cidade": ["SP", "RJ", "SP", "MG", "RJ"],
        "salario": [3000, 5000, 4000, 3500, np.nan],
        "data_contratacao": pd.to_datetime(["2020-01-10", "2019-03-15", "2021-07-22", "2022-11-01", "2018-05-20"])
    }
    df = pd.DataFrame(dados)

    df["idade"] = df["idade"].fillna(df["idade"].mean())
    df["salario"] = df["salario"].fillna(df["salario"].median())

    df["salario_anual"] = df["salario"] * 12
    df["ano_contratacao"] = df["data_contratacao"].dt.year

    df["categoria_salario"] = df["salario"].apply(
        lambda x: "Alto" if x > 4500 else "Médio" if x > 3000 else "Baixo"
    )
    return df


st.sidebar.header("📂 Arquivo")
arquivo = st.sidebar.file_uploader("Joga o CSV aqui", type=["csv"])

if arquivo:
    df = pd.read_csv(arquivo)
else:
    df = carregar_dados()

st.sidebar.header("🔎 Filtros")

cidades_selecionadas = st.sidebar.multiselect(
    "Cidades:",
    options=df["cidade"].unique(),
    default=df["cidade"].unique()
)

min_salario = float(df["salario"].min())
max_salario = float(df["salario"].max())

faixa_salarial = st.sidebar.slider(
    "Salário entre:",
    min_salario,
    max_salario,
    (min_salario, max_salario)
)

opcoes_cat = ["Todas"] + list(df["categoria_salario"].unique())
categoria = st.sidebar.selectbox("Categoria salarial:", options=opcoes_cat)

df_filtrado = df[
    (df["cidade"].isin(cidades_selecionadas)) &
    (df["salario"] >= faixa_salarial[0]) &
    (df["salario"] <= faixa_salarial[1])
    ]

if categoria != "Todas":
    df_filtrado = df_filtrado[df_filtrado["categoria_salario"] == categoria]

st.title("📊 Painel da Equipe")

col1, col2, col3 = st.columns(3)

if not df_filtrado.empty:
    col1.metric("Média Salarial", f"R$ {df_filtrado['salario'].mean():.2f}")
    col2.metric("Total de Pessoas", len(df_filtrado))
    col3.metric("Maior Salário", f"R$ {df_filtrado['salario'].max():.2f}")
else:
    col1.metric("Média Salarial", "R$ 0.00")
    col2.metric("Total de Pessoas", 0)
    col3.metric("Maior Salário", "R$ 0.00")

st.subheader("📋 Tabela de Dados")
st.dataframe(df_filtrado, use_container_width=True)

st.subheader("📊 Gráfico")

if not df_filtrado.empty:
    grafico = px.bar(
        df_filtrado,
        x="cidade",
        y="salario",
        color="categoria_salario",
        title="Salários por Cidade",
        barmode="group",
        hover_data={"salario": ':.2f', "nome": True, "cidade": False}
    )
    st.plotly_chart(grafico, use_container_width=True)

st.subheader("🔀 Tabela Dinâmica")

if not df_filtrado.empty:
    pivot = pd.pivot_table(
        df_filtrado,
        values="salario",
        index="cidade",
        columns="categoria_salario",
        aggfunc="mean"
    )
    st.dataframe(pivot)

st.divider()

if not df_filtrado.empty:
    csv = df_filtrado.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="⬇️ Baixar dados filtrados",
        data=csv,
        file_name="dados_limpos.csv",
        mime="text/csv"
    )