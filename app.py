# app.py

import streamlit as st
from src.dcf import calcular_valor_justo_dcf
from src.comparables import valuation_por_multiplos
from src.financials import buscar_dados_financeiros

st.set_page_config(page_title="Valuation Pro", layout="centered")

st.title("\U0001F4C8 Valuation Pro")
st.markdown("Este app realiza o **valuation profissional** de empresas da B3 e NYSE usando Fluxo de Caixa Descontado (DCF) e múltiplos.")

ticker_input = st.text_input("Digite o código da ação (Ex: AAPL, PETR4.SA)", value="AAPL")

if ticker_input:
    dados = buscar_dados_financeiros(ticker_input)

    if dados:
        df_income = dados['income']
        df_cashflow = dados['cashflow']

        st.subheader("\U0001F4CA Dados Financeiros (últimos anos)")
        st.dataframe(df_income[['Total Revenue', 'Net Income']].dropna(), use_container_width=True)

        # === VALUATION POR DCF ===
        st.subheader("\U0001F4B0 Valuation por DCF")

        try:
            fcf = df_cashflow['Total Cash From Operating Activities'] - df_cashflow['Capital Expenditures']
            fcf = fcf.dropna()
            fcf_medio = fcf.mean()

            st.write(f"FCF médio: US$ {fcf_medio:,.2f}")

            crescimento = st.slider("Taxa de crescimento anual (%)", 0.0, 20.0, 5.0) / 100
            desconto = st.slider("Taxa de desconto (%)", 5.0, 20.0, 10.0) / 100
            anos = st.slider("Anos de projeção", 3, 10, 5)

            valor_justo_dcf = calcular_valor_justo_dcf(fcf_medio, crescimento, desconto, anos)
            st.success(f"Valor Justo por DCF: US$ {valor_justo_dcf:,.2f}")

        except Exception as e:
            st.warning("Erro ao calcular DCF. Verifique se a empresa possui dados de FCF.")

        # === VALUATION POR MÚLTIPLOS ===
        st.subheader("\U0001F4A0 Valuation por Múltiplos")

        try:
            import yfinance as yf
            empresa = yf.Ticker(ticker_input)
            pl = empresa.info.get('trailingPE', None)
            lucro_liquido = df_income['Net Income'].iloc[-1]

            if pl and lucro_liquido:
                valor_multiplos = valuation_por_multiplos(pl, lucro_liquido)
                st.success(f"Valor Justo por P/L: US$ {valor_multiplos:,.2f}")
            else:
                st.warning("Múltiplos ou lucro líquido indisponíveis.")
        except:
            st.warning("Erro ao calcular valuation por múltiplos.")
    else:
        st.error("Erro ao buscar os dados financeiros da empresa.")
