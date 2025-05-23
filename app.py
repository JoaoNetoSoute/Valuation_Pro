import streamlit as st
import yfinance as yf
from modules.dcf import calcular_dcf

st.set_page_config(layout='centered', page_title="Valuation Pro")
st.title("📊 Valuation Profissional por Fluxo de Caixa Descontado (DCF)")

ticker = st.text_input("Digite o ticker da empresa (ex: AAPL, PETR4.SA)", value="AAPL")

if ticker:
    empresa = yf.Ticker(ticker)
    
    st.subheader("📌 Informações Básicas")
    try:
        st.write(empresa.info)
    except:
        st.warning("Não foi possível obter os dados da empresa.")

    st.subheader("📉 Demonstrativo Financeiro")
    df_income = empresa.financials.T
    st.dataframe(df_income[['Total Revenue', 'Net Income']])

    st.subheader("⚙️ Premissas de Valuation")
    receita = df_income['Total Revenue'].iloc[-1]
    margem = st.slider("Margem FCF (%)", 0.0, 50.0, 15.0) / 100
    crescimento = st.slider("Crescimento Anual (%)", 0.0, 30.0, 5.0) / 100
    wacc = st.slider("WACC (%)", 0.0, 20.0, 10.0) / 100
    anos = st.slider("Anos de Projeção", 1, 10, 5)

    valor_justo = calcular_dcf(receita, margem, crescimento, wacc, anos)

    st.subheader("💰 Resultado do Valuation")
    st.success(f"Valor justo estimado: US$ {valor_justo:,.2f}")

