import streamlit as st
from src.dcf import calcular_vpl_dcf
from src.wacc import calcular_wacc

st.set_page_config(page_title="Valuation Pro", layout="centered")
st.title("📊 Valuation Pro - DCF & Comparables")

st.sidebar.header("🔍 Parâmetros de Avaliação")
ticker = st.sidebar.text_input("Código da Ação (ex: AAPL, PETR4.SA)", value="AAPL")
risk_free = st.sidebar.number_input("Taxa Livre de Risco (rf)", value=0.04)
market_return = st.sidebar.number_input("Retorno Esperado do Mercado (rm)", value=0.10)
desconto = st.sidebar.slider("Taxa de Desconto (%)", 5.0, 15.0, 10.0)
crescimento_perpetuo = st.sidebar.slider("Crescimento Perpétuo (%)", 0.0, 5.0, 2.0)
anos = st.sidebar.slider("Anos de Projeção", 3, 10, 5)

if st.sidebar.button("Calcular Valuation"):
    with st.spinner("🔄 Coletando dados e calculando..."):
        try:
            wacc = calcular_wacc(ticker, risk_free, market_return)
            resultado = calcular_vpl_dcf(ticker, wacc, crescimento_perpetuo, anos)

            st.subheader("💰 Resultado do Valuation DCF")
            st.metric(label="Valor Justo por Ação (DCF)", value=f"US$ {resultado['valor_justo']:.2f}")
            st.write(f"WACC Utilizado: **{wacc:.2%}**")
            st.write("\n\n")

            st.markdown("---")
            st.subheader("📈 Projeções de Fluxo de Caixa")
            st.dataframe(resultado['fluxo'])

        except Exception as e:
            st.error(f"Erro ao calcular valuation: {e}")
else:
    st.info("Insira um código de ação e clique em 'Calcular Valuation'.")
